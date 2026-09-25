"""Hash the verified full16 volume, then remove the superseded corrupt quarantine copy."""
import gzip, hashlib, os

GOOD = r'D:\HumanBrain\01_3D_Volumes\Histological_Space\full16_100um_optbal.nii.gz'
QUAR = r'D:\HumanBrain\99_Logs\QUARANTINE'
OUT = r'D:\HumanBrain\99_Logs\full16_final.txt'

lines = []
sz = os.path.getsize(GOOD)
lines.append(f'good_copy={GOOD}')
lines.append(f'bytes={sz} (expected 1444555927) size_ok={sz == 1444555927}')
n = 0
with gzip.open(GOOD, 'rb') as fh:
    while True:
        b = fh.read(1 << 24)
        if not b:
            break
        n += len(b)
lines.append(f'gzip_CRC_OK uncompressed={n}')
h = hashlib.sha256()
with open(GOOD, 'rb') as fh:
    for c in iter(lambda: fh.read(1 << 20), b''):
        h.update(c)
lines.append(f'sha256={h.hexdigest()}')

qs = os.path.join(QUAR, 'full16_100um_optbal.nii.gz.quarantine')
if os.path.exists(qs):
    os.remove(qs)
    lines.append(f'removed superseded quarantine: {qs} (gzip-CRC-invalid seed bytes; good copy re-downloaded and verified)')

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines) + '\n')
print('\n'.join(lines))
