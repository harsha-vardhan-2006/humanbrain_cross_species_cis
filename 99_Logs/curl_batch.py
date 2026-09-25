"""curl-driven parallel downloader with resume.

Used for CDN sources (e.g. Zenodo) where python-requests connections get stalled,
while curl sustains throughput.

Usage: py curl_batch.py <listfile> <tag> [nparallel]
List format: url|dest|bytes

Behaviour (mirrors dl_batch.py guarantees):
- skips files already present at the exact expected size
- downloads into <dest>.part with `curl -C -` (resumes on re-run)
- size-verifies before renaming .part -> dest; mismatch keeps .part and logs a FAIL row
- appends every outcome to download_manifest.csv
- stops a worker (STOP_DISK_LOW) if its drive drops below the 15 GB reserve
"""
import csv, datetime, os, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

LIST_FILE, TAG = sys.argv[1], sys.argv[2]
NPAR = int(sys.argv[3]) if len(sys.argv) > 3 else 6
MANIFEST = r'D:\HumanBrain\00_Metadata\download_manifest.csv'
STATUS = rf'D:\HumanBrain\99_Logs\status_{TAG}.txt'
MIN_FREE = 15 * 1024 ** 3
CURL = 'curl.exe'

rows = []
for ln in open(LIST_FILE, encoding='utf-8'):
    ln = ln.strip()
    if not ln:
        continue
    u, d, s = ln.split('|', 2)
    rows.append((u, d, int(s)))

lock = threading.Lock()
count = {'done': 0, 'skip': 0, 'fail': 0, 'bytes': 0}
t_start = time.time()


def log_mani(dest, url, exp, act, status, secs):
    drive = os.path.splitdrive(dest)[0][0]
    with lock:
        with open(MANIFEST, 'a', newline='', encoding='utf-8') as fh:
            csv.writer(fh).writerow([datetime.datetime.now().isoformat(timespec='seconds'),
                                     os.path.basename(dest), url, drive, dest, exp, act, status,
                                     round(secs, 1)])


def worker(u, d, exp):
    drive = os.path.splitdrive(d)[0][0]
    try:
        free = shutil.disk_usage(drive + ':\\').free
    except Exception:
        free = MIN_FREE
    if free < MIN_FREE:
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
    part = d + '.part'
    t0 = time.time()
    last = None
    for _ in range(4):
        cmd = [CURL, '-sS', '-L', '--retry', '5', '--retry-delay', '2',
               '--retry-all-errors', '-C', '-', '-o', part, u]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
            if r.returncode != 0:
                last = (r.stderr or '').strip()[:120]
        except Exception as e:
            last = f'{type(e).__name__}'
        if os.path.exists(part) and os.path.getsize(part) == exp:
            break
        time.sleep(4)
    act = os.path.getsize(part) if os.path.exists(part) else 0
    if act == exp:
        os.replace(part, d)
        with lock:
            count['done'] += 1
            count['bytes'] += act
        log_mani(d, u, exp, act, 'OK', time.time() - t0)
        print(f'OK   {os.path.basename(d)} {act} bytes in {time.time()-t0:.0f}s', flush=True)
    else:
        with lock:
            count['fail'] += 1
        log_mani(d, u, exp, act, f'FAIL_CURL_PARTIAL:{last}', time.time() - t0)
        print(f'FAIL {os.path.basename(d)} got {act}/{exp} {last}', flush=True)


todo = [(u, d, exp) for u, d, exp in rows
        if not (os.path.exists(d) and os.path.getsize(d) == exp)]
print(f'{TAG}: {len(todo)} to fetch of {len(rows)} planned, {NPAR} parallel curl workers', flush=True)

with ThreadPoolExecutor(max_workers=NPAR) as ex:
    futs = [ex.submit(worker, u, d, exp) for u, d, exp in todo]
    done_n = 0
    for fu in futs:
        fu.result()
        done_n += 1
        with lock:
            msg = (f"{TAG}: {done_n}/{len(futs)} | ok={count['done']} skip={count['skip']} "
                   f"fail={count['fail']} bytes={count['bytes']/1e9:.2f}GB "
                   f"elapsed={time.time()-t_start:.0f}s")
        print(msg, flush=True)
        with open(STATUS, 'w', encoding='utf-8') as fh:
            fh.write(msg + '\n')

final = (f"{TAG} FINAL: ok={count['done']} skip={count['skip']} fail={count['fail']} "
         f"bytes={count['bytes']/1e9:.2f}GB elapsed={time.time()-t_start:.0f}s")
print(final, flush=True)
with open(STATUS, 'w', encoding='utf-8') as fh:
    fh.write(final + '\n')
