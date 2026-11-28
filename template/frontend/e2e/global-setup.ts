import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { basename, join, resolve } from "node:path";
import { setTimeout as delay } from "node:timers/promises";

export default async function globalSetup() {
  const frontendDir = resolve(import.meta.dirname, "..");
  const projectRoot = resolve(frontendDir, "..");
  const stateFile = resolve(frontendDir, ".e2e-state.json");
  const healthUrl = "http://127.0.0.1:5050/healthz";

  try {
    await fetch(healthUrl);
    throw new Error(
      "Port 5050 is already in use. Stop the process using it; E2E never reuses a server.",
    );
  } catch (error) {
    if (error instanceof Error && error.message.includes("already in use")) {
      throw error;
    }
  }

  const tempDir = await mkdtemp(
    join(tmpdir(), `flask-e2e-${basename(projectRoot)}-`),
  );
  const databasePath = join(tempDir, "e2e.db").replaceAll("\\", "/");
  const venvPython =
    process.platform === "win32"
      ? ".venv/Scripts/python.exe"
      : ".venv/bin/python";
  const hasVenv = existsSync(resolve(projectRoot, venvPython));

  const command = hasVenv ? resolve(projectRoot, venvPython) : "uv";
  const args = hasVenv
    ? ["-m", "flask", "--app", "project.app", "run"]
    : ["run", "flask", "--app", "project.app", "run"];

  const backend = spawn(
    command,
    [...args, "--host", "127.0.0.1", "--port", "5050", "--no-reload"],
    {
      cwd: projectRoot,
      env: {
        ...process.env,
        APP_PROFILE: "test",
        FLASK_ENV: "test",
        FLASK_DEBUG: "0",
        DATABASE_URL: `sqlite:///${databasePath}`,
      },
      stdio: "inherit",
    },
  );

  await writeFile(
    stateFile,
    JSON.stringify({ tempDir, pid: backend.pid ?? null }),
    "utf8",
  );

  const deadline = Date.now() + 60_000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(healthUrl);
      if (response.ok) {
        console.log(`[e2e] temporary SQLite: ${databasePath}`);
        return;
      }
    } catch {
      // Server is still starting.
    }

    if (backend.exitCode !== null) {
      throw new Error(`E2E backend exited with code ${backend.exitCode}`);
    }

    await delay(250);
  }

  throw new Error("E2E backend did not become healthy within 60 seconds");
}
