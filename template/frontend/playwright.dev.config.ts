import { defineConfig, devices } from "@playwright/test";

/**
 * Fast local loop: reuses the dev servers you already have running.
 *
 *   npm run dev          # in one terminal (Vite)
 *   uv run flask ...     # in another (API)
 *   npm run test:e2e:dev # instant when both are warm
 */
export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  workers: 2,
  reporter: "line",
  timeout: 15_000,
  expect: { timeout: 5_000 },
  use: {
    baseURL: "http://127.0.0.1:5173",
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
  webServer: [
    {
      command:
        "cd .. && uv run flask --app project.app run --host 127.0.0.1 --port 5000 --no-reload",
      url: "http://127.0.0.1:5000/healthz",
      reuseExistingServer: true,
      timeout: 120_000,
      env: {
        ...(process.env as Record<string, string>),
        DATABASE_URL: "sqlite:///e2e.db",
      },
    },
    {
      command: "npm run dev -- --host 127.0.0.1 --port 5173",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: true,
      timeout: 120_000,
    },
  ],
});
