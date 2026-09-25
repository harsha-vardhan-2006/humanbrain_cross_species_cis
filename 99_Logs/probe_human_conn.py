"""Probe openly-licensed human connectome sources (Zenodo API) for a precomputed, parcellated structural connectome.

Selection criteria printed per record: license, file count/size, titles of the files.
"""
import json, urllib.request, urllib.parse

QUERIES = [
    'title:"MICA-MICs"',
    'title:("structural connectome") AND title:(human)',
    'title:("group connectome")',
    'title:("connectome") AND title:("HCP") AND type:dataset',
    '("structural connectivity") AND ("parcellation") AND type:dataset',
    'title:("brain connectivity") AND title:("dataset") AND type:dataset',
]


def api(q, size=8):
    url = ('https://zenodo.org/api/records?q=' + urllib.parse.quote(q)
           + f'&type=dataset&size={size}&sort=bestmatch')
    with urllib.request.urlopen(url, timeout=40) as r:
        return json.load(r)


for q in QUERIES:
    print('=' * 100)
    print('QUERY:', q)
    try:
        d = api(q)
    except Exception as e:
        print('  error', type(e).__name__, e)
        continue
    print('  total hits:', d['hits']['total'])
    for h in d['hits']['hits']:
        md = h['metadata']
        lic = (md.get('license') or {})
        lic = lic.get('id') or lic.get('title') or '?'
        files = h.get('files', [])
        tot = sum(f.get('size', 0) for f in files)
        print(f"  [{h['id']}] lic={lic} files={len(files)} {tot/1e6:.1f}MB")
        print('      title:', (md.get('title') or '')[:110])
        for f in files[:6]:
            print(f"      - {f.get('key')}  {f.get('size',0)/1e6:.2f}MB")
