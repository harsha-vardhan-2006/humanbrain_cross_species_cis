"""Deduplicate manifest rows: keep last row per (drive, dest)."""
import csv, os

MANIFEST = r'D:\HumanBrain\00_Metadata\download_manifest.csv'

def main():
    with open(MANIFEST, encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    fieldnames = rows[0].keys() if rows else []

    # Keep last occurrence per (drive, dest)
    seen = {}
    for i, r in enumerate(rows):
        key = (r['drive'], r['dest'])
        seen[key] = i  # last index wins

    deduped = [rows[i] for i in sorted(seen.values())]
    removed = len(rows) - len(deduped)

    with open(MANIFEST, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(deduped)

    print(f'Removed {removed} duplicate rows')
    print(f'Manifest now: {len(deduped)} rows')

    from collections import Counter
    print('Status:', dict(Counter(r['status'] for r in deduped)))
    f_count = sum(1 for r in deduped if r['drive'] == 'F')
    d_count = sum(1 for r in deduped if r['drive'] == 'D')
    print(f'F: {f_count}, D: {d_count}')

if __name__ == '__main__':
    main()
