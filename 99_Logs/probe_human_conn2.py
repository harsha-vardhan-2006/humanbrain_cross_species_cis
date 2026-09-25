"""Detailed inspection of candidate human connectome Zenodo records + download-speed probe."""
import json, urllib.request

IDS = [19796783, 8158914, 10050233, 21771265]

for rid in IDS:
    url = f'https://zenodo.org/api/records/{rid}'
    try:
        with urllib.request.urlopen(url, timeout=45) as r:
            d = json.load(r)
    except Exception as e:
        print(f'[{rid}] error {type(e).__name__}: {e}')
        continue
    md = d['metadata']
    lic = (md.get('license') or {})
    lic = lic.get('id') or lic.get('title') or '?'
    print('=' * 100)
    print(f"[{rid}] {md.get('title')}")
    print(f"  license={lic}  doi={d.get('doi')}  published={md.get('publication_date')}")
    print(f"  creators={[c.get('name') for c in md.get('creators', [])][:5]}")
    desc = (md.get('description') or '').replace('<p>', ' ').replace('</p>', ' ')
    import re
    desc = re.sub(r'<[^>]+>', ' ', desc)
    desc = re.sub(r'\s+', ' ', desc)
    print('  description:', desc[:900])
    files = sorted(d.get('files', []), key=lambda f: -f.get('size', 0))
    print(f'  files ({len(files)}):')
    for f in files[:14]:
        print(f"    {f.get('size',0)/1e6:9.2f} MB  {f.get('key')}")
        print(f"        {f.get('links',{}).get('self')}")
