r"""E01 v2 — AOMIC extraction, raw QC, manifests. RESUME-SAFE part cache.

Why v2: the original preprocess.py accumulated every worker's matrices in the
parent process before writing one giant npz -> RAM exhaustion (WinError 1450)
after zip 1/10. v2 writes ONE npz part per raw zip (worker writes its own
file; parent stays lightweight) and skips already-completed parts.

READ-ONLY on RAW zips. All outputs under 13_CROSS_SPECIES_CIS.

Outputs:
    02_PREPROCESSING/cache_parts/cache_part_NN.npz   (fp32 matrices)
    02_PREPROCESSING/cache_keys.csv                  (key index)
    01_RAW_PROBES/raw_qc_report.csv                  (full QC, all 7x4 combos)
    01_RAW_PROBES/raw_flags.json
    00_MANIFEST/subject_manifest.csv / atlas_manifest.csv / variant_manifest.csv
    00_MANIFEST/ENVIRONMENT_MANIFEST.txt

Usage:
    py preprocess_v2.py          # full run (resume-safe)
    py preprocess_v2.py --limit 2
"""
import argparse, io, json, os, platform, sys, time, zipfile
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import scipy
import scipy.io as sio

BASE = r"D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS"
RAW = r"D:\humanbrain\humanbrain\12_HumanConnectome_AOMIC\zenodo_19796783_raw"
PARTS = os.path.join(BASE, "02_PREPROCESSING", "cache_parts")

ATLASES = ["atlas_4S456Parcels", "atlas_4S256Parcels", "atlas_4S156Parcels",
           "atlas_Brainnetome246Ext", "atlas_AICHA384Ext", "atlas_Gordon333Ext",
           "atlas_AAL116"]
VARIANTS = ["sift_radius2_count_connectivity",
            "sift_invnodevol_radius2_count_connectivity",
            "radius2_count_connectivity",
            "radius2_meanlength_connectivity"]


def qc_one(A):
    """Raw-matrix QC on the symmetric input as stored (diag untouched)."""
    A = np.asarray(A, dtype=np.float64)
    n = A.shape[0]
    off = A[~np.eye(n, dtype=bool)]
    sym_dev = float(np.abs(A - A.T).max()) if n else 0.0
    absA = np.abs(A)
    np.fill_diagonal(absA, 0.0)
    strength = absA.sum(1)
    return {
        "n_nodes": int(n),
        "sym_max_abs_dev": sym_dev,
        "diag_nonzero": int((np.diag(A) != 0).sum()),
        "nan_count": int(np.isnan(A).sum()),
        "inf_count": int(np.isinf(A).sum()),
        "neg_offdiag": int((off < 0).sum()),
        "zero_offdiag": int((off == 0).sum()),
        "offdiag_density": float((off != 0).mean()),
        "strength_mean": float(strength.mean()),
        "strength_median": float(np.median(strength)),
        "strength_p95": float(np.percentile(strength, 95)),
        "weight_min": float(off.min()), "weight_max": float(off.max()),
    }


def process_zip(zpath):
    """QC + cache every matrix in one zip; worker writes its own npz part.

    Returns only a small record dict to the parent (RAM-safe).
    """
    zname = os.path.basename(zpath)
    znum = int(zname.split("part_")[1].split(".")[0])
    part_file = f"cache_part_{znum:02d}.npz"
    part_path = os.path.join(PARTS, part_file)

    rec = {"zip": zname, "part_file": part_file, "status": "skipped_existing",
           "qc_rows": None, "keys": None, "elapsed_s": None}

    if os.path.exists(part_path):
        return rec  # resume-safe: part already written

    t0 = time.time()
    qc_rows, cache = [], {}
    with zipfile.ZipFile(zpath) as z:
        for member in sorted(z.namelist()):
            sub = int(member.split("-")[1].split("_")[0])
            with z.open(member) as fh:
                m = sio.loadmat(io.BytesIO(fh.read()))
            for atlas in ATLASES:
                n_exp = int(m[atlas + "_region_ids"].size)
                for var in VARIANTS:
                    A = m[atlas + "_" + var]
                    q = qc_one(A)
                    q.update({"subject": sub, "atlas": atlas, "variant": var,
                              "expected_nodes": n_exp,
                              "source_zip": zname, "source_member": member})
                    qc_rows.append(q)
                    cache[f"{sub}|{atlas}|{var}".replace("|", "__")] = \
                        np.asarray(A, dtype=np.float32)

    # keys for this part (subject-level: all atlases x variants)
    keys_df = []
    subs = sorted({int(k.split("__")[0]) for k in cache})
    for s in subs:
        for a in ATLASES:
            for v in VARIANTS:
                kk = f"{s}|{a}|{v}"
                if kk.replace("|", "__") in cache:
                    keys_df.append({"key": kk, "subject": s, "atlas": a,
                                    "variant": v, "part_file": part_file})

    # worker writes its own part file (never returned to parent)
    np.savez_compressed(part_path, **cache)
    import pandas as pd
    pd.DataFrame(keys_df).to_csv(part_path.replace(".npz", "_keys.csv"), index=False)

    # return only the QC rows (small) to the parent
    rec["qc_rows"] = qc_rows
    rec["keys"] = keys_df
    rec["status"] = "ok"
    rec["elapsed_s"] = round(time.time() - t0, 1)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    t0 = time.time()
    os.makedirs(PARTS, exist_ok=True)
    zips = sorted(os.listdir(RAW))
    if args.limit:
        zips = zips[: args.limit]
    zpaths = [os.path.join(RAW, f) for f in zips]

    all_qc, all_keys, processed = [], [], []
    workers = 4
    print(f"[E01v2] {len(zpaths)} zips, {workers} workers, resume-safe", flush=True)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(process_zip, zpaths)):
            if rec["qc_rows"] is not None:
                all_qc.extend(rec["qc_rows"])
                all_keys.extend(rec["keys"])
                processed.append(rec["zip"])
            print(f"[E01v2] {rec['zip']}: {rec['status']} "
                  f"({rec['elapsed_s']}s) at {time.time()-t0:.0f}s", flush=True)

    # merge per-part key indexes from disk (resume case: parts skipped above)
    import pandas as pd
    key_parts = sorted(f for f in os.listdir(PARTS) if f.endswith("_keys.csv"))
    if key_parts:
        all_keys = pd.concat([pd.read_csv(os.path.join(PARTS, f))
                              for f in key_parts], ignore_index=True)
    all_keys = pd.DataFrame(all_keys).drop_duplicates("key").sort_values("key")
    all_keys.to_csv(os.path.join(BASE, "02_PREPROCESSING", "cache_keys.csv"),
                    index=False)

    # QC table: replace rows only for zips actually re-processed this run
    qc_path = os.path.join(BASE, "01_RAW_PROBES", "raw_qc_report.csv")
    if os.path.exists(qc_path):
        old = pd.read_csv(qc_path)
        if processed:
            old = old[~old.source_zip.isin(processed)]
        if all_qc:
            old = pd.concat([old, pd.DataFrame(all_qc)], ignore_index=True)
        qc = old
    else:
        qc = pd.DataFrame(all_qc)
    qc = qc.drop_duplicates(["subject", "atlas", "variant"]).sort_values(
        ["subject", "atlas", "variant"])
    qc.to_csv(qc_path, index=False)

    # Manifests
    subjects = sorted(qc["subject"].unique())
    pd.DataFrame({"subject": subjects}).to_csv(
        os.path.join(BASE, "00_MANIFEST", "subject_manifest.csv"), index=False)
    pd.DataFrame({"atlas": ATLASES,
                  "expected_nodes": [qc.loc[qc.atlas == a, "n_nodes"].iloc[0]
                                     for a in ATLASES],
                  "role": ["PRIMARY", "sensitivity", "sensitivity", "sensitivity",
                           "archived", "archived", "coarse_anchor"]}).to_csv(
        os.path.join(BASE, "00_MANIFEST", "atlas_manifest.csv"), index=False)
    pd.DataFrame({"variant": VARIANTS,
                  "role": ["PRIMARY", "sensitivity", "sensitivity",
                           "sensitivity"]}).to_csv(
        os.path.join(BASE, "00_MANIFEST", "variant_manifest.csv"), index=False)

    # Flags summary (flag, never delete)
    flags = {
        "rows_total": int(len(qc)),
        "subjects_total": int(len(subjects)),
        "dim_mismatch": int((qc.n_nodes != qc.expected_nodes).sum()),
        "nan_or_inf": int(((qc.nan_count > 0) | (qc.inf_count > 0)).sum()),
        "asymmetric_gt_1e9": int((qc.sym_max_abs_dev > 1e-9).sum()),
        "negative_offdiag": int((qc.neg_offdiag > 0).sum()),
        "cache_matrices": int(len(all_keys)),
        "cache_subjects": int(all_keys.subject.nunique()),
    }
    with open(os.path.join(BASE, "01_RAW_PROBES", "raw_flags.json"), "w") as f:
        json.dump(flags, f, indent=1)

    # Environment manifest (append-style v2 record)
    import pandas as pd_  # noqa: F401  (pandas version)
    import pyarrow, matplotlib
    env = (open(os.path.join(BASE, "00_MANIFEST",
                             "ENVIRONMENT_MANIFEST.txt")).read()
           if os.path.exists(os.path.join(BASE, "00_MANIFEST",
                                          "ENVIRONMENT_MANIFEST.txt")) else "")
    marker = "" if env.endswith("\n") or not env else "\n"
    env += (marker + f"""--- E01v2 rerun generated {time.strftime('%Y-%m-%d %H:%M:%S')}
python={platform.python_version()} platform={platform.platform()}
numpy={np.__version__} scipy={scipy.__version__} pandas={pd.__version__}
pyarrow={pyarrow.__version__} matplotlib={matplotlib.__version__}
raw_zips={len(zips)} cache_parts={len(key_parts)} cache_matrices={flags['cache_matrices']}
subjects={flags['subjects_total']} rows_qcd={flags['rows_total']} elapsed_s={time.time()-t0:.1f}
""")
    with open(os.path.join(BASE, "00_MANIFEST", "ENVIRONMENT_MANIFEST.txt"), "w") as f:
        f.write(env)

    print(f"[E01v2] DONE. rows={len(qc)} subjects={len(subjects)} flags={flags}")
    print(f"[E01v2] cache parts={len(key_parts)} elapsed={time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
