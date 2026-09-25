"""Split the remaining coronal downloads across the two BigBrain hosts for parallel fetching.

Both hosts throttle per-IP independently, so a main-host downloader + a mirror downloader
running concurrently gives roughly the sum of the two rates.
Input : dl_F_coronal.txt        (url|dest|bytes, main host)
Output: dl_F_coronal_main.txt   (remaining even slots, main host URLs)
        dl_F_coronal_mirror.txt (remaining odd slots, LORIS mirror URLs)
"""
import os

MD = r'D:\HumanBrain\00_Metadata'
MAIN = os.path.join(MD, 'dl_F_coronal.txt')
OUT_MAIN = os.path.join(MD, 'dl_F_coronal_main.txt')
OUT_MIR = os.path.join(MD, 'dl_F_coronal_mirror.txt')
OLD = 'https://ftp.bigbrainproject.org/bigbrain-ftp/'
NEW = 'https://bigbrain-ftp.loris.ca/bigbrain-ftp/'

rows = []
for ln in open(MAIN, encoding='utf-8'):
    ln = ln.strip()
    if not ln:
        continue
    u, d, s = ln.split('|', 2)
    rows.append((u, d, int(s)))

remaining = [(u, d, s) for u, d, s in rows
             if not (os.path.exists(d) and os.path.getsize(d) == s)]

main_rows, mir_rows = [], []
for i, (u, d, s) in enumerate(remaining):
    if i % 2 == 0:
        main_rows.append((u, d, s))
    else:
        mu = u.replace(OLD, NEW, 1)
        assert mu != u and mu.startswith(NEW), u
        mir_rows.append((mu, d, s))

for path, rs in ((OUT_MAIN, main_rows), (OUT_MIR, mir_rows)):
    with open(path, 'w', encoding='utf-8') as fh:
        for u, d, s in rs:
            fh.write(f'{u}|{d}|{s}\n')

print(f'total={len(rows)} remaining={len(remaining)} '
      f'main_list={len(main_rows)} mirror_list={len(mir_rows)}')
