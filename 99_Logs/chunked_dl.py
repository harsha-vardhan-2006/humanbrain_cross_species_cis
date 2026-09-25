"""Chunked range downloader for full16_100um_optbal.nii.gz (server drops long streams; short 64MB range requests survive)."""
import os, sys, time, requests

URL = 'https://ftp.bigbrainproject.org/bigbrain-ftp/BigBrainRelease.2015/3D_Volumes/Histological_Space/nii/full16_100um_optbal.nii.gz'
TMP = r'D:\HumanBrain\99_Logs\full16_chunks.tmp'
FINAL = r'D:\HumanBrain\01_3D_Volumes\Histological_Space\full16_100um_optbal.nii.gz'
TOTAL = 1444555927
CHUNK = 64 * 1024 * 1024
STATUS = r'D:\HumanBrain\99_Logs\status_full16.txt'
QUAR = r'D:\HumanBrain\99_Logs\QUARANTINE'

def st(msg):
    print(msg, flush=True)
    with open(STATUS, 'a', encoding='utf-8') as fh:
        fh.write(msg + '\n')

def fetch_range(start, end):
    h = {'Range': f'bytes={start}-{end}'}
    last = None
    for i in range(8):
        try:
            r = requests.get(URL, headers=h, timeout=(30, 120))
            if r.status_code == 206 and len(r.content) == end - start + 1:
                return r.content
            last = f'HTTP {r.status_code} len {len(r.content) if r.status_code==206 else "?"}'
        except Exception as e:
            last = type(e).__name__
        time.sleep(10)
    raise RuntimeError(f'chunk {start}-{end} failed after retries: {last}')

pos = os.path.getsize(TMP) if os.path.exists(TMP) else 0
if pos > TOTAL:
    os.remove(TMP); pos = 0
st(f'start pos={pos} total={TOTAL}')
t0 = time.time()
while pos < TOTAL:
    end = min(pos + CHUNK, TOTAL) - 1
    data = fetch_range(pos, end)
    with open(TMP, 'ab') as fh:
        fh.write(data)
    pos = os.path.getsize(TMP)
    rate = (pos) / max(1, time.time() - t0) / 1e6
    st(f'progress {pos}/{TOTAL} ({100*pos/TOTAL:.1f}%) {rate:.2f} MB/s')
if os.path.getsize(TMP) != TOTAL:
    st('FATAL size mismatch'); sys.exit(2)
st('size complete; gzip CRC check')
import gzip
try:
    n = 0
    with gzip.open(TMP, 'rb') as fh:
        while True:
            b = fh.read(1 << 24)
            if not b: break
            n += len(b)
    st(f'gzip CRC OK, uncompressed {n} bytes -> installing')
    os.makedirs(os.path.dirname(FINAL), exist_ok=True)
    os.replace(TMP, FINAL)
    st('OK_CHUNKED full16_100um_optbal.nii.gz installed')
except Exception as e:
    os.makedirs(QUAR, exist_ok=True)
    os.replace(TMP, os.path.join(QUAR, 'full16_100um_optbal.nii.gz.quarantine'))
    st(f'gzip CRC FAILED: {e} -> quarantined')
    sys.exit(3)
