"""Full detail for AOMIC connectome record 19796783: complete description + all files."""
import json, re, urllib.request

with urllib.request.urlopen('https://zenodo.org/api/records/19796783', timeout=60) as r:
    d = json.load(r)
md = d['metadata']
print('TITLE:', md.get('title'))
print('DOI:', d.get('doi'), '| license:', (md.get('license') or {}).get('id'))
desc = re.sub(r'<[^>]+>', ' ', md.get('description') or '')
desc = re.sub(r'&nbsp;', ' ', desc)
desc = re.sub(r'\s+', ' ', desc)
print('\nFULL DESCRIPTION:\n', desc)
print('\nFILES:')
for f in sorted(d.get('files', []), key=lambda x: -x.get('size', 0)):
    print(f"  {f.get('size',0)/1e6:9.2f} MB  {f.get('key')}  -> {f.get('links',{}).get('self')}")
print('\nRELATED / notes keys:', [k for k in md.keys()])
