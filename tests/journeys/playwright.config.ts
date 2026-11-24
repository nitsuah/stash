// Nightly "AI user" journeys for the stash Pages site (pages/), run by
// .github/workflows/journeys.yml through the shared nitsuah/.github harness,
// which files/dedups/closes `bot:journey` issues from the JSON report
// (contract: journeys/STANDARD.md). Baselines are Linux-only: generate them in
// the Playwright Docker image (see README.md).
import path from 'node:path';
import { defineConfig, devices } from '@playwright/test';

const here = __dirname;
const repoRoot = path.resolve(here, '..', '..');
const PORT = 4180;

export default defineConfig({
  testDir: here,
  outputDir: path.join(repoRoot, 'test-results', 'journeys'),
  snapshotPathTemplate: '{testDir}/__screenshots__/{testFilePath}/{testName}/{arg}{ext}',
  // A missing baseline must fail in CI instead of being written and thrown away.
  updateSnapshots: process.env.CI ? 'none' : 'missing',
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0, // pass-on-retry = flaky, not an issue
  timeout: 60_000,
  reporter: [['list'], ['json', { outputFile: path.join(repoRoot, 'journeys-report', 'report.json') }]],
  expect: {
    timeout: 10_000,
    toHaveScreenshot: { maxDiffPixels: 100, animations: 'disabled', caret: 'hide', scale: 'css' },
  },
  webServer: {
    command: `node serve.mjs ../../pages ${PORT}`,
    cwd: here,
    url: `http://127.0.0.1:${PORT}/`,
    reuseExistingServer: false,
    timeout: 30_000,
  },
  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    colorScheme: 'dark',
    locale: 'en-US',
    timezoneId: 'UTC',
    reducedMotion: 'reduce',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } } }],
});
