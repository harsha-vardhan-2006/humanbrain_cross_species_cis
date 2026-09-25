"""Cross-species builder STEP 2: comparability tags + final manifests + integrity report.
Reads csm_state.json; writes cross_species_manifest.json/.csv, dataset_bigbrain.csv,
INTEGRITY_REPORT.md in D:\\HumanBrain\\00_Metadata.
"""
import csv, json, os

MD = r'D:\HumanBrain\00_Metadata'
st = json.load(open(os.path.join(MD, 'csm_state.json'), encoding='utf-8'))

human_dataset = {
    'dataset_id': 'BigBrain_2015',
    'species': 'Homo sapiens (65yo male, post-mortem histology)',
    'modality': 'histological volume (20um sections) + classified volumes + surfaces/parcellations',
    'location': r'D:\HumanBrain + F:\HumanBrain',
    'role': 'ACQUIRED_LOCAL_COPY',
    'license': 'CC BY-NC-SA 4.0 (research-only, no commercial use, share-alike)',
    'canonical_release': 'BigBrainRelease.2015',
    'official_source': 'https://ftp.bigbrainproject.org/bigbrain-ftp/BigBrainRelease.2015/',
    'provenance_basis': ('Per-file size pre-check vs official server; byte-count verification; '
                         'gzip-CRC + NIfTI/gii/PNG structural validation; '
                         'SHA-256 in CHECKSUMS_D/F.sha256'),
}

COMPARABILITY = [
    {'pair_id': 'CP01',
     'fly': 'FAFB v783 whole-brain EM volume (neuropil)',
     'human': 'BigBrain full16/full8 optbal histological volumes (histological space)',
     'tag': 'NOT_DIRECTLY_COMPARABLE',
     'reason': ('BigBrain provides NO connectome; FAFB provides no cellular-resolution anatomy '
                'of human brain. Both whole-brain structural datasets but different modalities, '
                'species, and scales.')},
    {'pair_id': 'CP02',
     'fly': 'FAFB hemisphere/side separation of neurons (L/R)',
     'human': 'BigBrain hemispheres_mask_*.nii.gz (L/R masks)',
     'tag': 'APPROXIMATELY_COMPARABLE',
     'reason': ('Both encode bilateral symmetry structure; resolution and semantics differ '
                '(neuron level vs voxel level).')},
    {'pair_id': 'CP03',
     'fly': 'FAFB fly neuropils (e.g., optic lobes, central brain compartments)',
     'human': 'BigBrain cortical parcellations (Brainnetome, DKT, Economo, Schaefer2018, HCP-MMP)',
     'tag': 'APPROXIMATELY_COMPARABLE',
     'reason': ('Region-level organizational comparison only. NO homology claims between fly '
                'neuropils and human cortical areas.')},
    {'pair_id': 'CP04',
     'fly': 'FAFB neuron/synapse counts (connectome topology)',
     'human': 'BigBrain classified volume class statistics (grey/white/CSF fractions)',
     'tag': 'NOT_DIRECTLY_COMPARABLE',
     'reason': 'Connectome topology vs tissue-class volumetry: no common graph space.'},
    {'pair_id': 'CP05',
     'fly': 'FAFB visual-system subconnectomes (optic lobe circuits)',
     'human': 'BigBrain occipital/cerebellum ROI volumes at 100um',
     'tag': 'APPROXIMATELY_COMPARABLE',
     'reason': ('Coarse sensory-region correspondence only (visual processing regions); '
                'no cell-type or circuit homology implied.')},
]

cross = {
    'generated': st['now'],
    'generator': r'D:\HumanBrain\99_Logs\csm_collect.py + csm_finalize.py',
    'datasets': [st['fly_dataset'], human_dataset],
    'comparability_pairs': COMPARABILITY,
    'shared_assets': st['shared_assets'],
    'human_files': st['human_files'],
    'fly_manifest_summary': {'n_entries': st['fly_n'],
                             'file': st['fly_dataset']['source_manifest'],
                             'immutable_reference': True},
    'notes': [
        'G: drive is strictly read-only; nothing written there.',
        'BigBrain2_PreRelease.2023 exists on server (FTP-listable) but is OUT OF SCOPE; '
        'HTTPS access is IP-restricted (MCIN network only).',
        'BigBrain1_MSM_2023.tar (264,898,560 B) listed but anonymous download denied '
        '(550/403) -> NOT_ACQUIRED_ACCESS_DENIED.',
        'Comparability tags: DIRECTLY / APPROXIMATELY / NOT_DIRECTLY; fly-neuropil to '
        'human-parcellation mappings are APPROXIMATELY only (no homology claims).',
    ],
}
json.dump(cross, open(os.path.join(MD, 'cross_species_manifest.json'), 'w', encoding='utf-8'), indent=1)

with open(os.path.join(MD, 'cross_species_manifest.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['pair_id', 'fly_asset', 'human_asset', 'comparability_tag', 'reason'])
    for p in COMPARABILITY:
        w.writerow([p['pair_id'], p['fly'], p['human'], p['tag'], p['reason']])

with open(os.path.join(MD, 'dataset_bigbrain.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['file', 'bytes', 'source', 'status', 'url'])
    for f_ in st['human_files']:
        w.writerow([f_['file'], f_['bytes'], f_['source'], f_['status'], f_['url'] or ''])

nb = sum(f_['bytes'] for f_ in st['human_files'])
tags = '\n'.join(f"- {p['pair_id']}: {p['tag']}" for p in COMPARABILITY)
with open(os.path.join(MD, 'INTEGRITY_REPORT.md'), 'w', encoding='utf-8') as fh:
    fh.write(f'''# BigBrain 2015 Acquisition - Integrity Report (LIVE)
Generated: {st['now']}

## Human dataset (BigBrainRelease.2015)
- Files recorded so far: {len(st['human_files'])}
- Bytes so far: {nb:,} ({nb/1e9:.2f} GB)
- Verification: byte-size vs official FTP (all rows) + gzip-CRC/NIfTI/gii/PNG structural
  checks + SHA-256 (CHECKSUMS_D.sha256 / CHECKSUMS_F.sha256, generated post-download)

## Fly dataset (FAFB v783) - read-only reference
- Source manifest: {st['fly_dataset']['source_manifest']} ({st['fly_n']} entries)
- Untouched; used only as reference for cross-species manifests.

## Comparability tagging (mandatory)
{tags}

## Not acquired (recorded, no guessing)
- BigBrain2_PreRelease.2023: server-listable via FTP; HTTPS IP-restricted; out of approved
  scope -> NOT_ACQUIRED_OUT_OF_SCOPE
- BigBrain1_MSM_2023.tar: 264,898,560 B listed; anonymous RETR denied -> NOT_ACQUIRED_ACCESS_DENIED
- 3D A3D hippocampus model (~110 GB), Raw_Data (~1 TB), 40um ROI subsets, STL/JSON/OBJ
  duplicates, fsaverage mirrors: JUSTIFIED_SKIP (per approved plan)

Status: DOWNLOADS_IN_PROGRESS (resumable; see download_manifest.csv)
''')
print('cross_species_manifest.json/.csv, dataset_bigbrain.csv, INTEGRITY_REPORT.md written')
print(f"human files: {len(st['human_files'])} ({nb/1e9:.2f} GB)")
print('STEP2_DONE')


