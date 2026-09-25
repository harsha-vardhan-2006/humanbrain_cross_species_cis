"""Byte-equivalence spot check: one already-verified local coronal PNG vs the same file from the LORIS mirror."""
import hashlib, os, requests

LOCAL = r'F:\HumanBrain\01_Histology\2D_Final_Sections\Coronal\Png\Full_Resolution'
MIR = 'https://bigbrain-ftp.loris.ca/bigbrain-ftp/BigBrainRelease.2015/2D_Final_Sections/Coronal/Png/Full_Resolution/'
OUT = r'D:\HumanBrain\99_Logs\mirror_equiv.txt'

f = 'pm0001o.png'
lp = os.path.join(LOCAL, f)
msgs = []
try:
    with open(lp, 'rb') as fh:
        lh = hashlib.sha256(fh.read()).hexdigest()
    r = requests.get(MIR + f, timeout=(30, 600))
    rh = hashlib.sha256(r.content).hexdigest()
    ok = r.status_code == 200 and rh == lh
    msgs.append(f'{f} local_sha={lh[:16]} mirror_sha={rh[:16]} mirror_bytes={len(r.content)} local_bytes={os.path.getsize(lp)} EQUAL={ok}')
except Exception as e:
    msgs.append(f'{f} ERROR {type(e).__name__}: {e}')
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(msgs) + '\n')
print('\n'.join(msgs))
