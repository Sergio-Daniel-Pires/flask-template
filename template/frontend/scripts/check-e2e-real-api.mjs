import { readdir, readFile } from "node:fs/promises";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const e2eDir = fileURLToPath(new URL("../e2e", import.meta.url));

const forbidden = [
  ["page.route", /page\.route\s*\(/],
  ["context.route", /context\.route\s*\(/],
  ["route.fulfill", /\.fulfill\s*\(/],
  ["route.abort", /\.abort\s*\(/],
  ["routeFromHAR", /routeFromHAR\s*\(/],
  ["MSW/setupServer", /\b(?:msw|setupServer)\b/],
];

async function* walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      yield* walk(path);
    } else if (entry.isFile()) {
      yield path;
    }
  }
}

let failed = false;

for await (const file of walk(e2eDir)) {
  if (!/\.(ts|tsx)$/.test(file)) continue;

  const source = await readFile(file, "utf8");
  for (const [label, pattern] of forbidden) {
    if (pattern.test(source)) {
      console.error(
        `E2E guard: ${relative(e2eDir, file)} uses ${label}.`,
      );
      failed = true;
    }
  }
}

if (failed) {
  console.error(
    "E2E tests must exercise the real Flask API. " +
      "Mocking is only allowed in unit/component tests outside frontend/e2e.",
  );
  process.exit(1);
}

console.log("E2E guard: no API route mocking found.");
