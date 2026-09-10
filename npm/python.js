const { spawnSync } = require("child_process");

function commands(args) {
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

function runPython(args) {
  for (const cmd of commands(args)) {
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

module.exports = { runPython };
