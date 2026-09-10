#!/usr/bin/env node
const { spawnSync } = require("child_process");

function candidates(args) {
  if (process.platform === "win32") {
    return [
      ["py", "-3", ...args],
      ["python", ...args],
      ["python3", ...args],
    ];
  }
  return [
    ["python3", ...args],
    ["python", ...args],
  ];
}

function run(args) {
  for (const cmd of candidates(args)) {
    const result = spawnSync(cmd[0], cmd.slice(1), {
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    if (result.error && result.error.code === "ENOENT") {
      continue;
    }
    process.exit(result.status ?? 1);
  }
  console.error("juanig needs Python 3. Install Python, then run: npm i -g juanig");
  process.exit(1);
}

run(["-m", "juanig", ...process.argv.slice(2)]);
