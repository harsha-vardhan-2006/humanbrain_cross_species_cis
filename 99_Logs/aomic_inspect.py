r"""Inspect the FIRST completed AOMIC zip: member layout, atlases, atlas dictionary, one subject's connectome shape.

Writes: D:\HumanBrain\99_Logs\aomic_inspect_out.log
"""
import glob, io, os, zipfile
import numpy as np
import pandas as pd

RAW = r'D:\HumanBrain\12_HumanConnectome_AOMIC\zenodo_19796783_raw'


def main():
    done = sorted(glob.glob(os.path.join(RAW, 'connectomes_part_*.zip')))
    print('completed zips:', [os.path.basename(f) for f in done])
    if not done:
        print('NO_COMPLETED_ZIP_YET')
        return
    zf = done[0]
    print('inspecting:', zf, os.path.getsize(zf))
    with zipfile.ZipFile(zf) as z:
        bad = z.testzip()
        names = z.namelist()
    print('zip CRC bad member:', bad)
    print('members:', len(names))
    top = {}
    for n in names:
        k = n.split('/')[0] if '/' in n else '(root)'
        top[k] = top.get(k, 0) + 1
    print('top-level dirs:', top)
    atlas_files = [n for n in names if 'atlas' in n.lower() or 'dict' in n.lower() or 'label' in n.lower()]
    print('atlas/dict/label members:', len(atlas_files))
    for n in sorted(atlas_files)[:20]:
        print('  ', n)
    conn = [n for n in names if 'connect' in n.lower() and n.endswith(('.csv', '.tsv', '.npy', '.txt', '.mat'))]
    print('connectivity members:', len(conn))
    for n in sorted(conn)[:10]:
        print('  ', n)
    with zipfile.ZipFile(zf) as z:
        for n in sorted(conn)[:5]:
            with z.open(n) as fh:
                data = fh.read(200000)
            print(f'  --- {n}: first 400 bytes ---')
            print('   ', data[:400].decode(errors='replace').replace(chr(10), ' | ')[:400])


if __name__ == '__main__':
    main()
