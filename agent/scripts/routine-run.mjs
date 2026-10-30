#!/usr/bin/env node
// routine-run.mjs: run one routine prompt locally through `claude -p` and the
// 9router proxy (the imps kit's runner), with a zero-model pre-step that can skip
// the model entirely. No secrets live here: the kit's cleanEnv() reads the proxy
// key from the user's own settings at run time.
//
//   node routine-run.mjs --prompt agent/prompts/X.md --pre "node check.mjs" --skip-exit 3 \
//     --model MAX --tools "Read,Bash(node *),Write" --budget 1 --max-turns 30 --minutes 15 \
//     --log agent/logs/routine-run.log --cwd . --out agent/logs/routine-out
//
// Flow: lock -> --pre (exit == skip-exit => idle) -> probe 9router -> claude -p -> out + log.
import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync, statSync, rmSync } from 'node:fs';
import { homedir } from 'node:os';
import { basename, dirname, join, resolve } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';

export const STALE_LOCK_MS = 3 * 60 * 60 * 1000;
export const PRE_OUTPUT_MAX = 8 * 1024;

export const DEFAULTS = {
    model: 'MAX', tools: 'Read,Write', budget: '1', maxTurns: 30, minutes: 15, skipExit: 3,
};

const FLAGS = new Set(['prompt', 'model', 'tools', 'budget', 'max-turns', 'minutes', 'pre', 'skip-exit', 'log', 'cwd', 'out']);

/** Parse `--flag value` argv into a normalized options object. Throws on unknown or incomplete flags. */
export function parseArgs(argv) {
    const raw = {};
    for (let i = 0; i < argv.length; i++) {
        const a = argv[i];
        if (!a.startsWith('--')) throw new Error(`unexpected argument: ${a}`);
        const key = a.slice(2);
        if (!FLAGS.has(key)) throw new Error(`unknown flag: ${a}`);
        if (i + 1 >= argv.length) throw new Error(`missing value for ${a}`);
        raw[key] = argv[++i];
    }
    if (!raw.prompt) throw new Error('--prompt <file> is required');
    const num = (name, v) => {
        const n = Number(v);
        if (!Number.isFinite(n) || n < 0) throw new Error(`--${name} must be a non-negative number`);
        return n;
    };
    const cwd = resolve(raw.cwd || process.cwd());
    return {
        prompt: raw.prompt,
        model: raw.model || DEFAULTS.model,
        tools: splitTools(raw.tools || DEFAULTS.tools),
        budget: num('budget', raw.budget ?? DEFAULTS.budget),
        maxTurns: num('max-turns', raw['max-turns'] ?? DEFAULTS.maxTurns),
        minutes: num('minutes', raw.minutes ?? DEFAULTS.minutes),
        pre: raw.pre || null,
        skipExit: num('skip-exit', raw['skip-exit'] ?? DEFAULTS.skipExit),
        cwd,
        log: resolve(cwd, raw.log || 'agent/logs/routine-run.log'),
        out: resolve(cwd, raw.out || 'agent/logs/routine-out'),
    };
}

/** Split a comma-separated tool list without breaking commas inside parentheses. */
export function splitTools(s) {
    const out = [];
    let depth = 0;
    let cur = '';
    for (const ch of s) {
        if (ch === '(') depth++;
        if (ch === ')') depth = Math.max(0, depth - 1);
        if (ch === ',' && depth === 0) { out.push(cur.trim()); cur = ''; } else cur += ch;
    }
    if (cur.trim()) out.push(cur.trim());
    return out.filter(Boolean);
}

/** Truncate to a byte budget, keeping the head and noting what was dropped. */
export function truncate(text, max = PRE_OUTPUT_MAX) {
    const buf = Buffer.from(text ?? '', 'utf8');
    if (buf.length <= max) return text ?? '';
    return `${buf.subarray(0, max).toString('utf8').replace(/�+$/, '')}\n[truncated ${buf.length - max} bytes]`;
}

/** Take the lock unless a fresh one exists. Returns true when acquired; a lock older than staleMs is replaced. */
export function acquireLock(path, now = Date.now(), staleMs = STALE_LOCK_MS) {
    mkdirSync(dirname(path), { recursive: true });
    if (existsSync(path)) {
        let age = Infinity;
        try { age = now - statSync(path).mtimeMs; } catch { /* vanished: treat as stale */ }
        if (age < staleMs) return false;
        rmSync(path, { force: true });
    }
    writeFileSync(path, JSON.stringify({ pid: process.pid, at: new Date(now).toISOString() }), { flag: 'wx' });
    return true;
}
export const releaseLock = (path) => rmSync(path, { force: true });

/** One log line: date | routine | outcome | turns | tokens. */
export function logLine({ date, routine, outcome, turns = 0, tokens = 0 }) {
    const clean = (v) => String(v).replace(/[|\r\n]+/g, ' ').trim();
    return [date, routine, outcome, turns, tokens].map(clean).join(' | ');
}

export const routineName = (promptPath) => basename(promptPath).replace(/\.[^.]+$/, '');

/** Build the short inline prompt (Windows caps a command line near 32k; no stdin path). */
export function buildPrompt(promptPath, preOut) {
    const head = `Read ${promptPath.replaceAll('\\', '/')} and follow it.`;
    return preOut ? `${head} Pre-step output:\n${truncate(preOut)}` : head;
}

function defaultRunPre(cmd, cwd) {
    const r = spawnSync(cmd, { shell: true, cwd, encoding: 'utf8', windowsHide: true, timeout: 5 * 60_000, maxBuffer: 16 * 1024 * 1024 });
    return { code: r.status, stdout: r.stdout || '', stderr: r.stderr || '', error: r.error?.message };
}

export async function loadKit() {
    const p = readFileSync(join(homedir(), '.imps', 'kit-path.txt'), 'utf8').replace(/^﻿/, '').trim();
    return import(pathToFileURL(join(p, 'imps', 'runner.mjs')).href);
}

/** Same probe the kit dispatcher uses: one tiny real message to the proxy. */
export async function defaultProbe(kit) {
    const env = kit.cleanEnv();
    try {
        const r = await fetch(`${env.ANTHROPIC_BASE_URL.replace(/\/$/, '')}/messages`, {
            method: 'POST',
            signal: AbortSignal.timeout(60_000),
            headers: { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
            body: JSON.stringify({ model: 'MAX', max_tokens: 5, messages: [{ role: 'user', content: 'say ok' }] }),
        });
        return r.ok;
    } catch { return false; }
}

/** Run the whole flow. `deps` lets tests stub the kit, pre-step, probe and clock. Returns the process exit code. */
export async function main(argv, deps = {}) {
    const o = parseArgs(argv);
    const now = deps.now || (() => Date.now());
    const date = new Date(now()).toISOString().slice(0, 10);
    const routine = routineName(o.prompt);
    const log = (outcome, turns = 0, tokens = 0) => {
        mkdirSync(dirname(o.log), { recursive: true });
        appendFileSync(o.log, logLine({ date, routine, outcome, turns, tokens }) + '\n');
    };
    const lock = join(o.out, `.${routine}.lock`);
    if (!acquireLock(lock, now())) { log('locked'); return 0; }
    try {
        let preOut = '';
        if (o.pre) {
            const pre = (deps.runPre || defaultRunPre)(o.pre, o.cwd);
            if (pre.code === o.skipExit) { log('idle'); return 0; }
            preOut = pre.stdout;
            // Fail open, like the kit's precheck.mjs: a broken gate must not silence the routine.
            if (pre.code !== 0) {
                log(`pre-failed exit ${pre.code ?? pre.error ?? 'none'}`);
                preOut = `[pre-step failed with exit ${pre.code}; stderr: ${truncate(pre.stderr, 1024)}]\n${preOut}`;
            }
        }
        const kit = deps.kit || await loadKit();
        if (!(await (deps.probe || defaultProbe)(kit))) { log('skip-9router-down'); return 0; }
        mkdirSync(o.out, { recursive: true });
        const m = await kit.runClaude({
            cwd: o.cwd, prompt: buildPrompt(o.prompt, preOut), model: o.model, tools: o.tools,
            minutes: o.minutes, budget: o.budget, maxTurns: o.maxTurns,
            transcript: join(o.out, `${date}.transcript.jsonl`),
        });
        const tokens = Object.values(m.tokens || {}).reduce((a, b) => a + (Number(b) || 0), 0);
        writeFileSync(join(o.out, `${date}.md`), m.finalText || `(no output; run ended ${m.end})\n`);
        log(m.end, m.turns ?? 0, tokens);
        return m.end === 'success' ? 0 : 1;
    } finally {
        releaseLock(lock);
    }
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
    main(process.argv.slice(2)).then((c) => process.exit(c), (e) => { console.error(`routine-run: ${e.message}`); process.exit(2); });
}
