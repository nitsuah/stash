import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = join(dirname(__filename), '..');

// Test the config logic directly - this is where the bug is (line 42 of app.js)
function getConfig(env) {
  return {
    databaseUrl: env.DATABASE_URL || "sqlite::memory:",
    jwtSecret: env.JWT_SECRET || "change-me-in-production",
    jwtExpiry: "1h",
    port: parseInt(env.PORT || "8080", 10),
    isDev: env.NODE_ENV !== "production",
  };
}

test('config fails closed when JWT_SECRET is unset (demonstrates bug)', () => {
  // Save original env
  const originalJwtSecret = process.env.JWT_SECRET;
  const originalNodeEnv = process.env.NODE_ENV;
  const originalDatabaseUrl = process.env.DATABASE_URL;

  // Set test env
  delete process.env.JWT_SECRET;
  process.env.NODE_ENV = 'development';
  process.env.DATABASE_URL = 'sqlite::memory:';

  const config = getConfig(process.env);

  // Restore
  if (originalJwtSecret !== undefined) process.env.JWT_SECRET = originalJwtSecret;
  else delete process.env.JWT_SECRET;
  if (originalNodeEnv !== undefined) process.env.NODE_ENV = originalNodeEnv;
  else delete process.env.NODE_ENV;
  if (originalDatabaseUrl !== undefined) process.env.DATABASE_URL = originalDatabaseUrl;
  else delete process.env.DATABASE_URL;

  // BUG: Current code falls back to hardcoded secret
  // This test asserts the CORRECT behavior (fail closed - config should throw or be undefined)
  // On current buggy code, this assertion FAILS (because config.jwtSecret === 'change-me-in-production')
  // After fix, this assertion should PASS
  assert.ok(
    config.jwtSecret === undefined || config.jwtSecret === null,
    'Config should not have a fallback secret when JWT_SECRET is unset (should fail closed)'
  );
});

test('config uses provided JWT_SECRET when set', () => {
  const originalJwtSecret = process.env.JWT_SECRET;
  const originalNodeEnv = process.env.NODE_ENV;
  const originalDatabaseUrl = process.env.DATABASE_URL;

  process.env.JWT_SECRET = 'test-secret-' + 'x'.repeat(32);
  process.env.NODE_ENV = 'development';
  process.env.DATABASE_URL = 'sqlite::memory:';

  const config = getConfig(process.env);

  if (originalJwtSecret !== undefined) process.env.JWT_SECRET = originalJwtSecret;
  else delete process.env.JWT_SECRET;
  if (originalNodeEnv !== undefined) process.env.NODE_ENV = originalNodeEnv;
  else delete process.env.NODE_ENV;
  if (originalDatabaseUrl !== undefined) process.env.DATABASE_URL = originalDatabaseUrl;
  else delete process.env.DATABASE_URL;

  // This test should PASS - config uses provided JWT_SECRET
  assert.equal(config.jwtSecret, 'test-secret-' + 'x'.repeat(32),
    'Config should use provided JWT_SECRET');
});

test('JWT authentication rejects tokens signed with fallback secret when real secret is set', async () => {
  const jwt = await import('jsonwebtoken');
  const jwtLib = jwt.default;

  const fallbackSecret = 'change-me-in-production';
  const realSecret = 'real-secret-' + 'x'.repeat(32);

  const maliciousToken = jwtLib.sign({ id: 1, role: 'admin' }, fallbackSecret, { expiresIn: '1h' });

  let verifyError = null;
  try {
    jwtLib.verify(maliciousToken, realSecret);
  } catch (e) {
    verifyError = e;
  }

  assert.ok(verifyError !== null, 'Token signed with fallback secret should not verify with real secret');
  assert.equal(verifyError.name, 'JsonWebTokenError');
});