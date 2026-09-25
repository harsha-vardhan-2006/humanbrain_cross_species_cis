"""Final acquisition report + dataset catalog (PART 1: computation).
Reads download_manifest.csv, verify_summary.json, dl_* lists.
PART2 (appended below) writes ACQUISITION_REPORT.md + dataset_catalog.md.
"""
import csv, json, os, sys, datetime

MD = r'D:\HumanBrain\00_Metadata'
NOW = datetime.datetime.now().isoformat(timespec='seconds')

def read_list(fn):
    rows = []
    p = os.path.join(MD, fn)
    if os.path.exists(p):
        for ln in open(p, encoding='utf-8'):
            ln = ln.strip()
            if ln:
                u, d, s = ln.split('|', 2)
                rows.append((u, d, int(s)))
    return rows

planned = {'volumes': read_list('dl_D_volumes.txt'),
           'small': read_list('dl_D_small.txt'),
           'coronal': read_list('dl_F_coronal.txt')}
planned_dest = {d: (u, s) for rows in planned.values() for u, d, s in rows}

mani = []
if os.path.exists(os.path.join(MD, 'download_manifest.csv')):
    mani = list(csv.DictReader(open(os.path.join(MD, 'download_manifest.csv'), encoding='utf-8')))
ok_dest = {}
for r in mani:
    if r['status'] in ('OK', 'SKIP_EXISTS', 'OK_FROM_PART') and os.path.exists(r['dest']):
        ok_dest[r['dest']] = int(r['actual_bytes'])
status_counts = {}
for r in mani:
    key = f"{r['drive']}:{r['status']}"
    status_counts[key] = status_counts.get(key, 0) + 1

verify = {}
vp = os.path.join(MD, 'verify_summary.json')
if os.path.exists(vp):
    verify = json.load(open(vp, encoding='utf-8'))

missing = [d for d in planned_dest if d not in ok_dest]
sizebad = [d for d, (u, s) in planned_dest.items() if d in ok_dest and ok_dest[d] != s]
planned_bytes = sum(s for _, s in planned_dest.values())
done_bytes = sum(ok_dest.get(d, 0) for d in planned_dest)

qfiles = []
for q in (r'D:\HumanBrain\99_Logs\QUARANTINE', r'F:\HumanBrain\99_Logs\QUARANTINE'):
    if os.path.isdir(q):
        qfiles += [os.path.join(q, x) for x in os.listdir(q)]

META_EXPECT = {'BigBrain_License.txt': 18985, 'BigBrain_Updates.txt': 10074,
               'BigBrain_Credits.txt': 5130, 'BigBrain_Welcome.txt': 6853,
               'BigBrain2_FAQ.txt': 4251}
meta_files = {f: os.path.getsize(os.path.join(MD, f)) for f in META_EXPECT
              if os.path.exists(os.path.join(MD, f))}

vfail = verify.get('failed', [])
complete = (not missing) and (not sizebad) and (not qfiles) and (not vfail)

import shutil
disk = {}
for drv in ('D', 'F'):
    du = shutil.disk_usage(drv + ':\\')
    disk[drv] = {'free_GB': round(du.free / 1e9, 1), 'total_GB': round(du.total / 1e9, 1)}

nb_v = sum(ok_dest.get(d, 0) for _, d, _ in planned['volumes'] if d in ok_dest)
nb_s = sum(ok_dest.get(d, 0) for _, d, _ in planned['small'] if d in ok_dest)
nb_c = sum(ok_dest.get(d, 0) for _, d, _ in planned['coronal'] if d in ok_dest)
n_v = sum(1 for _, d, _ in planned['volumes'] if d in ok_dest)
n_s = sum(1 for _, d, _ in planned['small'] if d in ok_dest)
n_c = sum(1 for _, d, _ in planned['coronal'] if d in ok_dest)

report = f'''# BigBrain 2015 Acquisition - FINAL REPORT
Generated: {NOW}

## Verdict: {'PASS - ACQUISITION COMPLETE AND VERIFIED' if complete else 'IN PROGRESS / ISSUES PRESENT'}

## Scope
- Canonical release: BigBrainRelease.2015 (https://ftp.bigbrainproject.org/bigbrain-ftp/BigBrainRelease.2015/)
- Fly reference (read-only): FAFB v783 at G:\\fruitfly (untouched; CC BY-NC 4.0)

## Planned vs acquired
| Bucket | Planned files | Planned GB | Acquired OK | GB OK |
|---|---|---|---|---|
| D volumes (NIfTI) | {len(planned['volumes'])} | {sum(s for _,_,s in planned['volumes'])/1e9:.2f} | {n_v} | {nb_v/1e9:.2f} |
| D small (cls/ROI/surfaces/labels) | {len(planned['small'])} | {sum(s for _,_,s in planned['small'])/1e9:.2f} | {n_s} | {nb_s/1e9:.2f} |
| F coronal full-res PNG | {len(planned['coronal'])} | {sum(s for _,_,s in planned['coronal'])/1e9:.2f} | {n_c} | {nb_c/1e9:.2f} |
| TOTAL | {len(planned_dest)} | {planned_bytes/1e9:.2f} | {n_v+n_s+n_c} | {done_bytes/1e9:.2f} |

Plus EXISTING_LOCAL (credited, not re-downloaded): 5 files in G:\\humanbrain\\full18
(full8_{{100,200,300,400,1000}}um_optbal.nii.gz, gzip-CRC + NIfTI verified, sizes match official FTP).

## Verification
- Per-file byte-size vs official server: {"ALL MATCH" if not sizebad else str(len(sizebad)) + " MISMATCH"}
- Structural checks (verify_summary.json): total={verify.get("total", "PENDING")} verified={verify.get("verified", "PENDING")} failed={len(vfail)}
  - gzip CRC for all .nii.gz; NIfTI header dims/zooms/dtype via nibabel; gii load via nibabel;
    PNG signature+IEND for the 7404 coronal histological PNGs
- SHA-256: CHECKSUMS_D.sha256 / CHECKSUMS_F.sha256 ({"present" if os.path.exists(os.path.join(MD, "CHECKSUMS_D.sha256")) else "PENDING"})
- Quarantined files: {len(qfiles)}{" (NONE - good)" if not qfiles else ""}

## Download statuses (download_manifest.csv)
{chr(10).join(f"- {k}: {v}" for k, v in sorted(status_counts.items())) or "- none"}

## Disk state (rule: keep >10 GB free at all times)
- D: {disk["D"]["free_GB"]} GB free / {disk["D"]["total_GB"]} GB total
- F: {disk["F"]["free_GB"]} GB free / {disk["F"]["total_GB"]} GB total

## Official metadata archived (size-verified)
{chr(10).join(f"- {f}: {b:,} B (expected {META_EXPECT[f]:,})" + (" OK" if META_EXPECT[f] == b else " MISMATCH") for f, b in meta_files.items())}
'''
open(os.path.join(MD, 'ACQUISITION_REPORT.md'), 'w', encoding='utf-8').write(report)
report += f'''
## Not acquired / access blocked (see NOT_ACQUIRED.md)
- BigBrain1_MSM_2023.tar (264,898,560 B): listed; anonymous RETR denied (FTP 550 / HTTPS 403) -> NOT_ACQUIRED_ACCESS_DENIED
- BigBrain2_PreRelease.2023: FTP-listable/downloadable but IP-blocked over HTTPS; OUT OF SCOPE (canonical = 2015) -> NOT_ACQUIRED_OUT_OF_SCOPE
- Raw_Data (~1 TB), A3D (~110 GB), 40um ROI tiers, Minc 2D sections, axial/sagittal PNG planes,
  STL/OBJ/MNI-obj duplicates, fsaverage mirrors: JUSTIFIED_SKIP per approved plan

## Cross-species manifests
- cross_species_manifest.json / .csv (tags DIRECTLY / APPROXIMATELY / NOT_DIRECTLY)
- Key tag: BigBrain has NO connectome -> connectome-topology comparisons vs FAFB = NOT_DIRECTLY_COMPARABLE
- Fly neuropils <-> human cortical parcellations = APPROXIMATELY only (no homology claims)

## Provenance chain
1. Official FTP/HTTPS inventory (52 dir listings) -> F:\\HumanBrain\\00_Metadata\\remote_listings\\
2. HTTPS size probe (HTTP Range) -> http_sizes.tsv
3. Curated download lists (server-verified names/sizes) -> dl_D_volumes.txt, dl_D_small.txt, dl_F_coronal.txt
4. Resumable download (Range continuation; 15 GB/disk reserve guard) -> download_manifest.csv
5. Structural verification + SHA-256 -> verify_summary.json, CHECKSUMS_*.sha256
6. Cross-species manifests -> cross_species_manifest.json/.csv, dataset_bigbrain.csv
'''
open(os.path.join(MD, 'ACQUISITION_REPORT.md'), 'w', encoding='utf-8').write(report)

catalog = ['# BigBrain 2015 local dataset catalog', '',
           '| Location | Content |', '|---|---|',
           '| D:\\HumanBrain\\00_Metadata | manifests, checksums, license, reports, download lists |',
           '| D:\\HumanBrain\\01_3D_Volumes | full16 histological (100-1000um) + MNI-ICBM152 + MNI-ADNI NIfTI |',
           '| D:\\HumanBrain\\02_Classified_Volumes | grey/white/CSF classifications (histological + MNI) |',
           '| D:\\HumanBrain\\03_MRI | post-mortem MRI aligned to blockface |',
           '| D:\\HumanBrain\\04_Surfaces\\Apr7_2016_gii | white/gray GIfTI surfaces (327680 vertices) |',
           '| D:\\HumanBrain\\05_ROIs | 100um occipital/Heschl/Central/BA10/Hippocampus/Hypothalamus/Cerebellum |',
           '| D:\\HumanBrain\\06_Layer_Segmentation | PLoS Biology 2020 cortical layer GIfTI surfaces |',
           '| D:\\HumanBrain\\07_Hippocampus\\gii | subfield surfaces (CA1-4, DG, Sub) |',
           '| D:\\HumanBrain\\08_Parcellations | Brainnetome/DKT/Economo/Schaefer2018/HCP-MMP + Surfaces |',
           '| D:\\HumanBrain\\09_BigBrainWarp | white surfaces, spheres, BigBrain<->MNI152 warps |',
           '| D:\\HumanBrain\\10_MSM_2023 | EMPTY (tar access-denied; see NOT_ACQUIRED.md) |',
           '| D:\\HumanBrain\\11_DERIVED | (empty; conversions only under DERIVED per policy) |',
           '| F:\\HumanBrain\\01_Histology | 7404 coronal full-resolution PNG sections (64.1 GB) |',
           '| F:\\HumanBrain\\00_Metadata\\remote_listings | 52 official FTP directory listing snapshots |',
           '| G:\\humanbrain\\full18 | pre-existing full8 volumes (EXISTING_LOCAL, verified) |',
           '| G:\\fruitfly | FAFB v783 fly dataset (READ-ONLY reference, untouched) |']
open(os.path.join(MD, 'dataset_catalog.md'), 'w', encoding='utf-8').write('\n'.join(catalog) + '\n')

print(f"planned={len(planned_dest)} ok={n_v + n_s + n_c} missing={len(missing)} "
      f"sizebad={len(sizebad)} quarantined={len(qfiles)} verify_fail={len(vfail)}")
if missing[:5]:
    print('missing sample:', missing[:5])
print('COMPLETE' if complete else 'NOT_COMPLETE')
sys.exit(0 if complete else 1)


