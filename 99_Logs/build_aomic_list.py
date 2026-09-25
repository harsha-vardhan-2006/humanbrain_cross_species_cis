"""Build the download list for the AOMIC-ID1000 human structural connectomes (Zenodo 19796783).

Writes dl_D_aomic.txt as url|dest|bytes using the EXACT sizes from the Zenodo API.
"""
import json, os, urllib.request

REC = 19796783
DEST = r'D:\HumanBrain\12_HumanConnectome_AOMIC\zenodo_19796783_raw'
OUT = r'D:\HumanBrain\00_Metadata\dl_D_aomic.txt'

with urllib.request.urlopen(f'https://zenodo.org/api/records/{REC}', timeout=60) as r:
    d = json.load(r)

lines = []
for f in sorted(d['files'], key=lambda x: x['key']):
    url = f['links']['self']
    dest = os.path.join(DEST, f['key'])
    lines.append(f"{url}|{dest}|{f['size']}")

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines) + '\n')

total = sum(f['size'] for f in d['files'])
print(f'wrote {len(lines)} entries to {OUT}')
print(f'total bytes {total} = {total/1e9:.3f} GB')
for ln in lines:
    print('  ', ln.split('|')[2], os.path.basename(ln.split('|')[1]))
