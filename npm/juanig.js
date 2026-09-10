#!/usr/bin/env node
const { runPython } = require("./python");

const status = runPython(["-m", "juanig", ...process.argv.slice(2)]);
if (status === null) {
  console.error("juanig needs Python 3. Install Python, then run: npm i -g juanig");
  process.exit(1);
}
process.exit(status);
