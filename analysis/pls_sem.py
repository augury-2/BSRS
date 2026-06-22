"""
PLS-SEM analysis for the BSRS metaverse / avatar-mediated IS study.

Model (SDT-based):
    UE  ->  BSAT, BSUC
    UX  ->  BSAT, BSUC
    BSAT -> BSUC   (mediator)

Implements the PLS-PM algorithm (Mode A / reflective, path-weighting scheme)
from scratch in numpy, plus nonparametric bootstrapping for significance.
All measurement- and structural-model quality criteria are reported.

Outputs are written to analysis/outputs/ as CSV + a JSON summary.
"""

import json
import os
import numpy as np
import pandas as pd

RNG = np.random.default_rng(20240622)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
os.makedirs(OUT, exist_ok=True)
DATA = os.path.join(HERE, "..", "Original collected reponses.xlsx")

# ---------------------------------------------------------------- model spec
BLOCKS = {
    "UE":   ["UE1", "UE2", "UE3", "UE4", "UE5"],
    "UX":   ["UX1", "UX2", "UX3", "UX4", "UX5"],
    "BSAT": ["BSAT1", "BSAT2", "BSAT3", "BSAT4"],
    "BSUC": ["BSUC1", "BSUC2", "BSUC3", "BSUC4"],
}
LVS = list(BLOCKS.keys())

# structural paths: predictor -> outcome
PATHS = [
    ("UE", "BSAT"), ("UX", "BSAT"),
    ("UE", "BSUC"), ("UX", "BSUC"), ("BSAT", "BSUC"),
]
PREDECESSORS = {lv: [p for p, o in PATHS if o == lv] for lv in LVS}

# adjacency (symmetric) for inner weighting
ADJ = {lv: set() for lv in LVS}
for a, b in PATHS:
    ADJ[a].add(b)
    ADJ[b].add(a)


def standardize(X):
    return (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)


def pls_algorithm(data, max_iter=500, tol=1e-7):
    """Run the basic PLS-PM algorithm. Returns weights, scores, loadings."""
    Z = {lv: standardize(data[BLOCKS[lv]].values.astype(float)) for lv in LVS}
    # init outer weights = 1, get initial scores
    w = {lv: np.ones(Z[lv].shape[1]) for lv in LVS}

    def scores_from_w(w):
        S = {}
        for lv in LVS:
            s = Z[lv] @ w[lv]
            s = (s - s.mean()) / s.std(ddof=1)
            S[lv] = s
        return S

    S = scores_from_w(w)
    for _ in range(max_iter):
        # inner approximation (path weighting scheme)
        Sinner = {}
        for lv in LVS:
            agg = np.zeros(len(data))
            for other in ADJ[lv]:
                if other in PREDECESSORS[lv]:        # other is predecessor -> regression coef
                    e = np.corrcoef(S[other], S[lv])[0, 1]
                    agg += e * S[other]
                else:                                 # lv predicts other -> use correlation
                    e = np.corrcoef(S[other], S[lv])[0, 1]
                    agg += e * S[other]
            Sinner[lv] = (agg - agg.mean()) / agg.std(ddof=1)
        # outer weights (Mode A: covariance of indicators with inner score)
        w_new = {}
        for lv in LVS:
            wv = Z[lv].T @ Sinner[lv] / len(data)
            w_new[lv] = wv
        S_new = scores_from_w(w_new)
        diff = sum(np.sum(np.abs(np.abs(w_new[lv]) - np.abs(w[lv]))) for lv in LVS)
        w, S = w_new, S_new
        if diff < tol:
            break

    # loadings = correlation of indicator with its own LV score
    loadings = {}
    for lv in LVS:
        loadings[lv] = np.array([np.corrcoef(Z[lv][:, j], S[lv])[0, 1]
                                 for j in range(Z[lv].shape[1])])
    return w, S, loadings


def structural_coeffs(S):
    """OLS path coefficients + R2 for each endogenous LV."""
    coeffs, r2 = {}, {}
    for lv in LVS:
        preds = PREDECESSORS[lv]
        if not preds:
            continue
        X = np.column_stack([S[p] for p in preds])
        y = S[lv]
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)  # standardized -> no intercept
        yhat = X @ beta
        ss_res = np.sum((y - yhat) ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        coeffs[lv] = dict(zip(preds, beta))
        r2[lv] = 1 - ss_res / ss_tot
    return coeffs, r2


def main():
    df = pd.read_excel(DATA)
    n = len(df)

    # ---- run PLS
    w, S, loadings = pls_algorithm(df)
    coeffs, r2 = structural_coeffs(S)

    # ---- measurement model quality
    mm_rows = []
    rel_rows = []
    for lv in LVS:
        L = loadings[lv]
        ave = np.mean(L ** 2)
        # composite reliability (rho_c)
        sl = np.sum(L)
        se = np.sum(1 - L ** 2)
        cr = (sl ** 2) / (sl ** 2 + se)
        # cronbach alpha
        block = df[BLOCKS[lv]]
        k = block.shape[1]
        alpha = (k / (k - 1)) * (1 - block.var(ddof=1).sum() / block.sum(axis=1).var(ddof=1))
        rel_rows.append(dict(Construct=lv, Items=k, Cronbach_alpha=alpha,
                             Composite_Reliability=cr, AVE=ave))
        for it, ld in zip(BLOCKS[lv], L):
            mm_rows.append(dict(Construct=lv, Indicator=it, Loading=ld))

    rel_df = pd.DataFrame(rel_rows)
    mm_df = pd.DataFrame(mm_rows)

    # ---- LV correlations, Fornell-Larcker, HTMT
    Smat = pd.DataFrame({lv: S[lv] for lv in LVS})
    lv_corr = Smat.corr()

    fl = lv_corr.copy()
    for lv in LVS:
        fl.loc[lv, lv] = np.sqrt(rel_df.set_index("Construct").loc[lv, "AVE"])

    # HTMT
    def htmt(a, b):
        ia, ib = BLOCKS[a], BLOCKS[b]
        cross = df[ia + ib].corr().loc[ia, ib].values
        mono_a = df[ia].corr().values[np.triu_indices(len(ia), 1)]
        mono_b = df[ib].corr().values[np.triu_indices(len(ib), 1)]
        return np.abs(cross).mean() / np.sqrt(np.abs(mono_a).mean() * np.abs(mono_b).mean())

    htmt_df = pd.DataFrame(index=LVS, columns=LVS, dtype=float)
    for i, a in enumerate(LVS):
        for j, b in enumerate(LVS):
            if i > j:
                htmt_df.loc[a, b] = htmt(a, b)

    # ---- f2 effect sizes (for BSUC and BSAT)
    f2_rows = []
    for lv in LVS:
        preds = PREDECESSORS[lv]
        if not preds:
            continue
        full = r2[lv]
        for p in preds:
            others = [x for x in preds if x != p]
            if others:
                X = np.column_stack([S[o] for o in others])
                y = S[lv]
                beta, *_ = np.linalg.lstsq(X, y, rcond=None)
                yhat = X @ beta
                r2_ex = 1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)
            else:
                r2_ex = 0.0
            f2 = (full - r2_ex) / (1 - full) if (1 - full) > 1e-9 else 0.0
            f2_rows.append(dict(Predictor=p, Outcome=lv, f2=f2))
    f2_df = pd.DataFrame(f2_rows)

    # ---- bootstrap path coefficients
    B = 5000
    boot = {f"{a}->{b}": [] for a, b in PATHS}
    idx_all = np.arange(n)
    for _ in range(B):
        samp = RNG.choice(idx_all, size=n, replace=True)
        d = df.iloc[samp].reset_index(drop=True)
        try:
            _, Sb, _ = pls_algorithm(d, max_iter=300)
            cb, _ = structural_coeffs(Sb)
            for a, b in PATHS:
                boot[f"{a}->{b}"].append(cb[b][a])
        except Exception:
            continue

    path_rows = []
    for a, b in PATHS:
        key = f"{a}->{b}"
        arr = np.array(boot[key])
        orig = coeffs[b][a]
        se = arr.std(ddof=1)
        tval = orig / se if se > 0 else 0.0
        # two-tailed p from bootstrap t
        from scipy import stats
        pval = 2 * (1 - stats.t.cdf(abs(tval), df=n - 1))
        ci_lo, ci_hi = np.percentile(arr, [2.5, 97.5])
        path_rows.append(dict(Path=key, Beta=orig, SE=se, t=tval, p=pval,
                              CI_2_5=ci_lo, CI_97_5=ci_hi,
                              Significant=("Yes" if pval < 0.05 else "No")))
    path_df = pd.DataFrame(path_rows)

    # ---- Q2 via blindfolding-style approximation (cross-validated redundancy)
    # Simple CV: predict each endogenous indicator's standardized block score
    q2_rows = []
    for lv in LVS:
        preds = PREDECESSORS[lv]
        if not preds:
            continue
        y = S[lv].copy()
        X = np.column_stack([S[p] for p in preds])
        preds_cv = np.zeros(n)
        for i in range(n):
            mask = np.ones(n, bool); mask[i] = False
            beta, *_ = np.linalg.lstsq(X[mask], y[mask], rcond=None)
            preds_cv[i] = X[i] @ beta
        sse = np.sum((y - preds_cv) ** 2)
        sso = np.sum((y - y.mean()) ** 2)
        q2_rows.append(dict(Construct=lv, Q2=1 - sse / sso))
    q2_df = pd.DataFrame(q2_rows)

    # ---- mediation (indirect effects via bootstrap) UE->BSAT->BSUC, UX->BSAT->BSUC
    med_rows = []
    from scipy import stats
    for x in ["UE", "UX"]:
        a_arr = np.array(boot[f"{x}->BSAT"])
        b_arr = np.array(boot["BSAT->BSUC"])
        m = min(len(a_arr), len(b_arr))
        ind = a_arr[:m] * b_arr[:m]
        orig_ind = coeffs["BSAT"][x] * coeffs["BSUC"]["BSAT"]
        se = ind.std(ddof=1)
        tval = orig_ind / se if se > 0 else 0.0
        pval = 2 * (1 - stats.t.cdf(abs(tval), df=n - 1))
        lo, hi = np.percentile(ind, [2.5, 97.5])
        med_rows.append(dict(Indirect=f"{x}->BSAT->BSUC", Effect=orig_ind, SE=se,
                             t=tval, p=pval, CI_2_5=lo, CI_97_5=hi,
                             Direct=coeffs["BSUC"][x],
                             Significant=("Yes" if pval < 0.05 else "No")))
    med_df = pd.DataFrame(med_rows)

    # ---- save everything
    rel_df.to_csv(os.path.join(OUT, "pls_reliability_validity.csv"), index=False)
    mm_df.to_csv(os.path.join(OUT, "pls_loadings.csv"), index=False)
    lv_corr.to_csv(os.path.join(OUT, "pls_lv_correlations.csv"))
    fl.to_csv(os.path.join(OUT, "pls_fornell_larcker.csv"))
    htmt_df.to_csv(os.path.join(OUT, "pls_htmt.csv"))
    path_df.to_csv(os.path.join(OUT, "pls_structural_paths.csv"), index=False)
    f2_df.to_csv(os.path.join(OUT, "pls_f2.csv"), index=False)
    q2_df.to_csv(os.path.join(OUT, "pls_q2.csv"), index=False)
    med_df.to_csv(os.path.join(OUT, "pls_mediation.csv"), index=False)
    pd.DataFrame([dict(Construct=lv, R2=r2.get(lv, np.nan)) for lv in LVS]
                 ).dropna().to_csv(os.path.join(OUT, "pls_r2.csv"), index=False)
    Smat.to_csv(os.path.join(OUT, "lv_scores.csv"), index=False)

    summary = dict(N=n, R2=r2, bootstrap_samples=B,
                   note="Within-block reliability high; structural paths near zero.")
    with open(os.path.join(OUT, "pls_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=float)

    # console
    pd.set_option("display.width", 160)
    print("=== Reliability & Validity ===\n", rel_df.round(3), "\n")
    print("=== Loadings ===\n", mm_df.round(3).to_string(index=False), "\n")
    print("=== LV correlations ===\n", lv_corr.round(3), "\n")
    print("=== Fornell-Larcker (diag = sqrt(AVE)) ===\n", fl.round(3), "\n")
    print("=== HTMT ===\n", htmt_df.round(3), "\n")
    print("=== R2 ===\n", {k: round(v, 4) for k, v in r2.items()}, "\n")
    print("=== Structural paths (bootstrap) ===\n", path_df.round(4).to_string(index=False), "\n")
    print("=== f2 ===\n", f2_df.round(4).to_string(index=False), "\n")
    print("=== Q2 ===\n", q2_df.round(4).to_string(index=False), "\n")
    print("=== Mediation ===\n", med_df.round(4).to_string(index=False), "\n")


if __name__ == "__main__":
    main()
