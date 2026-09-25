import csv
from collections import Counter

MANIFEST = r'D:\HumanBrain\00_Metadata\download_manifest.csv'

with open(MANIFEST, encoding='utf-8') as fh:
    rows = list(csv.DictReader(fh))

print('Status counts:')
for st, cnt in sorted(Counter(r['status'] for r in rows).items()):
    print(f'  {st}: {cnt}')
print(f'Total: {len(rows)}')
print()

must = [r for r in rows if r['status'] == 'MUST_DOWNLOAD']
print(f'MUST_DOWNLOAD entries ({len(must)}):')
for r in must:
    print(f'  {r["filename"]} -> {r["dest"]} ({r["expected_bytes"]} B)')

# Also check F drive files not in must that are not OK
f_non_ok = [r for r in rows if r['drive'] == 'F' and r['status'] != 'OK']
print(f'\nF non-OK entries ({len(f_non_ok)}):')
for r in f_non_ok:
    print(f'  {r["filename"]} status={r["status"]}')
