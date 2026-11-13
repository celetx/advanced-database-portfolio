#!/usr/bin/env python3
"""Static/evidence QA only. Does not rerun PostgreSQL or verify any cloud deployment."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

BASE = Path(__file__).resolve().parent
PREFIX = 'Osisiogu_Nnabugwu_301930508_'

def check(ok, message):
    if not ok:
        raise AssertionError(message)
    print('PASS: ' + message)

files = [path for path in BASE.rglob('*') if path.is_file()]
check(all(path.name.startswith(PREFIX) for path in files), 'all submitted filenames use student prefix')
for path in files:
    if path.suffix == '.py':
        ast.parse(path.read_text(), filename=str(path))
    elif path.suffix == '.sh':
        subprocess.run(['bash', '-n', str(path)], check=True)
    elif path.suffix == '.json':
        json.loads(path.read_text())
    elif path.suffix == '.md':
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if not target.startswith(('http:', 'https:', '#')):
                check((path.parent / target.split('#')[0]).is_file(), 'relative link exists: ' + target)
check(True, 'Python AST, Bash syntax and JSON checks')
manifest = json.loads((BASE / (PREFIX + 'EvidenceManifest.json')).read_text())
raw = (BASE / manifest['logFile']).read_text()
check(hashlib.sha256((BASE / manifest['logFile']).read_bytes()).hexdigest() == manifest['logSHA256'], 'raw execution evidence SHA-256')
check(raw.rstrip().endswith('ALL PORTFOLIO 5 TESTS PASSED') and raw.count('PASS:') == 37 == manifest['passAssertionCount'],
      'actual final verdict and 37 assertions match manifest')
for name, digest in manifest['sourceSHA256'].items():
    check(hashlib.sha256((BASE / name).read_bytes()).hexdigest() == digest, 'executed source hash: ' + name)
for name, digest in manifest['screenshots'].items():
    check(hashlib.sha256((BASE / 'screenshots' / name).read_bytes()).hexdigest() == digest, 'screenshot hash: ' + name)
measurements = json.loads(next(line.removeprefix('MEASUREMENTS_JSON: ') for line in raw.splitlines()
                              if line.startswith('MEASUREMENTS_JSON: ')))
check(measurements == json.loads((BASE / (PREFIX + 'Measurements.json')).read_text()), 'measurements match actual raw output')
patterns = [r'AKIA[0-9A-Z]{16}', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
            r'postgres(?:ql)?://[^\s/:]+:[^\s@]+@', r'mongodb(?:\+srv)?://[^\s/:]+:[^\s@]+@']
for path in files:
    if path.suffix in {'.py', '.sh', '.sql', '.conf', '.json', '.md', '.txt'}:
        check(not any(re.search(pattern, path.read_text()) for pattern in patterns), 'focused credential scan: ' + path.name)
repo = BASE.parents[1]
if (repo / '.git').exists():
    prior = [str(BASE.parent / name) for name in ('portfolio-1-database-design', 'portfolio-2-query-optimisation',
                                               'portfolio-3-transactions-concurrency', 'portfolio-4-nosql')]
    diff = subprocess.check_output(['git', '-C', str(repo), 'diff', '20ed34d', '--', *prior], text=True)
    check(not diff, 'Portfolios 1–4 unchanged from reviewed base commit 20ed34d')
else:
    print('SKIP: Git preservation check requires original repository with base commit 20ed34d')
print('STATIC AND EVIDENCE QA PASSED')
