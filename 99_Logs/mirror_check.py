"""Verify the LORIS mirror serves byte-identical files: compare mirror listing sizes with local verified sizes."""
import os, re, requests

MIR = 'https://bigbrain-ftp.loris.ca/bigbrain-ftp/BigBrainRelease.2015/2D_Final_Sections/Coronal/Png/Full_Resolution/'
LOCAL = r'F:\HumanBrain\01_Histology\2D_Final_Sections\Coronal\Png\Full_Resolution'

r = requests.get(MIR, timeout=(30, 300))
print('mirror listing status', r.status_code, 'bytes', len(r.content), flush=True)
sizes = {}
for line in r.text.splitlines():
    m = re.match(r'^\S+\s+\d+\s+\S+\s+\S+\s+(\d+)\s+\S+\s+\S+\s+(pm\d{4}o\.png)$', line.strip())
    if m:
        sizes[m.group(2)] = int(m.group(1))
print('mirror files parsed:', len(sizes), flush=True)

local = {}
for f in os.listdir(LOCAL):
    if f.endswith('.png'):
        local[f] = os.path.getsize(os.path.join(LOCAL, f))
print('local pngs:', len(local), flush=True)

common = set(sizes) & set(local)
same = [n for n in common if sizes[n] == local[n]]
diff = [n for n in common if sizes[n] != local[n]]
print(f'common={len(common)} same_size={len(same)} diff={len(diff)}')
if diff:
    for n in diff[:10]:
        print('  DIFF', n, 'mirror', sizes[n], 'local', local[n])
only_mir = [n for n in sizes if n not in local]
print('mirror-only (not yet local):', len(only_mir))
missing_on_mirror = [n for n in local if n not in sizes]
print('local-but-not-on-mirror:', len(missing_on_mirror))
with open(r'D:\HumanBrain\99_Logs\mirror_check.txt', 'w', encoding='utf-8') as fh:
    fh.write(f'mirror_files={len(sizes)} local={len(local)} common={len(common)} same={len(same)} diff={len(diff)} mirror_only={len(only_mir)} local_not_mirror={len(missing_on_mirror)}\n')
