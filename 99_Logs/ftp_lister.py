"""FTP LIST runner: imports LIST_DIRS from ftp_dirs, writes listings + summary."""
import ftplib, json, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r'D:\HumanBrain\99_Logs')
from ftp_dirs import LIST_DIRS

FTP_HOST = 'ftp.bigbrainproject.org'
OUT_LIST = r'F:\HumanBrain\00_Metadata\remote_listings'
OUT_D = r'D:\HumanBrain\00_Metadata'
os.makedirs(OUT_LIST, exist_ok=True)
os.makedirs(OUT_D, exist_ok=True)

def ftp_list(path):
    out = []
    try:
        with ftplib.FTP(FTP_HOST, timeout=90) as f:
            f.login('anonymous', 'bigbrain@anonymous.org')
            f.cwd(path)
            f.retrlines('LIST', out.append)
    except Exception as e:
        out.append(f'ERROR: {e}')
    return out

print('Listing FTP directories...', flush=True)
listings = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = {k: ex.submit(ftp_list, p) for k, p in LIST_DIRS.items()}
    for k, fu in futs.items():
        listings[k] = fu.result()
        with open(os.path.join(OUT_LIST, k + '.txt'), 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(listings[k]))
print(f'Listed {len(listings)} directories', flush=True)

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

summary = {}
for k, lines in listings.items():
    entries = parse_ls(lines)
    files = [(n, s) for n, s, d in entries if not d and s >= 0]
    dirs = [n for n, s, d in entries if d]
    summary[k] = {'n_files': len(files), 'total_bytes': sum(s for _, s in files),
                  'n_dirs': len(dirs), 'dirs': dirs[:20],
                  'first': files[:2], 'last': files[-2:]}
with open(os.path.join(OUT_D, 'remote_listing_summary.json'), 'w', encoding='utf-8') as fh:
    json.dump(summary, fh, indent=1)
for k, v in summary.items():
    print(f"{k}: files={v['n_files']} bytes={v['total_bytes']} dirs={v['n_dirs']} {v['dirs'][:6]}", flush=True)
print('LIST_DONE', flush=True)
