"""Find the 18th NIfTI in the manifest (outside 01_3D_Volumes)."""
import csv, os

MD = r'D:\HumanBrain\00_Metadata'
rows = list(csv.DictReader(open(os.path.join(MD, 'download_manifest.csv'), encoding='utf-8')))
nii = [r for r in rows if r['dest'].lower().endswith(('.nii', '.nii.gz')) and r['dest'].startswith('D:\\')]
print('NIfTI rows on D: %d' % len(nii))
for r in nii:
    if '01_3d_volumes' not in r['dest'].lower():
        print('  %10s  %s  [%s]' % (r['actual_bytes'], r['dest'], r['status']))
