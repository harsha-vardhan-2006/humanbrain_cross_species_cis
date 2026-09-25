"""Coordinator for a cyclic-curl download (one file at a time, cycle N is for process-safety).

Launch ONE file via: py curl_cycle.py <listfile> <tag>
The coordinator checks for an existing .lock; if present it exits (a worker is running).
Otherwise it picks the next incomplete entry, writes <dest>.next, and starts itself as
a detached worker for that single file.

Worker: fresh curl each cycle, run capped at CYCLE_CAP seconds; the coordinator is
re-run by the caller to continue the loop. Re-runs are cheap for the supervisor.

Actually simplest robust pattern: run ONE detached worker that loops internally with
a cycle cap per restart. This script is that worker: it cycles ALL incomplete files,
one at a time, restarting curl every CYCLE seconds, until all are complete.
"""
import csv, datetime, os, subprocess, sys, time

LIST_FILE = sys.argv[1]
TAG = sys.argv[2]
CYCLE = int(sys.argv[3]) if len(sys.argv) > 3 else 150
MANIFEST = r'D:\HumanBrain\00_Metadata\download_manifest.csv'
STATUS = rf'D:\HumanBrain\99_Logs\status_{TAG}.txt'
LOCK = rf'D:\HumanBrain\99_Logs\curl_cycle_{TAG}.lock'
MIN_FREE = 15 * 1024 ** 3


def st(msg):
    print(msg, flush=True)
    with open(STATUS, 'w', encoding='utf-8') as fh:
        fh.write(msg + '\n')


def log_mani(dest, url, exp, act, status, secs):
    drive = os.path.splitdrive(dest)[0][0]
    with open(MANIFEST, 'a', newline='', encoding='utf-8') as fh:
        csv.writer(fh).writerow([datetime.datetime.now().isoformat(timespec='seconds'),
                                 os.path.basename(dest), url, drive, dest, exp, act, status,
                                 round(secs, 1)])


def main():
    if os.path.exists(LOCK):
        print(f'{TAG}: another cycle worker already holds the lock; exiting', flush=True)
        return 0
    open(LOCK, 'w').write(str(os.getpid()))
    t_start = time.time()
    try:
        while True:
            done_all = True
            for ln in open(LIST_FILE, encoding='utf-8'):
                ln = ln.strip()
                if not ln:
                    continue
                u, d, exp = ln.split('|', 2)
                exp = int(exp)
                os.makedirs(os.path.dirname(d), exist_ok=True)
                if os.path.exists(d) and os.path.getsize(d) == exp:
                    continue
                done_all = False
                part = d + '.part'
                t0 = time.time()
                got_before = os.path.getsize(part) if os.path.exists(part) else 0
                try:
                    subprocess.run(['curl.exe', '-sS', '-L', '-C', '-', '--max-time',
                                    str(CYCLE), '-o', part, u],
                                   capture_output=True, timeout=CYCLE + 30)
                except Exception:
                    pass
                got_after = os.path.getsize(part) if os.path.exists(part) else 0
                rate = (got_after - got_before) / max(1, time.time() - t0) / 1e3
                if got_after == exp:
                    os.replace(part, d)
                    log_mani(d, u, exp, got_after, 'OK_CURL_CYCLE', time.time() - t0)
                    st(f'{TAG} OK {os.path.basename(d)} ({got_after/1e9:.2f} GB)')
                elif got_after > got_before:
                    st(f'{TAG} {os.path.basename(d)}: {got_after/1e6:.0f}/{exp/1e6:.0f} MB '
                       f'(+{rate:.0f} KB/s this cycle) elapsed={time.time()-t_start:.0f}s')
                else:
                    st(f'{TAG} {os.path.basename(d)}: {got_after/1e6:.0f}/{exp/1e6:.0f} MB '
                       f'(stalled this cycle) elapsed={time.time()-t_start:.0f}s')
            if done_all:
                st(f'{TAG} ALL COMPLETE elapsed={time.time()-t_start:.0f}s')
                return 0
            # loop again; if MANIFEST free-space guard trips, keep cycling (safe)
    finally:
        if os.path.exists(LOCK):
            os.remove(LOCK)

    return 0


if __name__ == '__main__':
    sys.exit(main())
