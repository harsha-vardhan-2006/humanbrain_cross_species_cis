"""Build download lists PART 2: surface/label collections + F: coronal PNGs.
Reads small_part1.json, writes dl_D_small.txt, dl_F_coronal.txt, planned_totals.json."""
import json, os, re

RL = r'F:\HumanBrain\00_Metadata\remote_listings'
MD = r'D:\HumanBrain\00_Metadata'
BASE = 'https://ftp.bigbrainproject.org/bigbrain-ftp/'
D = r'D:\HumanBrain'
F = r'F:\HumanBrain'

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

small = [tuple(x) for x in json.load(open(os.path.join(MD, 'small_part1.json')))]

COLL = [('surfaces_gii.txt', '3D_Surfaces/Apr7_2016/gii', rf'{D}\04_Surfaces\Apr7_2016_gii', None),
        ('layer_plos_gii.txt', 'Layer_Segmentation/3D_Surfaces/PLoSBiology2020/gii',
         rf'{D}\06_Layer_Segmentation\PLoSBiology2020_gii', None),
        ('hippo_gii.txt', 'Hippocampus_Segmentation/gii', rf'{D}\07_Hippocampus\gii', None),
        ('parcel_BB_Brainnetome.txt', 'Surface_Parcellations/BigBrain_space/Brainnetome',
         rf'{D}\08_Parcellations\BigBrain_space\Brainnetome', None),
        ('parcel_BB_DKT.txt', 'Surface_Parcellations/BigBrain_space/DKT',
         rf'{D}\08_Parcellations\BigBrain_space\DKT', None),
        ('parcel_BB_Economo.txt', 'Surface_Parcellations/BigBrain_space/Economo',
         rf'{D}\08_Parcellations\BigBrain_space\Economo', None),
        ('parcel_BB_Schaefer2018.txt', 'Surface_Parcellations/BigBrain_space/Schaefer2018',
         rf'{D}\08_Parcellations\BigBrain_space\Schaefer2018', None),
        ('parcel_BB_HCPMMP.txt', 'Surface_Parcellations/BigBrain_space/HCP-MMP-1.0',
         rf'{D}\08_Parcellations\BigBrain_space\HCP-MMP-1.0', None),
        ('parcel_BB_Surfaces.txt', 'Surface_Parcellations/BigBrain_space/Surfaces',
         rf'{D}\08_Parcellations\BigBrain_space\Surfaces', ('.obj',)),
        ('warp_white_surfaces.txt', 'BigBrainWarp_Support/white_surfaces',
         rf'{D}\09_BigBrainWarp\white_surfaces', None),
        ('warp_mni152_spheres.txt', 'BigBrainWarp_Support/BigBrain_to_MNI152/spheres',
         rf'{D}\09_BigBrainWarp\spheres\MNI152', None),
        ('warp_fsLR_spheres.txt', 'BigBrainWarp_Support/BigBrain_to_fsLR/spheres',
         rf'{D}\09_BigBrainWarp\spheres\fsLR', None),
        ('warp_mni152_in_input.txt', 'BigBrainWarp_Support/BigBrain_to_MNI152/inmap_BigBrain_outmap_MNI152/input',
         rf'{D}\09_BigBrainWarp\maps\BigBrain_to_MNI152\input', None),
        ('warp_mni152_in_output.txt', 'BigBrainWarp_Support/BigBrain_to_MNI152/inmap_BigBrain_outmap_MNI152/output',
         rf'{D}\09_BigBrainWarp\maps\BigBrain_to_MNI152\output', None),
        ('warp_mni152_rev_input.txt', 'BigBrainWarp_Support/BigBrain_to_MNI152/inmap_MNI152_outmap_BigBrain/input',
         rf'{D}\09_BigBrainWarp\maps\MNI152_to_BigBrain\input', None),
        ('warp_mni152_rev_output.txt', 'BigBrainWarp_Support/BigBrain_to_MNI152/inmap_MNI152_outmap_BigBrain/output',
         rf'{D}\09_BigBrainWarp\maps\MNI152_to_BigBrain\output', None)]
for fn, rel, dest, excl in COLL:
    for n, sz in read_sizes(fn).items():
        if excl and n.endswith(tuple(excl)):
            continue
        small.append((BASE + 'BigBrainRelease.2015/' + rel + '/' + n, dest + '\\' + n, sz))

coronal = [(BASE + 'BigBrainRelease.2015/2D_Final_Sections/Coronal/Png/Full_Resolution/' + n,
            rf'{F}\01_Histology\2D_Final_Sections\Coronal\Png\Full_Resolution\{n}', sz)
           for n, sz in read_sizes('2d_coronal_png_full.txt').items()]

def w(fn, rows):
    with open(os.path.join(MD, fn), 'w', encoding='utf-8') as fh:
        for u, d_, s in rows:
            fh.write(f'{u}|{d_}|{s}\n')

w('dl_D_small.txt', small)
w('dl_F_coronal.txt', coronal)
print('small_final:', len(small), sum(s for _, _, s in small) / 1e9, 'GB')
print('coronal:', len(coronal), sum(s for _, _, s in coronal) / 1e9, 'GB')
print('PART2_DONE')
