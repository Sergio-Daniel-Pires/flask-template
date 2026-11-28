import { spawnSync } from "node:child_process";
import { readFile, rm } from "node:fs/promises";
import { resolve } from "node:path";
import { setTimeout as delay } from "node:timers/promises";

export default async function globalTeardown() {
  const stateFile = resolve(import.meta.dirname, "..", ".e2e-state.json");

  let state: { tempDir: string; pid: number | null } | null = null;
  try {
    state = JSON.parse(await readFile(stateFile, "utf8"));
  } catch {
    return;
  }

  if (!state) return;

  if (state.pid) {
    if (process.platform === "win32") {
      spawnSync("taskkill", ["/pid", String(state.pid), "/T", "/F"], {
        stdio: "ignore",
      });
    } else {
      try {
        process.kill(state.pid, "SIGTERM");
      } catch {
        // Process already exited.
      }
    }
  }

  await delay(500);

  for (let attempt = 0; attempt < 100; attempt += 1) {
    try {
      await rm(state.tempDir, { recursive: true, force: true });
      break;
    } catch {
      await delay(100);
    }
  }

  await rm(stateFile, { force: true });
}
