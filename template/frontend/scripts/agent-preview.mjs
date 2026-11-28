import { spawn, spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { resolve } from "node:path";

const frontendDir = resolve(import.meta.dirname, "..");
const projectRoot = resolve(frontendDir, "..");
const venvPython =
  process.platform === "win32"
    ? ".venv/Scripts/python.exe"
    : ".venv/bin/python";
const hasVenv = existsSync(resolve(projectRoot, venvPython));
const npmCommand = process.platform === "win32" ? "npm.cmd" : "npm";

const backendCommand = hasVenv ? resolve(projectRoot, venvPython) : "uv";
const backendArgs = hasVenv
  ? ["-m", "flask", "--app", "project.app", "run"]
  : ["run", "flask", "--app", "project.app", "run"];
const databasePath = resolve(projectRoot, "instance", "preview.db")
  .replaceAll("\\", "/");

const backend = spawn(
  backendCommand,
  [...backendArgs, "--host", "127.0.0.1", "--port", "5051", "--no-reload"],
  {
    cwd: projectRoot,
    env: {
      ...process.env,
      APP_PROFILE: "preview",
      FLASK_ENV: "development",
      DATABASE_URL: `sqlite:///${databasePath}`,
    },
    stdio: "inherit",
  },
);

const frontend = spawn(
  npmCommand,
  ["run", "dev", "--", "--host", "127.0.0.1", "--port", "5273"],
  {
    cwd: frontendDir,
    env: {
      ...process.env,
      VITE_API_TARGET: "http://127.0.0.1:5051",
    },
    shell: process.platform === "win32",
    stdio: "inherit",
  },
);

let stopping = false;

function stop(child) {
  if (!child || child.exitCode !== null) return;

  if (process.platform === "win32") {
    spawnSync("taskkill", ["/pid", String(child.pid), "/T", "/F"], {
      stdio: "ignore",
    });
  } else {
    child.kill("SIGTERM");
  }
}

function shutdown(code) {
  if (stopping) return;
  stopping = true;
  stop(frontend);
  stop(backend);
  process.exit(code);
}

backend.on("exit", (code) => shutdown(code ?? 0));
frontend.on("exit", (code) => shutdown(code ?? 0));
process.on("SIGINT", () => shutdown(0));
process.on("SIGTERM", () => shutdown(0));

console.log(`[preview] SQLite: ${databasePath}`);
console.log("[preview] API:  http://127.0.0.1:5051");
console.log("[preview] App:  http://127.0.0.1:5273");
