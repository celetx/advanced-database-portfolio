"""Capture actual saved stdout in a labelled browser viewer.
Requires Python, playwright and Chromium; optional, not required to run MongoDB.
Run.sh must have completed successfully before capturing its stdout.
"""
from pathlib import Path
import hashlib
import html
import json
import os
import subprocess
from playwright.sync_api import sync_playwright

base = Path(__file__).resolve().parent
prefix = 'Osisiogu_Nnabugwu_301930508_'
raw = (base / (prefix + 'ExecutionOutput.txt')).read_text()
if not raw.rstrip().endswith('ALL TESTS PASSED'):
    raise SystemExit('Refusing to capture a log without the successful final verdict')
sha = hashlib.sha256(raw.encode()).hexdigest()
shots = base / 'screenshots'
shots.mkdir(exist_ok=True)
sections = {
    'CRUDAndAggregations': raw.split('=== Tests ===')[0],
    'ValidationResults': raw.split('=== Tests ===')[1].split('Hinted compound')[0]
        + '\n' + raw[raw.rfind('PASS: hinted'):],
}
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'),
                                headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1300, 'height': 900}, device_scale_factor=1)
    for label, content in sections.items():
        page.set_content('<!doctype html><meta charset="utf-8"><title>MongoDB execution output</title>'
                         '<style>body{background:#111827;color:#e5e7eb;padding:24px;font:16px monospace}'
                         'header{color:#93c5fd;font:14px monospace}pre{white-space:pre-wrap;line-height:1.45}</style>'
                         '<header>ACTUAL MONGOSH OUTPUT — browser log viewer (unmodified excerpts)<br>Source: '
                         + prefix + 'ExecutionOutput.txt<br>SHA-256: ' + sha + '</header><pre>'
                         + html.escape(content) + '</pre>')
        page.screenshot(path=str(shots / (prefix + label + '.png')), full_page=True)
    browser.close()
image_digest = subprocess.check_output([
    'env', '-u', 'DOCKER_HOST', '-u', 'DOCKER_CONTEXT', '-u', 'DOCKER_TLS',
    '-u', 'DOCKER_TLS_VERIFY', '-u', 'DOCKER_CERT_PATH',
    'docker', '--host=unix:///var/run/docker.sock', 'image', 'inspect', 'mongo:8.0.16',
    '--format', '{{index .RepoDigests 0}}'
], text=True).strip()
manifest = {
    'log': prefix + 'ExecutionOutput.txt', 'sha256': sha,
    'capture': 'Chromium/Playwright screenshots of actual saved mongosh stdout excerpts; not Codespaces or live terminal screenshots',
    'runCommand': 'bash ' + prefix + 'Run.sh',
    'image': 'mongo:8.0.16', 'imageDigest': image_digest,
    'assertionCount': raw.count('PASS:'), 'runTimestampUTC': raw.splitlines()[0].split(' | ')[1],
    'screenshots': [prefix + key + '.png' for key in sections],
}
(base / (prefix + 'EvidenceManifest.json')).write_text(json.dumps(manifest, indent=2) + '\n')
print('Captured actual output; source SHA-256:', sha)
