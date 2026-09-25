"""Byte-compare already-verified local coronal PNGs against the LORIS mirror (SHA-256 equivalence test)."""
import hashlib, os, random, requests

LOCAL = r'F:\HumanBrain\01_Histology\2D_Final_Sections\Coronal\Png\Full_Resolution'
MIR = 'https://bigbrain-ftp.loris.ca/bigbrain-ftp/BigBrainRelease.2015/2D_Final_Sections/Coronal/Png/Full_Resolution/'

def sha(b):
    return hashlib.sha256(b).hexdigest()

files = sorted(f for f in os.listdir(LOCAL) if f.endswith('.png'))
random.seed(7)
sample = random.sample(files, 6)
mismatch = 0
for f in sample:
    lp = os.path.join(LOCAL, f)
    with open(lp, 'rb') as fh:
        lh = sha(fh.read())
    try:
        r = requests.get(MIR + f, timeout=(30, 240))
        rh = sha(r.content)
    except Exception as e:
        print(f'{f}: mirror fetch error {type(e).__name__}', flush=True)
        mismatch += 1
        continue
    ok = (r.status_code == 200 and rh == lh and len(r.content) == os.path.getsize(lp))
    print(f'{f}: mirror={len(r.content)}B local={os.path.getsize(lp)}B sha_match={rh == lh} -> {"OK" if ok else "MISMATCH"}', flush=True)
    if not ok:
        mismatch += 1
print(f'RESULT sample={len(sample)} mismatches={mismatch}')
with open(r'D:\HumanBrain\99_Logs\mirror_equiv.txt', 'w', encoding='utf-8') as fh:
    fh.write(f'sample={len(sample)} mismatches={mismatch}\n')
