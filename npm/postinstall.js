const { spawnSync } = require("child_process");
const path = require("path");

const root = path.join(__dirname, "..");

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
    return result.status ?? 1;
  }
  return null;
}

const status = run(["-m", "pip", "install", "--upgrade", root]);
if (status === null) {
  console.warn("juanig: Python 3 was not found. Install Python, then run:");
  console.warn(`  python -m pip install "${root}"`);
  process.exit(0);
}
if (status !== 0) {
  console.error("juanig: pip install failed. Install Python 3 and pip, then retry npm i -g juanig.");
  process.exit(status);
}

run(["-m", "juanig", "--install-skills"]);
