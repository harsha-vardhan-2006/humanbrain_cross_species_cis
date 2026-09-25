import csv
from collections import Counter

MANIFEST = r'D:\HumanBrain\00_Metadata\download_manifest.csv'

with open(MANIFEST, encoding='utf-8') as fh:
    rows = list(csv.DictReader(fh))

print('Status:', dict(Counter(r['status'] for r in rows)))
print('Total:', len(rows))

f_rows = [r for r in rows if r['drive'] == 'F']
d_rows = [r for r in rows if r['drive'] == 'D']
print(f'F drive: {len(f_rows)} rows')
print(f'D drive: {len(d_rows)} rows')

files = [r['dest'] for r in rows]
print(f'Unique destinations: {len(set(files))}')
dups = set(d for d in files if files.count(d) > 1)
print(f'Duplicate destinations: {len(dups)}')
for d in list(dups)[:5]:
    print(f'  Dup: {d}')
    for r in rows:
        if r['dest'] == d:
            print(f'    {r["filename"]} {r["status"]} {r["drive"]} {r["expected_bytes"]}')
