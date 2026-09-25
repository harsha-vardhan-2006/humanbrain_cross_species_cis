"""Remove the 18 corrupt MUST_DOWNLOAD F coronal files from disk and purge
their manifest rows so dl_batch.py re-downloads them fresh."""
import csv, os, sys

MANIFEST = r'D:\HumanBrain\00_Metadata\download_manifest.csv'

def main():
    # Load manifest
    with open(MANIFEST, encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    fieldnames = rows[0].keys() if rows else []

    kept = []
    removed_count = 0
    for r in rows:
        if r['status'] == 'MUST_DOWNLOAD':
            dest = r['dest']
            if os.path.exists(dest):
                os.remove(dest)
                print(f'  removed {dest} ({r["filename"]})')
            else:
                print(f'  not on disk: {dest} ({r["filename"]})')
            removed_count += 1
            continue
        kept.append(r)

    # Rewrite manifest without MUST_DOWNLOAD rows
    with open(MANIFEST, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(kept)

    print(f'\nPurged {removed_count} MUST_DOWNLOAD rows from manifest')
    print(f'Manifest now has {len(kept)} rows')

    # Quick status summary
    from collections import Counter
    status_counts = Counter(r['status'] for r in kept)
    print('Status counts:', dict(status_counts))

if __name__ == '__main__':
    main()
