"""Read-only HTTPS size probe (HTTP Range 0-0) for curated BigBrain 2015 URLs.
Writes D:\\HumanBrain\\00_Metadata\\http_sizes.tsv (bytes TAB url).
"""
import os
from concurrent.futures import ThreadPoolExecutor
import requests

BASE = 'https://ftp.bigbrainproject.org/bigbrain-ftp/BigBrainRelease.2015/'
OUT = r'D:\HumanBrain\00_Metadata\http_sizes.tsv'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

probe_rel = []
for r_ in ('100um', '200um', '300um', '400um', '1000um'):
    probe_rel.append(f'3D_Volumes/Histological_Space/nii/full16_{r_}_optbal.nii.gz')
for r_ in ('200um', '300um', '400um'):
    probe_rel.append(f'3D_Volumes/MNI-ICBM152_Space/nii/full8_{r_}_2009b_sym.nii.gz')
    probe_rel.append(f'3D_Volumes/MNI-ICBM152_Space/nii/full16_{r_}_2009b_sym.nii.gz')
    probe_rel.append(f'3D_Volumes/MNI-ADNI_Space/nii/full8_{r_}_adni.nii.gz')
    probe_rel.append(f'3D_Volumes/MNI-ADNI_Space/nii/full16_{r_}_adni.nii.gz')
for n in ('full_cls_100um.nii.gz', 'full_cls_200um.nii.gz', 'full_cls_200um_9classes.nii.gz',
          'full_cls_200um_mask.nii.gz', 'full_cls_300um.nii.gz', 'full_cls_400um.nii.gz',
          'full_cls_1000um.nii.gz', 'hemispheres_mask_100um.nii.gz', 'hemispheres_mask_200um.nii.gz',
          'hemispheres_mask_300um.nii.gz', 'hemispheres_mask_400um.nii.gz', 'hemispheres_mask_1000um.nii.gz'):
    probe_rel.append('3D_Classified_Volumes/Histological_Space/nii/' + n)
for r_ in ('200um', '300um', '400um'):
    probe_rel.append(f'3D_Classified_Volumes/MNI-ICBM152_Space/nii/full_cls_{r_}_2009b_sym.nii.gz')
probe_rel.append('3D_MRI/nii/mri_to_blk_aligned.nii.gz')
ROI = [
    ('3D_ROIs/Occipital/nii', ['occipital_left_100um.nii.gz', 'occipital_right_100um.nii.gz',
                               'occipital_left_40um.nii.gz', 'occipital_right_40um.nii.gz']),
    ('3D_ROIs/Heschl/nii', ['heschl_right_100um.nii.gz', 'heschl_right_40um.nii.gz']),
    ('3D_ROIs/Central/nii', ['central_left_100um.nii.gz', 'central_left_40um.nii.gz']),
    ('3D_ROIs/BA10/nii', ['BA10_right_100um.nii.gz', 'BA10_right_40um.nii.gz']),
    ('3D_ROIs/Hippocampus/nii', ['hippocampus_left_100um.nii.gz', 'hippocampus_right_100um.nii.gz',
                                 'hippocampus_left_40um.nii.gz', 'hippocampus_right_40um.nii.gz']),
    ('3D_ROIs/Hypothalamus/nii', ['hypothalamus_full_100um.nii.gz', 'hypothalamus_full_40um.nii.gz']),
    ('3D_ROIs/Cerebellum/nii', ['cerebellum_full_100um.nii.gz']),
]
for d, names in ROI:
    for n in names:
        probe_rel.append(f'{d}/{n}')

def probe(rel):
    try:
        r = requests.get(BASE + rel, headers={'Range': 'bytes=0-0'}, timeout=30, stream=True)
        if r.status_code == 206:
            cr = r.headers.get('Content-Range', '')
            size = int(cr.split('/')[-1]) if '/' in cr else -1
        elif r.status_code == 200:
            size = int(r.headers.get('Content-Length', -1))
        else:
            size = -r.status_code
        r.close()
        return rel, size
    except Exception:
        return rel, -999

sizes = {}
with ThreadPoolExecutor(max_workers=12) as ex:
    for rel, size in ex.map(probe, probe_rel):
        sizes[rel] = size
with open(OUT, 'w', encoding='utf-8') as fh:
    for k in sorted(sizes):
        fh.write(f'{sizes[k]}\t{BASE}{k}\n')
bad = {k: v for k, v in sizes.items() if v <= 0}
tot = sum(v for v in sizes.values() if v > 0)
print(f'probed={len(sizes)} total={tot/1e9:.2f}GB bad={bad if bad else "none"}')
print('PROBE_DONE')
