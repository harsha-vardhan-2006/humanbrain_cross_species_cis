r"""E05 — Observed vs null statistics + population CIS results (frozen).

Runs ONLY after E03 (subject_cis complete for the QC cohort) and E04 battery A
(100 subjects x 100 degree-preserving nulls) + battery B (200 subjects).
Implements PROTOCOL_FREEZE §6 statistics:

  1. Per-node population null test (battery A): per subject and node, empirical
     one-sided p = (#nulls >= observed + 1)/(100+1); combined across subjects
     with Stouffer's Z; BH-FDR (q=0.05) across the 456 nodes (single stratum =
     the primary configuration).
  2. Top-K system enrichment (fly E12-strong template): population top-K nodes
     by mean CIS (K in {25, 50, 100}); control A = tested universe (node-label
     shuffle, 10,000 reps); control B = degree-matched peer pools (+-10% mean
     degree, nearest-50 fallback, resampled 10,000 reps); z_A, z_B,
     enrichment ratios, empirical p.
  3. Battery B: population top-50 concentration vs nulls (per-subject z and
     empirical p; sign test across subjects).
  4. Rank stability: Spearman between mean-CIS ranks of 100 random half-splits
     (seed 20260922) -> median r.
  5. Degree/strength association: per-subject Spearman(CIS, degree) and
     Spearman(CIS, strength) -> medians.

Outputs:
  04_CIS/e05_statistics.json
  09_TABLES/table_07_null_results.csv          (per-node Stouffer table)
  09_TABLES/table_population_cis_summary.csv
  04_CIS/POPULATION_CIS_RESULTS.md
"""
import json, os, sys, time

import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata, binomtest, spearmanr

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "02_PREPROCESSING"))
from cache_io import BASE

COST = 0.15
N_NULLS = 100
SUBJECT_SEED = 20260922
N_PERM = 10_000
SYSTEMS = ["Vis", "SomMot", "DorsAttn", "SalVentAttn", "Limbic", "Cont",
           "Default", "Subcortical_Cerebellar"]
A_DIR = os.path.join(BASE, "05_NULLS", "degree_preserving", "battery_a")
B_DIR = os.path.join(BASE, "05_NULLS", "degree_preserving", "battery_b")
SUBJ_DIR = os.path.join(BASE, "04_CIS", "subject_cis")


def load_observed():
    qc = pd.read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
    qc_pass = set(qc.loc[qc.qc_pass, "subject"].astype(int))
    frames = []
    for f in sorted(os.listdir(SUBJ_DIR)):
        sub = int(f[4:8])
        if sub not in qc_pass:
            continue
        df = pd.read_csv(os.path.join(SUBJ_DIR, f))
        df["subject"] = sub
        frames.append(df)
    pop = pd.concat(frames, ignore_index=True)
    mat = pop.pivot(index="subject", columns="node", values="cis")
    deg = pop.pivot(index="subject", columns="node", values="degree")
    stre = pop.pivot(index="subject", columns="node", values="strength")
    # Unname the column axis: pandas >= 2.x raises "cannot insert node, already
    # exists" in main()'s top-10 reset_index() when the pivot carries the
    # column name 'node' into the transposed summary index (verified on this
    # stack 2026-09-24). Label-only change; no statistic is affected.
    for d in (mat, deg, stre):
        d.columns.name = None
    return mat.sort_index(), deg.sort_index(), stre.sort_index(), qc_pass


def stouffer_table(mat, null_mats):
    """Per-node one-sided empirical p per subject, Stouffer-combined."""
    subjects = mat.index.values
    nodes = mat.columns.values
    n_nodes = len(nodes)
    z_sum = np.zeros(n_nodes)
    used = 0
    for sub in subjects:
        npz = os.path.join(A_DIR, f"sub-{int(sub):04d}_nulls.npz")
        if not os.path.exists(npz):
            continue
        with np.load(npz) as z:
            nulls = z["null_cis"]  # (100, n_nodes)
        obs = mat.loc[sub].values
        # empirical one-sided p per node with add-one correction
        p = (nulls >= obs[None, :]).sum(axis=0)
        p = (p + 1.0) / (N_NULLS + 1.0)
        zj = norm.isf(p)  # Phi^{-1}(1-p)
        z_sum += zj
        used += 1
    z_comb = z_sum / np.sqrt(used)
    p_comb = norm.sf(z_comb)
    # Benjamini-Hochberg
    n = len(p_comb)
    order = np.argsort(p_comb)
    ranked = p_comb[order] * n / np.arange(1, n + 1)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    q = np.empty(n)
    q[order] = np.clip(ranked, 0, 1)
    return pd.DataFrame({"node": nodes, "stouffer_z": z_comb,
                         "p_one_sided": p_comb, "q_bh": q,
                         "subjects_with_nulls": used})


def degree_matched_pools(mean_deg, top_nodes, rel=0.10, k_nearest=50):
    """Fly E14 template: peer pool within +-10% degree; nearest-50 fallback."""
    pools = {}
    order = top_nodes[np.argsort(-mean_deg[top_nodes])]
    used = set()
    for node in order:
        lo, hi = mean_deg[node] * (1 - rel), mean_deg[node] * (1 + rel)
        pool = [j for j in range(len(mean_deg))
                if j != node and lo <= mean_deg[j] <= hi and j not in used]
        mtype = "pm10"
        if not pool:
            cand = [j for j in range(len(mean_deg))
                    if j != node and j not in used]
            pool = sorted(cand, key=lambda j: abs(mean_deg[j] - mean_deg[node])
                          )[:k_nearest]
            mtype = "nearest50"
        pools[node] = {"pool": pool, "type": mtype}
        used.add(node)  # do not reuse a top node as its own peer
    return pools


def system_enrichment(mat, n_perms=N_PERM):
    labels = pd.read_csv(os.path.join(BASE, "00_MANIFEST", "manifests",
                                      "atlas_4S456_system_labels.csv"))
    sys_arr = labels.system.values
    n_nodes = len(sys_arr)
    mean_cis = mat.mean(axis=0).values
    mean_deg = mat.columns.map(lambda c: None)  # placeholder; degree below
    # mean degree per node across subjects (from subject files)
    deg_mean = pd.read_csv(os.path.join(SUBJ_DIR,
                                        f"sub-{mat.index[0]:04d}.csv"))
    degs = []
    for sub in mat.index:
        d = pd.read_csv(os.path.join(SUBJ_DIR, f"sub-{sub:04d}.csv"))
        degs.append(d.degree.values)
    mean_deg = np.mean(np.array(degs), axis=0)

    results = {"K": {}}
    rng = np.random.default_rng(SUBJECT_SEED)
    for K in (25, 50, 100):
        top = np.argsort(-mean_cis)[:K]
        row = {"K": K, "observed": {}}
        for S in SYSTEMS:
            row["observed"][S] = int((sys_arr[top] == S).sum())
        # control A: node-label shuffle (tested universe)
        expA = {S: [] for S in SYSTEMS}
        for _ in range(n_perms):
            perm = rng.permutation(n_nodes)
            fake_top = perm[:K]
            for S in SYSTEMS:
                expA[S].append(int((sys_arr[fake_top] == S).sum()))
        # control B: degree-matched peer pools, resample one peer per slot
        pools = degree_matched_pools(mean_deg, top)
        expB = {S: [] for S in SYSTEMS}
        pool_arr = [np.array(pools[t]["pool"]) for t in top]
        for _ in range(n_perms):
            picks = [pool_arr[k][rng.integers(len(pool_arr[k]))]
                     for k in range(len(pool_arr))]
            for S in SYSTEMS:
                expB[S].append(int((sys_arr[picks] == S).sum()))
        sysres = {}
        for S in SYSTEMS:
            obs = row["observed"][S]
            eA = np.array(expA[S]); eB = np.array(expB[S])
            if eA.std() == 0 or eB.std() == 0:
                continue
            zA = (obs - eA.mean()) / eA.std()
            zB = (obs - eB.mean()) / eB.std()
            pA = (float((eA >= obs).sum()) + 1.0) / (n_perms + 1.0)
            pB = (float((eB >= obs).sum()) + 1.0) / (n_perms + 1.0)
            sysres[S] = {
                "observed": obs,
                "expected_A": float(eA.mean()), "z_A": float(zA), "p_A": pA,
                "expected_B": float(eB.mean()), "z_B": float(zB), "p_B": pB,
                "enrichment_A": obs / max(eA.mean(), 1e-9),
                "enrichment_B": obs / max(eB.mean(), 1e-9),
                "n_top_system": obs,
            }
        row["systems"] = sysres
        row["match_types"] = {int(t): pools[t]["type"] for t in top
                              if pools[t]["type"] != "pm10"}
        results["K"][K] = row
    return results


def rank_stability(mat, n_splits=100):
    rng = np.random.default_rng(SUBJECT_SEED)
    subs = mat.index.values
    n = len(subs)
    half = n // 2
    rs = []
    mean_by_sub = mat.values
    for _ in range(n_splits):
        perm = rng.permutation(n)
        a = mean_by_sub[perm[:half]].mean(axis=0)
        b = mean_by_sub[perm[half:2 * half]].mean(axis=0)
        r, _ = spearmanr(a, b)
        rs.append(r)
    return {"median_spearman": float(np.median(rs)),
            "iqr": [float(np.percentile(rs, 25)),
                    float(np.percentile(rs, 75))], "n_splits": n_splits}


def battery_b_summary():
    files = [f for f in sorted(os.listdir(B_DIR))
             if f.endswith("_battery_b.csv")]
    if not files:
        return {"status": "battery_b not run yet"}
    df = pd.concat([pd.read_csv(os.path.join(B_DIR, f)) for f in files],
                   ignore_index=True)
    sign = binomtest(int((df.z_vs_null > 0).sum()), len(df), 0.5)
    return {
        "n_subjects": int(len(df)),
        "median_z_vs_null": float(df.z_vs_null.median()),
        "iqr_z": [float(df.z_vs_null.quantile(0.25)),
                  float(df.z_vs_null.quantile(0.75))],
        "frac_emp_p_lt_05": float((df.emp_p_ge < 0.05).mean()),
        "frac_obs_above_null_median": float((df.z_vs_null > 0).mean()),
        "sign_test_p": float(sign.pvalue),
        "null_source_counts": df.null_source.value_counts().to_dict(),
    }


def degree_strength_association(mat, deg, stre):
    rd, rs_, rn = [], [], []
    for sub in mat.index:
        c = mat.loc[sub].values
        r1 = spearmanr(c, deg.loc[sub].values).statistic
        r2 = spearmanr(c, stre.loc[sub].values).statistic
        r3 = spearmanr(c, np.arange(len(c))).statistic  # sanity ~0
        rd.append(r1); rs_.append(r2); rn.append(r3)
    return {"spearman_cis_degree_median": float(np.median(rd)),
            "spearman_cis_degree_iqr": [float(np.percentile(rd, 25)),
                                        float(np.percentile(rd, 75))],
            "spearman_cis_strength_median": float(np.median(rs_)),
            "spearman_node_order_median": float(np.median(rn)),
            "n_subjects": len(rd)}


def main():
    t0 = time.time()
    mat, deg, stre, qc_pass = load_observed()
    print(f"[E05] observed: {mat.shape[0]} subjects x {mat.shape[1]} nodes",
          flush=True)

    out = {}
    st = stouffer_table(mat, None)
    st.to_csv(os.path.join(BASE, "09_TABLES", "table_07_null_results.csv"),
              index=False)
    out["per_node_null"] = {
        "n_q_nodes_fdr05": int((st.q_bh < 0.05).sum()),
        "nodes_fdr05": st.loc[st.q_bh < 0.05, "node"].tolist()[:50],
        "min_p": float(st.p_one_sided.min()),
        "max_z": float(st.stouffer_z.max()),
        "max_z_node": int(st.loc[st.stouffer_z.idxmax(), "node"]),
        "subjects_with_nulls": int(st.subjects_with_nulls.iloc[0]),
    }
    print("[E05] per-node null table done", flush=True)

    out["system_enrichment"] = system_enrichment(mat)
    print("[E05] system enrichment done", flush=True)

    out["battery_b"] = battery_b_summary()
    out["rank_stability"] = rank_stability(mat)
    out["degree_strength"] = degree_strength_association(mat, deg, stre)

    # population summary table
    g = mat.agg(["mean", "median", "std"]).T
    g.columns = ["cis_mean", "cis_median", "cis_sd"]
    g["node"] = g.index.astype(int)
    top = mat.rank(axis=1, ascending=False)
    g["mean_rank"] = top.mean(axis=0).values
    g["top50_rate"] = (top <= 50).mean(axis=0).values
    g.sort_values("cis_mean", ascending=False).to_csv(
        os.path.join(BASE, "09_TABLES", "table_population_cis_summary.csv"),
        index=False)
    out["top10_by_mean_cis"] = g.sort_values(
        "cis_mean", ascending=False).head(10).reset_index()[
        ["node", "cis_mean", "cis_median", "top50_rate"]].to_dict("records")

    with open(os.path.join(BASE, "04_CIS", "e05_statistics.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(f"[E05] DONE in {(time.time()-t0)/60:.1f} min")
    print(json.dumps(out.get("per_node_null"), indent=1))


if __name__ == "__main__":
    main()
