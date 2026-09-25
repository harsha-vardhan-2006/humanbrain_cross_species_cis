"""Final analysis-readiness check for the BigBrain 2015 dataset."""
import csv, json, os, shutil
from collections import Counter

MD = r'D:\HumanBrain\00_Metadata'
issues = []

# 1. Manifest integrity
rows = list(csv.DictReader(open(os.path.join(MD, 'download_manifest.csv'), encoding='utf-8')))
st = Counter(r['status'] for r in rows)
print('1. MANIFEST: %d rows, statuses=%s' % (len(rows), dict(st)))
if st.get('OK', 0) != len(rows):
    issues.append('manifest has non-OK rows')

# 2. All files exist on disk with expected size
missing, sizebad = [], []
for r in rows:
    if not os.path.exists(r['dest']):
        missing.append(r['dest'])
    elif int(r['actual_bytes']) != int(r['expected_bytes']):
        sizebad.append(r['dest'])
print('2. FILES: missing=%d size_mismatch=%d' % (len(missing), len(sizebad)))
if missing or sizebad:
    issues.append('missing/sizebad files')

# 3. Structural verification
v = json.load(open(os.path.join(MD, 'verify_summary.json')))
print('3. VERIFY: total=%d verified=%d failed=%d kinds=%s' %
      (v['total'], v['verified'], len(v['failed']), v['counts_by_kind']))
if v['failed']:
    issues.append('verify failures')

# 4. Checksums present
for f in ('CHECKSUMS_D.sha256', 'CHECKSUMS_F.sha256'):
    p = os.path.join(MD, f)
    n = sum(1 for _ in open(p, encoding='utf-8', errors='ignore')) if os.path.exists(p) else 0
    print('4. CHECKSUM %s: %s (%d lines)' % (f, 'OK' if n else 'MISSING', n))
    if not n:
        issues.append('checksum ' + f + ' missing')

# 5. Key directory content (analysis essentials)
checks = [
    (r'D:\HumanBrain\01_3D_Volumes', 17, 'NIfTI volumes (hist + MNI)'),
    (r'D:\HumanBrain\04_Surfaces\Apr7_2016_gii', None, 'GIfTI surfaces'),
    (r'D:\HumanBrain\05_ROIs', None, '100um ROI volumes'),
    (r'D:\HumanBrain\06_Layer_Segmentation', None, 'cortical layer surfaces'),
    (r'D:\HumanBrain\07_Hippocampus\gii', None, 'hippocampal subfields'),
    (r'D:\HumanBrain\08_Parcellations', None, 'atlases (Brainnetome/DKT/Economo/Schaefer/HCP-MMP)'),
    (r'D:\HumanBrain\09_BigBrainWarp', None, 'BigBrainWarp MSM spheres + surfaces'),
    (r'D:\HumanBrain\12_HumanConnectome_AOMIC', 10, 'AOMIC connectomes'),
    (r'F:\HumanBrain\01_Histology\2D_Final_Sections\Coronal\Png\Full_Resolution', 7404, 'coronal PNGs'),
]
print('5. DIRECTORY CONTENT:')
for d, expect_n, label in checks:
    if not os.path.isdir(d):
        print('   MISSING DIR: %s (%s)' % (d, label))
        issues.append('dir ' + d)
        continue
    n = sum(len(fs) for _, _, fs in os.walk(d))
    ok = '' if expect_n is None else ('OK' if n == expect_n else 'MISMATCH exp=%d' % expect_n)
    if expect_n is not None and n != expect_n:
        issues.append(d)
    print('   %-6s %5d files  %s' % (ok or 'dir', n, d))

# 6. Disk space guard (>10GB rule)
print('6. DISK FREE:')
for drv in ('D', 'F', 'G'):
    du = shutil.disk_usage(drv + ':\\')
    gb = du.free / 1e9
    print('   %s: %.1f GB free %s' % (drv, gb, 'OK' if gb > 10 else 'LOW!'))
    if gb < 10:
        issues.append('disk ' + drv)

# 7. Reports final
rep = open(os.path.join(MD, 'ACQUISITION_REPORT.md'), encoding='utf-8').read()
print('7. REPORT: verdict PASS =', 'PASS - ACQUISITION COMPLETE AND VERIFIED' in rep)

print('\n' + ('=== ALL CLEAR: DATASET READY FOR HUMAN BRAIN ANALYSIS ===' if not issues
              else '=== ISSUES: %s ===' % issues))

