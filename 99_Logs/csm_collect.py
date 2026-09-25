"""Cross-species builder STEP 1: collect fly + human file states -> csm_state.json"""
import csv, glob, json, os, datetime

G_FAFB = r'G:\fruitfly'
MD = r'D:\HumanBrain\00_Metadata'
NOW = datetime.datetime.now().isoformat(timespec='seconds')

e18_path = os.path.join(G_FAFB, 'results', 'tables', 'e18_manifest.json')
fafb = json.load(open(e18_path, encoding='utf-8'))
fly_files = fafb.get('files', fafb) if isinstance(fafb, dict) else fafb
print(f'FAFB e18_manifest: {len(fly_files)} entries')

fly_dataset = {
    'dataset_id': 'FAFB_v783',
    'species': 'Drosophila melanogaster (adult fruit fly)',
    'modality': 'serial-section EM connectome + skeleton graph',
    'location': G_FAFB,
    'role': 'READ_ONLY_REFERENCE',
    'license': 'CC BY-NC 4.0',
    'source_manifest': e18_path,
    'provenance_basis': ('Verified from its own README/LICENSE_NOTES/QC docs (not folder name); '
                         'SHA256 manifest for 19 raw files; frozen 138,584-neuron/3.7M-edge analysis graph'),
    'immutable': True,
}

human_files = []
bb_manifest = os.path.join(MD, 'download_manifest.csv')
if os.path.exists(bb_manifest):
    for row in csv.DictReader(open(bb_manifest, encoding='utf-8')):
        if row['status'] in ('OK', 'SKIP_EXISTS', 'OK_FROM_PART') and os.path.exists(row['dest']):
            human_files.append({'file': row['dest'], 'bytes': int(row['actual_bytes']),
                                'source': 'DOWNLOADED_2015_RELEASE', 'url': row['url'],
                                'status': row['status']})

EXISTING = [
    (r'G:\humanbrain\full18\full8_1000um_optbal.nii.gz', 726447, [140, 154, 121], [1.0, 1.0, 1.0]),
    (r'G:\humanbrain\full18\full8_100um_optbal.nii.gz', 602235591, [1392, 1541, 1209], [0.1, 0.1, 0.1]),
    (r'G:\humanbrain\full18\full8_200um_optbal.nii.gz', 77629942, [696, 770, 605], [0.2, 0.2, 0.2]),
    (r'G:\humanbrain\full18\full8_300um_optbal.nii.gz', 23703846, [465, 515, 403], [0.3, 0.3, 0.3]),
    (r'G:\humanbrain\full18\full8_400um_optbal.nii.gz', 10294542, [348, 386, 303], [0.4, 0.4, 0.4]),
]
for p, b, dims, zooms in EXISTING:
    if os.path.exists(p) and os.path.getsize(p) == b:
        human_files.append({'file': p, 'bytes': b, 'source': 'EXISTING_LOCAL_PREVERIFIED',
                            'url': None, 'status': 'EXISTING_LOCAL',
                            'nifti_dims': dims, 'nifti_zooms_mm': zooms,
                            'note': 'gzip CRC + nibabel header verified 2026-09-19; '
                                    'size matches official FTP; not re-downloaded'})

shared_assets = []
for c in [r'G:\fruitfly\tools\flyvqa.py', r'G:\fruitfly\tools\flyvqa_config.json',
          r'G:\fruitfly\tools\extract_flyvqa.py']:
    if os.path.exists(c):
        shared_assets.append({'path': c, 'bytes': os.path.getsize(c), 'mode': 'READ_ONLY_REFERENCE'})
if not shared_assets:
    print('NOTE: flyvqa tools not found; tools dir sample:',
          sorted(glob.glob(r'G:\fruitfly\tools\*'))[:10])

json.dump({'now': NOW, 'fly_dataset': fly_dataset,
           'fly_n': len(fly_files), 'human_files': human_files,
           'shared_assets': shared_assets},
          open(os.path.join(MD, 'csm_state.json'), 'w'), indent=1)
print(f'human files so far: {len(human_files)} '
      f'({sum(f["bytes"] for f in human_files)/1e9:.2f} GB)')
print('STEP1_DONE')
