// Tiny static server for pages/ (no dependencies): `node serve.mjs <dir> <port>`.
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve(process.argv[2] ?? '../../pages');
const port = Number(process.argv[3] ?? 4180);
// pages.yml copies generated visuals into pages/assets at deploy time; mirror that here.
const repo = path.resolve(root, '..');
const generated = [
  [/^\/assets\/diagrams\/(.+)$/, name => path.join(repo, 'docs', 'diagrams', name)],
  [/^\/assets\/(vault-graph\.[a-z]+)$/, name => path.join(repo, 'docs', 'screenshots', name)],
];
const types = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.mp4': 'video/mp4',
  '.svg': 'image/svg+xml',
};

createServer(async (req, res) => {
  const url = new URL(req.url ?? '/', 'http://x');
  let file = path.join(root, decodeURIComponent(url.pathname));
  if (!file.startsWith(root)) {
    res.writeHead(403).end();
    return;
  }
  try {
    for (const [re, to] of generated) {
      const m = re.exec(url.pathname);
      if (m && !(await stat(file).catch(() => null))) file = to(path.basename(m[1]));
    }
    if ((await stat(file)).isDirectory()) file = path.join(file, 'index.html');
    const body = await readFile(file);
    res.writeHead(200, { 'content-type': types[path.extname(file)] ?? 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404, { 'content-type': 'text/plain' }).end('not found');
  }
}).listen(port, '127.0.0.1');
