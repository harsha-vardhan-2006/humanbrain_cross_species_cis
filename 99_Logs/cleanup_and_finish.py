"""Dedup manifest (remove MUST_DOWNLOAD + duplicates), then verify + report."""
import csv, os, subprocess, sys
from collections import Counter

LOGS = 'D:\\HumanBrain\\99_Logs'
META = 'D:\\HumanBrain\\00_Metadata'
MANIFEST = os.path.join(META, 'download_manifest.csv')
VERIFY = os.path.join(LOGS, 'verify_downloads.py')
FINAL_REPORT = os.path.join(LOGS, 'final_report.py')

def read_manifest():
    with open(MANIFEST, encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    fn = list(rows[0].keys()) if rows else []
    return rows, fn

def write_manifest(rows, fn):
    with open(MANIFEST, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=fn)
        w.writeheader()
        w.writerows(rows)

# Step A: Remove MUST_DOWNLOAD rows + dedup
print('=== Dedup manifest + remove MUST_DOWNLOAD ===')
rows, fn = read_manifest()
print('Before: %d rows' % len(rows))
print('  Status:', dict(Counter(r['status'] for r in rows)))

# Remove MUST_DOWNLOAD rows
rows = [r for r in rows if r['status'] != 'MUST_DOWNLOAD']
print('After removing MUST_DOWNLOAD: %d rows' % len(rows))

# Dedup: keep last OK per (drive, dest)
seen_idx = {}
for i, r in enumerate(rows):
    seen_idx[(r['drive'], r['dest'])] = i
deduped = [rows[i] for i in sorted(seen_idx.values())]
removed = len(rows) - len(deduped)
if removed:
    print('  removed %d duplicate rows' % removed)
write_manifest(deduped, fn)
print('After dedup: %d rows' % len(deduped))
print('  Status:', dict(Counter(r['status'] for r in deduped)))

# Summary
f_ok = sum(1 for r in deduped if r['drive'] == 'F' and r['status'] == 'OK')
d_ok = sum(1 for r in deduped if r['drive'] == 'D' and r['status'] == 'OK')
print('F OK=%d, D OK=%d' % (f_ok, d_ok))

# Step B: Run verify_downloads.py
print('\n=== Step 5: verify ===')
with open(os.path.join(LOGS, 'continue_verify.log'), 'a', encoding='utf-8') as fh:
    fh.write('\n===== verify_downloads.py =====\n')
    fh.flush()
    rc = subprocess.run([sys.executable, VERIFY], stdout=fh, stderr=subprocess.STDOUT).returncode
print('verify_downloads.py rc=%d' % rc)
vp = os.path.join(META, 'verify_summary.json')
if os.path.exists(vp):
    print('--- verify_summary.json ---')
    print(open(vp, encoding='utf-8').read())

# Step C: Run final_report.py
print('\n=== Step 6: final report ===')
with open(os.path.join(LOGS, 'continue_final.log'), 'a', encoding='utf-8') as fh:
    fh.write('\n===== final_report.py =====\n')
    fh.flush()
    rc = subprocess.run([sys.executable, FINAL_REPORT], stdout=fh, stderr=subprocess.STDOUT).returncode
print('final_report.py rc=%d' % rc)
rp = os.path.join(META, 'ACQUISITION_REPORT.md')
if os.path.exists(rp):
    print('--- ACQUISITION_REPORT.md (first 20 lines) ---')
    for ln in open(rp, encoding='utf-8').readlines()[:20]:
        print(ln.rstrip())
cp = os.path.join(META, 'dataset_catalog.md')
if os.path.exists(cp):
    print('--- dataset_catalog.md ---')
    print(open(cp, encoding='utf-8').read())
