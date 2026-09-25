import csv, os, subprocess, sys

LOGS = 'D:\\HumanBrain\\99_Logs'
META = 'D:\\HumanBrain\\00_Metadata'
MANIFEST = os.path.join(META, 'download_manifest.csv')
DL_CORONAL = os.path.join(META, 'dl_F_coronal.txt')
DL_BATCH = os.path.join(LOGS, 'dl_batch.py')
VERIFY = os.path.join(LOGS, 'verify_downloads.py')
FINAL_REPORT = os.path.join(LOGS, 'final_report.py')

OK_CURL_FILES = ['connectomes_part_1.zip', 'connectomes_part_2.zip',
    'connectomes_part_3.zip', 'connectomes_part_4.zip', 'connectomes_part_5.zip',
    'connectomes_part_6.zip', 'connectomes_part_7.zip', 'connectomes_part_8.zip',
    'connectomes_part_9.zip', 'connectomes_part_10.zip']
CORRUPT_PNGS = ['pm3168o.png', 'pm3177o.png', 'pm3179o.png', 'pm6917o.png']

def read_manifest():
    if not os.path.exists(MANIFEST):
        return [], []
    with open(MANIFEST, encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    fn = list(rows[0].keys()) if rows else []
    return rows, fn

def write_manifest(rows, fn):
    with open(MANIFEST, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=fn)
        w.writeheader()
        w.writerows(rows)

def normalize_ok_curl():
    print('=== Step 1: normalize OK_CURL_CYCLE -> OK ===')
    rows, fn = read_manifest()
    if not rows:
        print('  manifest empty or missing, skip')
        return
    changed = 0
    for r in rows:
        if r['status'] == 'OK_CURL_CYCLE' and r['filename'] in OK_CURL_FILES:
            r['status'] = 'OK'
            changed += 1
    write_manifest(rows, fn)
    print('  normalized %d OK_CURL_CYCLE rows -> OK' % changed)

def purge_corrupt_pngs():
    print('=== Step 2: purge corrupt F coronal PNGs ===')
    rows, fn = read_manifest()
    if not rows:
        print('  manifest empty or missing, skip')
        return
    kept, removed = [], 0
    for r in rows:
        if r['drive'] == 'F' and r['status'].startswith('FAIL_') and r['filename'] in CORRUPT_PNGS:
            dp = r['dest']
            if os.path.exists(dp):
                os.remove(dp)
                print('  removed ' + dp)
            else:
                print('  not on disk: ' + dp)
            removed += 1
            continue
        kept.append(r)
    write_manifest(kept, fn)
    print('  purged %d FAIL manifest rows for corrupt PNGs' % removed)

def dedup_and_add_missing():
    print('=== Step 3: dedup + add missing F coronal files ===')
    rows, fn = read_manifest()
    if not rows:
        print('  manifest empty, skip')
        return
    seen_idx = {}
    for i, r in enumerate(rows):
        seen_idx[(r['drive'], r['dest'])] = i
    deduped = [rows[i] for i in sorted(seen_idx.values())]
    removed = len(rows) - len(deduped)
    if removed:
        print('  removed %d duplicate rows' % removed)
    write_manifest(deduped, fn)
    print('  manifest: %d rows after dedup' % len(deduped))
    planned = {}
    with open(DL_CORONAL, encoding='utf-8') as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln or '|' not in ln:
                continue
            url, dest, size_str = ln.split('|', 2)
            planned[dest] = (url, int(size_str))
    existing = set(r['dest'] for r in deduped if r['drive'] == 'F')
    missing = {d: planned[d] for d in planned if d not in existing}
    print('  still-missing F coronal files: %d' % len(missing))
    if not missing:
        print('  nothing to add')
        return
    with open(MANIFEST, 'a', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        for dest, (url, size) in sorted(missing.items()):
            w.writerow(['', os.path.basename(dest), url, 'F', dest, size, 0, 'MUST_DOWNLOAD', 0])
    print('  added %d MUST_DOWNLOAD rows' % len(missing))


def run_dl_batch():
    print('=== Step 4: download missing F coronal files ===')
    args = [sys.executable, DL_BATCH, DL_CORONAL, 'coronal_repair']
    logfile = os.path.join(LOGS, 'continue_coronal_dl.log')
    with open(logfile, 'a', encoding='utf-8') as fh:
        fh.write('\n===== dl_batch.py coronal_repair =====\n')
        fh.flush()
        rc = subprocess.run(args, stdout=fh, stderr=subprocess.STDOUT).returncode
    print('  dl_batch.py rc=%d' % rc)
    sf = os.path.join(LOGS, 'status_coronal_repair.txt')
    if os.path.exists(sf):
        print('  --- status ---')
        print(open(sf, encoding='utf-8').read())

def run_verify():
    print('=== Step 5: verify all downloaded files ===')
    logfile = os.path.join(LOGS, 'continue_verify.log')
    with open(logfile, 'a', encoding='utf-8') as fh:
        fh.write('\n===== verify_downloads.py =====\n')
        fh.flush()
        rc = subprocess.run([sys.executable, VERIFY], stdout=fh, stderr=subprocess.STDOUT).returncode
    print('  verify_downloads.py rc=%d' % rc)
    vp = os.path.join(META, 'verify_summary.json')
    if os.path.exists(vp):
        print('  --- verify_summary.json ---')
        print(open(vp, encoding='utf-8').read())

def run_final_report():
    print('=== Step 6: generate final report ===')
    logfile = os.path.join(LOGS, 'continue_final.log')
    with open(logfile, 'a', encoding='utf-8') as fh:
        fh.write('\n===== final_report.py =====\n')


def main():
    from datetime import datetime
    print('Starting continuation at ' + datetime.now().isoformat(timespec='seconds'))
    print('Manifest: ' + MANIFEST)
    n_planned = sum(1 for ln in open(DL_CORONAL, encoding='utf-8') if '|' in ln.strip())
    print('Planned F coronal: %d files' % n_planned)
    if os.path.exists(MANIFEST):
        rows, _ = read_manifest()
        f_ok = sum(1 for r in rows if r['drive'] == 'F' and r['status'] == 'OK')
        d_ok = sum(1 for r in rows if r['drive'] == 'D' and r['status'] == 'OK')
        print('Manifest now: F OK=%d, D OK=%d, total=%d' % (f_ok, d_ok, len(rows)))
    print()
    normalize_ok_curl()
    purge_corrupt_pngs()
    dedup_and_add_missing()
    print()
    run_dl_batch()
    print()
    run_verify()
    print()
    run_final_report()
    print()
    print('Done at ' + datetime.now().isoformat(timespec='seconds'))

if __name__ == '__main__':
    main()