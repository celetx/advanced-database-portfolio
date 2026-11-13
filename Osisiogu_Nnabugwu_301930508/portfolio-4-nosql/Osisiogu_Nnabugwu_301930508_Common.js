// Shared helpers; run from the Portfolio 4 directory with mongosh.
const fs = require('fs');
const prefix = 'Osisiogu_Nnabugwu_301930508_';
const clinic = db.getSiblingDB('medicare_portfolio4');
function check(ok, message) { if (!ok) throw new Error(message); print('PASS: ' + message); }
function show(label, value) { print('\n' + label); print(EJSON.stringify(value, null, 2)); }
function readData(name) { return EJSON.parse(fs.readFileSync(prefix + name + '.json', 'utf8')); }
function rejected(action, code, label) {
  let caught = false;
  try { action(); } catch (error) { if (error.code !== code) throw error; caught = true; }
  check(caught, label);
}
