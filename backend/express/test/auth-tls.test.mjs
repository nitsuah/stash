import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import http from 'node:http';

const require = createRequire(import.meta.url);

process.env.JWT_SECRET = 'test-secret-' + 'x'.repeat(32);
process.env.DATABASE_URL = 'postgres://u:p@127.0.0.1:1/x'; // never connected; models are stubbed below
process.env.NODE_ENV = 'test';
// Pin everything app.js reads at import so dotenv or the host env cannot change results.
process.env.PGSSL_CA = ['-----BEGIN CERTIFICATE-----', 'TEST', '-----END CERTIFICATE-----', ''].join('\n');
process.env.PORT = '0';
for (const k of ['DEMO_EMAIL', 'DEMO_LOGIN_ENABLED', 'DEMO_PASSWORD', 'PGSSL_REJECT_UNAUTHORIZED']) delete process.env[k];

const mod = require('../app.js');
const { createApp, User, sequelize } = mod;

// In-memory stand-in for the user table so no database driver is needed.
const store = new Map();
User.findOne = async ({ where }) => store.get(where.email) || null;
User.create = async ({ email, name }) => {
  const u = { id: store.size + 1, email, name, role: 'viewer' };
  store.set(email, u);
  return u;
};
sequelize.sync = async () => {};

let server;
let base;

before(async () => {
  const app = await createApp();
  server = http.createServer(app);
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  base = `http://127.0.0.1:${server.address().port}`;
});

after(() => server.close());

async function login(email, password) {
  const res = await fetch(`${base}/auth/login`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  return { status: res.status, body: await res.json() };
}

async function withEnv(vars, fn) {
  const saved = {};
  for (const k of Object.keys(vars)) saved[k] = process.env[k];
  for (const [k, v] of Object.entries(vars)) {
    if (v === undefined) delete process.env[k]; else process.env[k] = v;
  }
  try {
    return await fn();
  } finally {
    for (const [k, v] of Object.entries(saved)) {
      if (v === undefined) delete process.env[k]; else process.env[k] = v;
    }
  }
}

const on = (extra = {}) => ({ DEMO_LOGIN_ENABLED: 'true', ...extra });

test('demo login is off by default with NODE_ENV and DEMO_LOGIN_ENABLED unset', async () => {
  await withEnv({ NODE_ENV: undefined, DEMO_LOGIN_ENABLED: undefined }, async () => {
    assert.equal((await login('user@example.com', 'password')).status, 401);
  });
});

test('only exactly "true" or "1" enables demo login', async () => {
  for (const v of ['', 'false', '0', 'yes', 'on', 'True', 'TRUE', ' true', 'true ', 'maybe']) {
    await withEnv({ DEMO_LOGIN_ENABLED: v }, async () => {
      assert.equal((await login('user@example.com', 'password')).status, 401, JSON.stringify(v));
    });
  }
  for (const v of ['true', '1']) {
    await withEnv({ DEMO_LOGIN_ENABLED: v }, async () => {
      assert.equal((await login('user@example.com', 'password')).status, 200, v);
    });
  }
});

test('enabled flag works regardless of NODE_ENV (non-production)', async () => {
  for (const env of [undefined, 'development', 'test', 'staging']) {
    await withEnv(on({ NODE_ENV: env }), async () => {
      assert.equal((await login('user@example.com', 'password')).status, 200, String(env));
    });
  }
});

test('production refuses the default demo password even when enabled', async () => {
  await withEnv(on({ NODE_ENV: 'production' }), async () => {
    assert.equal((await login('user@example.com', 'password')).status, 401);
  });
});

test('production allows a custom demo password', async () => {
  await withEnv(on({ NODE_ENV: 'production', DEMO_PASSWORD: 's3cret-demo-pw' }), async () => {
    assert.equal((await login('user@example.com', 's3cret-demo-pw')).status, 200);
    assert.equal((await login('user@example.com', 'password')).status, 401);
  });
});

test('DEMO_PASSWORD overrides the demo password outside production', async () => {
  await withEnv(on({ DEMO_PASSWORD: 'other-pw' }), async () => {
    assert.equal((await login('user@example.com', 'other-pw')).status, 200);
    assert.equal((await login('user@example.com', 'password')).status, 401);
  });
});

test('demo password with another email is rejected and creates no user', async () => {
  await withEnv(on(), async () => {
    const r = await login('someone@else.com', 'password');
    assert.equal(r.status, 401);
    assert.equal(store.has('someone@else.com'), false);
  });
});

test('demo password with the demo email works when enabled', async () => {
  await withEnv(on(), async () => {
    const r = await login('user@example.com', 'password');
    assert.equal(r.status, 200);
    assert.ok(r.body.access_token);
  });
});

test('wrong password for the demo email is rejected', async () => {
  await withEnv(on(), async () => {
    assert.equal((await login('user@example.com', 'nope')).status, 401);
  });
});

test('DEMO_EMAIL overrides the demo account', async () => {
  await withEnv(on({ DEMO_EMAIL: 'demo@corp.example.com' }), async () => {
    assert.equal((await login('demo@corp.example.com', 'password')).status, 200);
    assert.equal((await login('user@example.com', 'password')).status, 401);
  });
});

test('startup logs one line saying whether demo login is on', async () => {
  const cases = [
    [{}, 'Demo login: disabled'],
    [{ DEMO_LOGIN_ENABLED: 'true' }, 'Demo login: enabled'],
    [{ DEMO_LOGIN_ENABLED: 'true', NODE_ENV: 'production' }, 'Demo login: disabled'],
  ];
  for (const [vars, expected] of cases) {
    await withEnv({ DEMO_LOGIN_ENABLED: undefined, NODE_ENV: undefined, ...vars }, async () => {
      const lines = [];
      const orig = console.log;
      const origWarn = console.warn;
      console.log = m => lines.push(String(m));
      console.warn = () => {};
      try {
        await createApp();
      } finally {
        console.log = orig;
        console.warn = origWarn;
      }
      assert.deepEqual(lines.filter(l => l.startsWith('Demo login')), [expected]);
    });
  }
});

test('postgres TLS verifies certificates by default', () => {
  const o = mod.dbDialectOptions('postgres://u:p@db.example.com/x', {});
  assert.equal(o.ssl.require, true);
  assert.equal(o.ssl.rejectUnauthorized, true);
  assert.equal(o.ssl.ca, undefined);
});

test('PGSSL_REJECT_UNAUTHORIZED=false is an explicit opt-out', () => {
  const warns = [];
  const orig = console.warn;
  console.warn = m => warns.push(m);
  try {
    const o = mod.dbDialectOptions('postgresql://u:p@h/x', { PGSSL_REJECT_UNAUTHORIZED: 'false' });
    assert.equal(o.ssl.rejectUnauthorized, false);
  } finally {
    console.warn = orig;
  }
  assert.equal(warns.length, 1);
});

test('PGSSL_CA accepts a PEM string or a file path (path read, not passed through)', async () => {
  const pem = '-----BEGIN CERTIFICATE-----\nABC\n-----END CERTIFICATE-----\n';
  assert.equal(mod.dbDialectOptions('postgres://h/x', { PGSSL_CA: pem }).ssl.ca, pem);
  const fs = await import('node:fs');
  const os = await import('node:os');
  const path = await import('node:path');
  const f = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'ca-')), 'ca.pem');
  fs.writeFileSync(f, pem);
  assert.equal(mod.dbDialectOptions('postgres://h/x', { PGSSL_CA: f }).ssl.ca, pem);
});

test('PGSSL_CA that is neither PEM nor a readable file fails at startup', () => {
  const missing = '/nonexistent/ca-missing.pem';
  assert.throws(
    () => mod.dbDialectOptions('postgres://h/x', { PGSSL_CA: missing }),
    err => err.message.includes('PGSSL_CA') && err.message.includes(missing),
  );
});

test('non-postgres URLs get no ssl options', () => {
  assert.deepEqual(mod.dbDialectOptions('sqlite::memory:', {}), {});
});
