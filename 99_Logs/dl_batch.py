"""Threaded batch downloader for url|dest|bytes list files.
Usage: py dl_batch.py <listfile> <tag>
- skips complete files, resumes via Range when .part exists and server allows
- size-verify each file; mismatch -> *_QUARANTINE (never deleted)
- appends to download_manifest.csv, prints progress every N files
"""
import csv, datetime, os, sys, threading, time
import requests

LIST_FILE, TAG = sys.argv[1], sys.argv[2]
MANIFEST = r'D:\HumanBrain\00_Metadata\download_manifest.csv'
STATUS = rf'D:\HumanBrain\99_Logs\status_{TAG}.txt'
QUAR = {r'D': r'D:\HumanBrain\99_Logs\QUARANTINE', r'F': r'F:\HumanBrain\99_Logs\QUARANTINE'}
MIN_FREE = 15 * 1024**3

rows = []
for ln in open(LIST_FILE, encoding='utf-8'):
    ln = ln.strip()
    if not ln:
        continue
    u, d, s = ln.split('|', 2)
    rows.append((u, d, int(s)))

import threading
_tl = threading.local()
lock = threading.Lock()
mani_lock = threading.Lock()
if not os.path.exists(MANIFEST):
    with open(MANIFEST, 'w', newline='', encoding='utf-8') as fh:
        csv.writer(fh).writerow(['timestamp', 'filename', 'url', 'drive', 'dest',
                                 'expected_bytes', 'actual_bytes', 'status', 'seconds'])
count = {'done': 0, 'skip': 0, 'fail': 0, 'quar': 0, 'bytes': 0}
t_start = time.time()

def log_mani(dest, url, exp, act, status, secs):
    drive = os.path.splitdrive(dest)[0][0]
    with mani_lock:
        with open(MANIFEST, 'a', newline='', encoding='utf-8') as fh:
            csv.writer(fh).writerow([datetime.datetime.now().isoformat(timespec='seconds'),
                                     os.path.basename(dest), url, drive, dest, exp, act, status,
                                     round(secs, 1)])

def get_free(drive):
    import shutil
    try:
        return shutil.disk_usage(drive + ':\\').free
    except Exception:
        return MIN_FREE

def worker(u, d, exp):
    drive = os.path.splitdrive(d)[0][0]
    if get_free(drive) < MIN_FREE:
        with lock:
            count['fail'] += 1
        log_mani(d, u, exp, 0, 'STOP_DISK_LOW', 0)
        return
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if os.path.exists(d) and os.path.getsize(d) == exp:
        with lock:
            count['skip'] += 1
        log_mani(d, u, exp, exp, 'SKIP_EXISTS', 0)
        return
    tmp = d + '.part'
    headers = {}
    mode = 'wb'
    if os.path.exists(tmp):
        psz = os.path.getsize(tmp)
        if psz == exp:
            os.replace(tmp, d)
            with lock:
                count['done'] += 1
                count['bytes'] += exp
            log_mani(d, u, exp, exp, 'OK_FROM_PART', 0)
            return
        if 0 < psz < exp:
            headers['Range'] = f'bytes={psz}-'
            mode = 'ab'
    sess = getattr(_tl, 'sess', None)
    if sess is None:
        sess = requests.Session()
        _tl.sess = sess
    t0 = time.time()
    try:
        with sess.get(u, headers=headers, stream=True, timeout=(30, 180)) as r:
            if r.status_code not in (200, 206):
                with lock:
                    count['fail'] += 1
                log_mani(d, u, exp, 0, f'HTTP_{r.status_code}', 0)
                return
            with open(tmp, mode) as f:
                for chunk in r.iter_content(1024 * 256):
                    f.write(chunk)
        act = os.path.getsize(tmp)
        if act != exp:
            qd = QUAR.get(drive)
            os.makedirs(qd, exist_ok=True)
            os.replace(tmp, os.path.join(qd, os.path.basename(d) + '.quarantine'))
            with lock:
                count['quar'] += 1
            log_mani(d, u, exp, act, 'SIZE_MISMATCH_QUARANTINED', time.time() - t0)
            return
        os.replace(tmp, d)
        with lock:
            count['done'] += 1
            count['bytes'] += act
        log_mani(d, u, exp, act, 'OK', time.time() - t0)
    except Exception as e:
        with lock:
            count['fail'] += 1
        log_mani(d, u, exp, 0, f'FAIL_{type(e).__name__}', time.time() - t0)

todo = [(u, d, exp) for u, d, exp in rows
        if not (os.path.exists(d) and os.path.getsize(d) == exp)]
from concurrent.futures import ThreadPoolExecutor
# optional argv[3] = explicit worker count (CDN sources such as Zenodo scale with connections)
NTHREADS = int(sys.argv[3]) if len(sys.argv) > 3 else (4 if len(rows) > 100 else 2)
with ThreadPoolExecutor(max_workers=NTHREADS) as ex:
    futs = [ex.submit(worker, u, d, exp) for u, d, exp in todo]
    done_n = 0
    for fu in futs:
        fu.result()
        done_n += 1
        if done_n % 50 == 0 or done_n == len(futs):
            with lock:
                msg = (f"{TAG}: {done_n}/{len(futs)} processed | ok={count['done']} "
                       f"skip={count['skip']} fail={count['fail']} quar={count['quar']} "
                       f"bytes={count['bytes']/1e9:.2f}GB elapsed={time.time()-t_start:.0f}s")
            print(msg, flush=True)
            with open(STATUS, 'w', encoding='utf-8') as fh:
                fh.write(msg + '\n')

final = (f"{TAG} FINAL: ok={count['done']} skip={count['skip']} fail={count['fail']} "
         f"quar={count['quar']} bytes={count['bytes']/1e9:.2f}GB "
         f"elapsed={time.time()-t_start:.0f}s")
print(final, flush=True)
with open(STATUS, 'w', encoding='utf-8') as fh:
    fh.write(final + '\n')
