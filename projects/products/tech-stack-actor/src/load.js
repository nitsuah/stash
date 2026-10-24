// Loads every fingerprints/*.json file. Kept separate from detect.js so tests and the Actor read the data the same way.
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = join(dirname(fileURLToPath(import.meta.url)), '..', 'fingerprints');

export function loadFingerprints() {
    return readdirSync(dir)
        .filter((f) => f.endsWith('.json'))
        .sort()
        .flatMap((f) => JSON.parse(readFileSync(join(dir, f), 'utf8')));
}
