"""Retry FTP listings for dirs that failed (530 connection limit), 3 workers."""
import ftplib, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r'D:\HumanBrain\99_Logs')
from ftp_dirs import LIST_DIRS

FTP_HOST = 'ftp.bigbrainproject.org'
OUT_LIST = r'F:\HumanBrain\00_Metadata\remote_listings'
OUT_D = r'D:\HumanBrain\00_Metadata'

def ftp_list(path):
    for attempt in range(3):
        out = []
        try:
            with ftplib.FTP(FTP_HOST, timeout=90) as f:
                f.login('anonymous', 'bigbrain@anonymous.org')
                f.cwd(path)
                f.retrlines('LIST', out.append)
            return out
        except Exception as e:
            out.append(f'ERROR: {e}')
            time.sleep(2 + attempt * 3)
    return out

todo = {}
for k, p in LIST_DIRS.items():
    fp = os.path.join(OUT_LIST, k + '.txt')
    if not os.path.exists(fp):
        todo[k] = p
        continue
    txt = open(fp, encoding='utf-8').read()
    if txt.startswith('ERROR') or txt.strip() == '':
        todo[k] = p
print(f'Retrying {len(todo)} failed dirs serially-ish (3 workers)', flush=True)
results = {}
with ThreadPoolExecutor(max_workers=3) as ex:
    futs = {k: ex.submit(ftp_list, p) for k, p in todo.items()}
    for k, fu in futs.items():
        results[k] = fu.result()
        with open(os.path.join(OUT_LIST, k + '.txt'), 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(results[k]))

def parse_ls(lines):
    res = []
    for ln in lines:
        if ln.startswith('ERROR') or len(ln) < 20:
            continue
        parts = ln.split()
        try:
            size = int(parts[4])
        except (IndexError, ValueError):
            size = -1
        name = ' '.join(parts[8:]) if len(parts) > 8 else parts[-1]
        res.append((name, size, ln.startswith('d')))
    return res

# merge into summary
sp = os.path.join(OUT_D, 'remote_listing_summary.json')
summary = json.load(open(sp, encoding='utf-8')) if os.path.exists(sp) else {}
for k in todo:
    entries = parse_ls(results[k])
    files = [(n, s) for n, s, d in entries if not d and s >= 0]
    dirs = [n for n, s, d in entries if d]
    summary[k] = {'n_files': len(files), 'total_bytes': sum(s for _, s in files),
                  'n_dirs': len(dirs), 'dirs': dirs[:20], 'first': files[:2], 'last': files[-2:]}
    print(f"{k}: files={summary[k]['n_files']} bytes={summary[k]['total_bytes']} dirs={summary[k]['dirs'][:6]}", flush=True)
json.dump(summary, open(sp, 'w', encoding='utf-8'), indent=1)
print('RETRY_DONE', flush=True)
