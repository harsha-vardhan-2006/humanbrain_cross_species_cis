"""Post-download verification + checksum generation.
- .nii.gz: full gzip CRC-decompress check + nibabel header read (dims, zooms, dtype)
- .gii / .label.gii: nibabel open (dimension check)
- .png: PNG signature + IEND trailer check
- .annot/.txt/.json/.label/.mgz/.obj: size presence check only (annot/obj not nibabel formats)
- SHA-256 for every verified file -> CHECKSUMS.sha256 per drive
Outputs: D:\\HumanBrain\\00_Metadata\\verify_summary.json
Reads download_manifest.csv (OK / SKIP_EXISTS / OK_FROM_PART rows).
"""
import csv, gzip, hashlib, json, os, struct, sys
import nibabel as nib

MD = r'D:\HumanBrain\00_Metadata'
MANIFEST = os.path.join(MD, 'download_manifest.csv')
OUT = os.path.join(MD, 'verify_summary.json')
SUMS = {r'D': os.path.join(MD, 'CHECKSUMS_D.sha256'),
        r'F': os.path.join(MD, 'CHECKSUMS_F.sha256')}

def iter_manifest_files():
    seen = set()
    if not os.path.exists(MANIFEST):
        return
    for row in csv.DictReader(open(MANIFEST, encoding='utf-8')):
        if row['status'] in ('OK', 'SKIP_EXISTS', 'OK_FROM_PART'):
            p = row['dest']
            if p not in seen and os.path.exists(p):
                seen.add(p)
                yield p, int(row['expected_bytes'])

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def check_gz(path):
    with gzip.open(path, 'rb') as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
    return 'gzip_CRC_OK'

def check_nifti(path):
    img = nib.load(path)
    hdr = img.header
    return {'nifti': 'OK', 'dims': list(img.shape),
            'zooms': [round(float(z), 6) for z in hdr.get_zooms()[:3]],
            'dtype': str(hdr.get_data_dtype())}

def check_gii(path):
    g = nib.load(path)
    nv = int(g.darrays[0].data.shape[0]) if g.darrays else 0
    return {'gii': 'OK', 'darrays': len(g.darrays), 'n_vertices': nv}

def check_png(path):
    with open(path, 'rb') as f:
        sig = f.read(8)
        f.seek(-12, 2)
        tail = f.read(12)
    if sig != b'\x89PNG\r\n\x1a\n':
        return {'png': 'BAD_SIGNATURE'}
    if b'IEND' not in tail:
        return {'png': 'BAD_TRAILER'}
    return {'png': 'OK'}


def check_zip(path):
    """Full ZIP member CRC validation via ZipFile.testzip() (returns None when all CRCs pass)."""
    import zipfile
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        n = len(z.namelist())
    if bad is not None:
        return {'zip': f'BAD_CRC:{bad}'}
    return {'zip': 'OK', 'zip_members': n}

def verify(path, exp):
    ext = os.path.basename(path).lower()
    res = {'file': path, 'bytes': os.path.getsize(path)}
    if res['bytes'] != exp:
        res['status'] = 'SIZE_MISMATCH'
        return res
    try:
        if ext.endswith('.nii.gz'):
            res['gzip'] = check_gz(path)
            res.update(check_nifti(path))
        elif ext.endswith('.gii'):
            res.update(check_gii(path))
        elif ext.endswith('.png'):
            res.update(check_png(path))
        elif ext.endswith('.zip'):
            res.update(check_zip(path))
        else:
            res['present'] = 'OK'
        res['sha256'] = sha256(path)
        res['status'] = 'VERIFIED'
    except Exception as e:
        res['status'] = f'VERIFY_FAIL_{type(e).__name__}'
        res['error'] = str(e)[:200]
    return res

def main():
    sums = {r'D': [], r'F': []}
    results = []
    n = 0
    for p, exp in iter_manifest_files():
        r = verify(p, exp)
        results.append(r)
        drive = os.path.splitdrive(p)[0][0]
        if 'sha256' in r:
            sums[drive].append(f"{r['sha256']}  {p}")
        n += 1
        if n % 200 == 0:
            print(f'verified {n}...', flush=True)
    for drv, path in SUMS.items():
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(sums[drv]) + '\n')
    bad = [r for r in results if r.get('status') != 'VERIFIED']
    summary = {'total': len(results),
               'verified': len(results) - len(bad),
               'failed': bad,
               'counts_by_kind': {}}
    for r in results:
        k = ('nifti' if r['file'].endswith('.nii.gz')
             else 'gii' if r['file'].endswith('.gii')
             else 'png' if r['file'].endswith('.png') else 'other')
        summary['counts_by_kind'][k] = summary['counts_by_kind'].get(k, 0) + 1
    json.dump(summary, open(OUT, 'w'), indent=1)
    print(json.dumps(summary['counts_by_kind'], indent=1))
    print(f"total={summary['total']} verified={summary['verified']} failed={len(bad)}")
    for r in bad[:20]:
        print('BAD:', r['file'], r.get('error', r['status']))
    print('VERIFY_DONE')

if __name__ == '__main__':
    main()
