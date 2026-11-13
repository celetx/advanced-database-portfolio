// Run from this directory with mongosh --file Osisiogu_Nnabugwu_301930508_Run.js
load('Osisiogu_Nnabugwu_301930508_Common.js');
print('MediCare Portfolio 4 | ' + new Date().toISOString());
print('MongoDB server: ' + clinic.version());
for (const part of ['Setup','CRUD','Aggregations','Tests']) {
  print('\n=== ' + part + ' ===');
  load(prefix + part + '.js');
}
