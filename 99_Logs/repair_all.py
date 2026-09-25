"""Complete-all supervisor: finish every download, then verify, finalize manifests, final report.

- volumes/small: single-host passes (stat-only when already complete)
- coronal: split remaining files across the two BigBrain hosts each attempt, then run the
  main-host and LORIS-mirror downloaders CONCURRENTLY on disjoint file sets
  (the two hosts throttle per-IP independently, so this roughly adds their throughput)
- loops until a pass adds no new failures (max 6 attempts)
- then: verify_downloads -> csm_collect -> csm_finalize -> final_report
"""
import csv, os, subprocess, sys

LOGS = r'D:\HumanBrain\99_Logs'
META = r'D:\HumanBrain\00_Metadata'
BATCH = os.path.join(LOGS, 'dl_batch.py')
SPLIT = os.path.join(LOGS, 'split_coronal.py')
MANIFEST = os.path.join(META, 'download_manifest.csv')
OUT = os.path.join(LOGS, 'repair_all_out.log')
OKS = ('OK', 'SKIP_EXISTS', 'OK_FROM_PART')
MAX_ATTEMPTS = 6


def log(msg):
    with open(OUT, 'a', encoding='utf-8') as fh:
        fh.write(msg + '\n')
    print(msg, flush=True)


def run_sync(script, args, logfile):
    with open(logfile, 'a', encoding='utf-8') as fh:
        fh.write(f'\n===== {script} {args} =====\n')
        fh.flush()
        return subprocess.run([sys.executable, script] + args,
                              stdout=fh, stderr=subprocess.STDOUT).returncode


def run_parallel(pairs):
    """pairs: [(script, args, tag)] -> run concurrently, wait for all."""
    procs = []
    for script, args, tag in pairs:
        fh = open(os.path.join(LOGS, f'par_{tag}.log'), 'a', encoding='utf-8')
        fh.write(f'\n===== {script} {args} =====\n')
        fh.flush()
        procs.append((tag, subprocess.Popen([sys.executable, script] + args,
                                            stdout=fh, stderr=subprocess.STDOUT), fh))
    for tag, p, fh in procs:
        rc = p.wait()
        fh.close()
        log(f'parallel {tag}: rc={rc}')


def count_fails():
    """Count files whose LATEST manifest row is not a success (stale retry rows ignored)."""
    if not os.path.exists(MANIFEST):
        return 0
    latest = {}
    with open(MANIFEST, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            latest[r['dest']] = r['status']
    return sum(1 for st in latest.values() if st not in OKS)


def main():
    for attempt in range(1, MAX_ATTEMPTS + 1):
        log(f'--- attempt {attempt} ---')
        run_sync(BATCH, [os.path.join(META, 'dl_D_volumes.txt'), 'volumes'],
                 os.path.join(LOGS, 'repair_volumes.log'))
        run_sync(BATCH, [os.path.join(META, 'dl_D_small.txt'), 'small'],
                 os.path.join(LOGS, 'repair_small.log'))
        log('splitting remaining coronal files across both hosts')
        run_sync(SPLIT, [], os.path.join(LOGS, 'split_coronal.log'))
        run_parallel([
            (BATCH, [os.path.join(META, 'dl_F_coronal_main.txt'), 'coronal_main'], 'coronal_main'),
            (BATCH, [os.path.join(META, 'dl_F_coronal_mirror.txt'), 'coronal_mirror'], 'coronal_mirror'),
        ])
        fails = count_fails()
        log(f'attempt {attempt} complete: manifest failures={fails}')
        if fails == 0:
            break

    for step in ('verify_downloads.py', 'csm_collect.py', 'csm_finalize.py', 'final_report.py'):
        log(f'final step: {step}')
        run_sync(os.path.join(LOGS, step), [], os.path.join(LOGS, 'final_run.log'))
    log('REPAIR_ALL_DONE')


if __name__ == '__main__':
    main()
