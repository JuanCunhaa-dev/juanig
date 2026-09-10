const path = require("path");
const { runPython } = require("./python");

const root = path.join(__dirname, "..");
const status = runPython(["-m", "pip", "install", "--upgrade", root]);
if (status === null) {
  console.error("juanig: Python 3 was not found. Install Python, then run:");
  console.error(`  python -m pip install "${root}"`);
  process.exit(1);
}
if (status !== 0) {
  console.error("juanig: pip install failed. Install Python 3 and pip, then retry npm i -g juanig.");
  process.exit(status);
}

runPython(["-m", "juanig", "--install-skills"]);
