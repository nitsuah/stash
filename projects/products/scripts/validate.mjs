// Dependency-free check for every package under projects/products: release.json is sane, listed files exist,
// the version file parses, and extension manifests meet the Chrome Web Store basics. Usage: node validate.mjs [packageName]
import { readdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const only = process.argv[2];
const problems = [];
const fail = (pkg, msg) => problems.push(`${pkg}: ${msg}`);
const readJson = (pkg, file) => {
  try { return JSON.parse(readFileSync(join(root, pkg, file), 'utf8')); } catch (e) { fail(pkg, `${file} is missing or invalid JSON (${e.message})`); return null; }
};

const KNOWN_TARGETS = new Set(['chrome-web-store', 'apify', 'npm', 'vscode']);
const packages = readdirSync(root).filter((n) => statSync(join(root, n)).isDirectory() && existsSync(join(root, n, 'release.json')) && (!only || n === only));
if (!packages.length) fail('(none)', only ? `no package named ${only}` : 'no packages found');

for (const pkg of packages) {
  const rel = readJson(pkg, 'release.json');
  if (!rel) continue;
  for (const t of rel.targets ?? []) if (!KNOWN_TARGETS.has(t)) fail(pkg, `unknown target ${t}`);
  if (!rel.targets?.length) fail(pkg, 'targets is empty');
  for (const f of rel.packageFiles ?? []) if (!existsSync(join(root, pkg, f))) fail(pkg, `listed file is missing: ${f}`);
  const ver = readJson(pkg, rel.versionFile ?? 'package.json');
  if (ver && !/^\d+\.\d+\.\d+$/.test(ver.version ?? '')) fail(pkg, `version "${ver?.version}" is not x.y.z`);
  if (rel.targets?.includes('chrome-web-store') && ver) {
    if (ver.manifest_version !== 3) fail(pkg, 'manifest_version must be 3');
    if ((ver.name ?? '').length > 75) fail(pkg, 'name is over 75 characters');
    if ((ver.description ?? '').length > 132) fail(pkg, 'description is over 132 characters');
    for (const size of ['16', '48', '128']) if (!ver.icons?.[size] || !existsSync(join(root, pkg, ver.icons[size]))) fail(pkg, `icon ${size} missing`);
  }
  if (rel.targets?.includes('apify')) {
    const actor = readJson(pkg, '.actor/actor.json');
    if (actor && actor.actorSpecification !== 1) fail(pkg, 'actor.json actorSpecification must be 1');
    readJson(pkg, '.actor/input_schema.json');
  }
  console.log(`checked ${pkg} (${(rel.targets ?? []).join(', ')})`);
}

if (problems.length) {
  console.error(problems.map((p) => `FAIL ${p}`).join('\n'));
  process.exit(1);
}
console.log('all packages valid');
