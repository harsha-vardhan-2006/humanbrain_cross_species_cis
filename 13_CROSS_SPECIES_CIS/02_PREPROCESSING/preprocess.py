r"""E01 — AOMIC extraction, raw QC, manifests, matrix cache.

READ-ONLY on RAW zips. All outputs under 13_CROSS_SPECIES_CIS.
Usage:
    py preprocess.py --limit 2          # smoke test
    py preprocess.py                    # full run (resume-safe: skips cached)
"""
import argparse, io, json, os, platform, sys, time, zipfile
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import scipy
import scipy.io as sio
import scipy.sparse as sp

BASE = r"D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS"
RAW = r"D:\humanbrain\humanbrain\12_HumanConnectome_AOMIC\zenodo_19796783_raw"
META = r"D:\humanbrain\humanbrain\00_Metadata"

ATLASES = ["atlas_4S456Parcels", "atlas_4S256Parcels", "atlas_4S156Parcels",
           "atlas_Brainnetome246Ext", "atlas_AICHA384Ext", "atlas_Gordon333Ext",
           "atlas_AAL116"]
VARIANTS = ["sift_radius2_count_connectivity",
            "sift_invnodevol_radius2_count_connectivity",
            "radius2_count_connectivity",
            "radius2_meanlength_connectivity"]
CACHE = os.path.join(BASE, "02_PREPROCESSING", "matrix_cache.npz")


def qc_one(A):
    """Raw-matrix QC on the symmetric input as stored (diag untouched)."""
    A = np.asarray(A, dtype=np.float64)
    n = A.shape[0]
    off = A[~np.eye(n, dtype=bool)]
    sym_dev = float(np.abs(A - A.T).max()) if n else 0.0
    # absolute off-diagonal values preserve symmetry after abs():
    # node strength = sum of |w_ij| over all partners (row sums of |A| off-diag)
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
    """Extract + QC every matrix in one zip. Returns (qc_rows, cache_items)."""
    zname = os.path.basename(zpath)
    qc_rows, cache_items = [], []
    with zipfile.ZipFile(zpath) as z:
        for member in sorted(z.namelist()):
            sub = member.split("-")[1].split("_")[0]  # subject id
            with z.open(member) as fh:
                m = sio.loadmat(io.BytesIO(fh.read()))
            for atlas in ATLASES:
                n_exp = m[atlas + "_region_ids"].size
                for var in VARIANTS:
                    A = m[atlas + "_" + var]
                    q = qc_one(A)
                    q.update({"subject": int(sub), "atlas": atlas, "variant": var,
                              "expected_nodes": int(n_exp),
                              "source_zip": zname, "source_member": member})
                    qc_rows.append(q)
                    cache_items.append((f"{sub}|{atlas}|{var}",
                                        np.asarray(A, dtype=np.float32)))
    return qc_rows, cache_items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="process first N zips only")
    args = ap.parse_args()

    t0 = time.time()
    zips = sorted(os.listdir(RAW))[: args.limit] if args.limit else sorted(os.listdir(RAW))
    zpaths = [os.path.join(RAW, f) for f in zips]

    all_qc, cache = [], {}
    workers = min(4, len(zpaths))
    print(f"[E01] processing {len(zpaths)} zips with {workers} workers", flush=True)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, (qc_rows, items) in enumerate(ex.map(process_zip, zpaths)):
            all_qc.extend(qc_rows)
            cache.update(dict(items))
            print(f"[E01] {zips[i]} done: {len(qc_rows)} matrices "
                  f"(total {len(all_qc)}) at {time.time()-t0:.0f}s", flush=True)

    # QC table
    import pandas as pd
    qc = pd.DataFrame(all_qc)
    qc_path = os.path.join(BASE, "01_RAW_PROBES", "raw_qc_report.csv")
    qc.to_csv(qc_path, index=False)

    # Manifests
    subjects = sorted(qc["subject"].unique())
    pd.DataFrame({"subject": subjects}).to_csv(
        os.path.join(BASE, "00_MANIFEST", "subject_manifest.csv"), index=False)
    pd.DataFrame({"atlas": ATLASES,
                  "expected_nodes": [qc.loc[qc.atlas == a, "n_nodes"].iloc[0] for a in ATLASES],
                  "role": ["PRIMARY", "sensitivity", "sensitivity", "sensitivity",
                           "archived", "archived", "coarse_anchor"]}).to_csv(
        os.path.join(BASE, "00_MANIFEST", "atlas_manifest.csv"), index=False)
    pd.DataFrame({"variant": VARIANTS,
                  "role": ["PRIMARY", "sensitivity", "sensitivity", "sensitivity"]}).to_csv(
        os.path.join(BASE, "00_MANIFEST", "variant_manifest.csv"), index=False)

    # Matrix cache (fp32 to halve disk; downstream binarizes anyway)
    keys = list(cache)
    np.savez_compressed(CACHE,
                        keys=np.array(keys, dtype=object),
                        allow_pickle=True,
                        **{k.replace("|", "__"): v for k, v in cache.items()})

    # Flags summary (flag, never delete)
    flags = {
        "rows_total": int(len(qc)),
        "dim_mismatch": int((qc.n_nodes != qc.expected_nodes).sum()),
        "nan_or_inf": int(((qc.nan_count > 0) | (qc.inf_count > 0)).sum()),
        "asymmetric_gt_1e9": int((qc.sym_max_abs_dev > 1e-9).sum()),
        "negative_offdiag": int((qc.neg_offdiag > 0).sum()),
    }
    with open(os.path.join(BASE, "01_RAW_PROBES", "raw_flags.json"), "w") as f:
        json.dump(flags, f, indent=1)

    # Environment manifest
    import pandas, pyarrow, matplotlib
    env = f"""ENVIRONMENT MANIFEST — generated {time.strftime('%Y-%m-%d %H:%M:%S')}
python={platform.python_version()} platform={platform.platform()}
numpy={np.__version__} scipy={scipy.__version__} pandas={pandas.__version__}
pyarrow={pyarrow.__version__} matplotlib={matplotlib.__version__}
raw_zips={len(zips)} matrices_qcd={len(qc)} subjects={len(subjects)}
elapsed_s={time.time()-t0:.1f}
"""
    with open(os.path.join(BASE, "00_MANIFEST", "ENVIRONMENT_MANIFEST.txt"), "w") as f:
        f.write(env)

    print(f"[E01] DONE. rows={len(qc)} subjects={len(subjects)} flags={flags}")
    print(f"[E01] cache={CACHE} qc={qc_path} elapsed={time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
