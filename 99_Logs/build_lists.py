"""Build download lists PART 1: big volumes + classified + ROIs.
Writes dl_D_volumes.txt and small_part1.json (rows [url,dest,bytes])."""
import json, os, re

RL = r'F:\HumanBrain\00_Metadata\remote_listings'
MD = r'D:\HumanBrain\00_Metadata'
BASE = 'https://ftp.bigbrainproject.org/bigbrain-ftp/'
D = r'D:\HumanBrain'

def read_sizes(fn):
    out = {}
    p = os.path.join(RL, fn)
    if not os.path.exists(p):
        return out
    for ln in open(p, encoding='utf-8', errors='replace'):
        m = re.match(r'^[-d][rwx-]{9}\s+\d+\s+\S+\s+\S+\s+(\d+)\s+\w+\s+\d+\s+[\d:]+\s+(.+)$', ln.strip())
        if m and not ln.startswith('d'):
            out[m.group(2)] = int(m.group(1))
    return out

vols = {}
for ln in open(os.path.join(MD, 'http_sizes.tsv'), encoding='utf-8'):
    sz, url = ln.rstrip('\n').split('\t')
    vols[url.replace(BASE + 'BigBrainRelease.2015/', '')] = int(sz)

volumes, small = [], []

def add_v(rel, dest):
    sz = vols.get(rel, -1)
    if sz > 0:
        volumes.append((BASE + 'BigBrainRelease.2015/' + rel, dest, sz))

def add_s(rel, dest):
    sz = vols.get(rel, -1)
    if sz > 0:
        small.append((BASE + 'BigBrainRelease.2015/' + rel, dest, sz))

for r_ in ('100um', '200um', '300um', '400um', '1000um'):
    add_v(f'3D_Volumes/Histological_Space/nii/full16_{r_}_optbal.nii.gz',
          rf'{D}\01_3D_Volumes\Histological_Space\full16_{r_}_optbal.nii.gz')
for sp, tag in (('MNI-ICBM152_Space', '2009b_sym'), ('MNI-ADNI_Space', 'adni')):
    for r_ in ('200um', '300um', '400um'):
        for st in ('full8', 'full16'):
            add_v(f'3D_Volumes/{sp}/nii/{st}_{r_}_{tag}.nii.gz',
                  rf'{D}\01_3D_Volumes\{sp}\{st}_{r_}_{tag}.nii.gz')
add_v('3D_MRI/nii/mri_to_blk_aligned.nii.gz', rf'{D}\03_MRI\mri_to_blk_aligned.nii.gz')

CLS = read_sizes('cls_hist_nii.txt')
for n, sz in CLS.items():
    small.append((BASE + 'BigBrainRelease.2015/3D_Classified_Volumes/Histological_Space/nii/' + n,
                  rf'{D}\02_Classified_Volumes\Histological_Space\{n}', sz))
for r_ in ('200um', '300um', '400um'):
    add_s(f'3D_Classified_Volumes/MNI-ICBM152_Space/nii/full_cls_{r_}_2009b_sym.nii.gz',
          rf'{D}\02_Classified_Volumes\MNI-ICBM152_Space\full_cls_{r_}_2009b_sym.nii.gz')

ROI_DIRS = {'Occipital': ['occipital_left_100um.nii.gz', 'occipital_right_100um.nii.gz'],
            'Heschl': ['Heschl_right_100um.nii.gz'],
            'Central': ['central_left_100um.nii.gz'],
            'BA10': ['BA10_right_100um.nii.gz'],
            'Hippocampus': ['hippocampus_left_100um.nii.gz', 'hippocampus_right_100um.nii.gz'],
            'Hypothalamus': ['hypothalamus_full_100um.nii.gz'],
            'Cerebellum': ['cerebellum_full_100um.nii.gz']}
for reg, names in ROI_DIRS.items():
    lst = read_sizes(f'roi_{reg.lower()}.txt')
    for n in names:
        if n in lst:
            small.append((BASE + f'BigBrainRelease.2015/3D_ROIs/{reg}/nii/' + n,
                          rf'{D}\05_ROIs\{reg}\{n}', lst[n]))

with open(os.path.join(MD, 'dl_D_volumes.txt'), 'w', encoding='utf-8') as fh:
    for u, d_, s in volumes:
        fh.write(f'{u}|{d_}|{s}\n')
json.dump(small, open(os.path.join(MD, 'small_part1.json'), 'w'))
print('volumes:', len(volumes), sum(s for _, _, s in volumes) / 1e9, 'GB')
print('small_p1:', len(small), sum(s for _, _, s in small) / 1e9, 'GB')
print('PART1_DONE')
