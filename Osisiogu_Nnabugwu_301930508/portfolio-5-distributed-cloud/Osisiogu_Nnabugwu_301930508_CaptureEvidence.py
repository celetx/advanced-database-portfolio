"""Create genuine browser screenshots of recorded PostgreSQL stdout (not a terminal).
Optional dependencies: Python Playwright and Chromium. Database runner does not need them.
"""
import hashlib
import html
import json
import os
from pathlib import Path
import subprocess
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
PREFIX = 'Osisiogu_Nnabugwu_301930508_'
log_path = BASE / (PREFIX + 'ExecutionOutput.txt')
raw = log_path.read_text()
if not raw.rstrip().endswith('ALL PORTFOLIO 5 TESTS PASSED'):
    raise SystemExit('Execution log lacks the final success verdict')
sha = hashlib.sha256(log_path.read_bytes()).hexdigest()
sections = {}
headings = [line for line in raw.splitlines() if line.startswith('=== ')]
chunks = [raw.split(heading, 1)[1].split('\n=== ', 1)[0] for heading in headings]
sections['SetupAndStreaming'] = headings[0] + chunks[0]
sections['ReplicatedChanges'] = headings[1] + chunks[1] + '\n' + headings[2] + chunks[2]
sections['PromotionAndRejoin'] = headings[3] + chunks[3] + '\n' + headings[4] + chunks[4]
sections['RestoreAndVerdict'] = headings[5] + chunks[5]
shots = BASE / 'screenshots'
shots.mkdir(exist_ok=True)
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'),
                                headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=1)
    for label, content in sections.items():
        page.set_content('<!doctype html><meta charset="utf-8"><title>Recorded PostgreSQL output</title>'
                         '<style>body{background:white;color:#162433;font:15px sans-serif;margin:28px}'
                         'header{border-bottom:2px solid #64748b;padding-bottom:16px}'
                         'pre{font:14px monospace;line-height:1.5;white-space:pre-wrap;overflow-wrap:anywhere}</style>'
                         '<header><h2>Portfolio 5 — recorded PostgreSQL execution output</h2>'
                         '<p>Actual saved output excerpt. This is a browser log viewer, not a live terminal or Codespaces screenshot.</p>'
                         '<p>Source: ' + PREFIX + 'ExecutionOutput.txt<br>SHA-256: ' + sha + '</p></header><pre>'
                         + html.escape(content) + '</pre>')
        page.screenshot(path=str(shots / (PREFIX + label + '.png')), full_page=True)
    browser.close()
metrics = json.loads(next(line.removeprefix('MEASUREMENTS_JSON: ') for line in raw.splitlines()
                          if line.startswith('MEASUREMENTS_JSON: ')))
(BASE / (PREFIX + 'Measurements.json')).write_text(json.dumps(metrics, indent=2) + '\n')
implementation = ['Schema.sql', 'SampleData.sql', 'Setup.sql', 'ReplicatedChanges.sql', 'Transaction.sql',
                  'Queries.sql', 'Primary.conf', 'PgHba.conf', 'Run.py', 'Run.sh']
manifest = {
    'status': 'actual successful managed-cloud Docker execution; not a managed PostgreSQL deployment',
    'runCommand': 'bash ' + PREFIX + 'Run.sh', 'exitCode': 0,
    'runTimestampUTC': raw.splitlines()[0].split(' | ')[1],
    'postgresqlVersion': '16.11', 'dockerImage': 'postgres:16.11-bookworm',
    'imageDigest': next(line.removeprefix('PostgreSQL image: ') for line in raw.splitlines()
                        if line.startswith('PostgreSQL image: ')),
    'logFile': log_path.name, 'logSHA256': sha, 'passAssertionCount': raw.count('PASS:'),
    'sourceSHA256': {PREFIX + name: hashlib.sha256((BASE / (PREFIX + name)).read_bytes()).hexdigest()
                     for name in implementation},
    'screenshots': {PREFIX + label + '.png': hashlib.sha256((shots / (PREFIX + label + '.png')).read_bytes()).hexdigest()
                    for label in sections},
    'capture': 'Chromium/Playwright screenshots of unmodified actual log sections in a labelled plain log viewer',
    'untested': ['CloudVerification.sql against a managed cloud database', 'student Codespaces execution',
                 'multi-host or multi-AZ failures', 'automatic failover', 'WAN performance', 'cloud PITR'],
}
(BASE / (PREFIX + 'EvidenceManifest.json')).write_text(json.dumps(manifest, indent=2) + '\n')
print('Saved four output-viewer screenshots; actual assertions:', manifest['passAssertionCount'])
