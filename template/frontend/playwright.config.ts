import { existsSync } from "node:fs";
import { resolve } from "node:path";

import { defineConfig, devices } from "@playwright/test";

const projectRoot = resolve(import.meta.dirname, "..");
const venvPython =
  process.platform === "win32"
    ? ".venv/Scripts/python.exe"
    : ".venv/bin/python";
const hasVenv = existsSync(resolve(projectRoot, venvPython));
const backend = hasVenv
  ? `cd .. && "${venvPython}" -m flask --app project.app run`
  : "cd .. && uv run flask --app project.app run";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: "line",
  timeout: 15_000,
  expect: { timeout: 5_000 },
  outputDir: "test-results",
  use: {
    baseURL: "http://127.0.0.1:5050",
    headless: true,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "off",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: {
    // Tests the production path: Vite build served by Flask, SPA fallback included.
    // Port 5050 avoids clashing with the dev server on 5000.
    command: `npm run build && ${backend} --host 127.0.0.1 --port 5050 --no-reload`,
    url: "http://127.0.0.1:5050/healthz",
    timeout: 120_000,
    stdout: "ignore",
    stderr: "pipe",
    env: {
      ...(process.env as Record<string, string>),
      // Relative SQLite paths live in Flask's instance/ directory.
      DATABASE_URL: "sqlite:///e2e.db",
    },
  },
});
