"""PARTS B, C, D, E, F, I - PLS-SEM measurement & structural model, bootstrap,
mediation, model quality (R2/Q2/f2/PLSpredict), IPMA. Saves tables to analysis/tables."""
import numpy as np
import pandas as pd
from numpy.random import default_rng
import common as C
from plssem import PLSSEM

RNG = default_rng(20240625)
B = 5000

df = C.load_raw()
N = len(df)
model = PLSSEM(C.CONSTRUCTS, C.STRUCTURAL_PATHS).fit(df)

# ---------------- PART B: measurement model ----------------
# Outer loadings + indicator reliability + communality
rows = []
for lv in model.lv_names:
    for k, ind in enumerate(C.CONSTRUCTS[lv]):
        l = model.loadings[lv][k]
        rows.append([lv, ind, model.outer_weights[lv][k], l, l ** 2, 1 - l ** 2])
load_tbl = pd.DataFrame(rows, columns=["Construct", "Indicator", "OuterWeight",
                                       "OuterLoading", "IndicatorReliability(Communality)", "Redundancy(1-L^2)"])
load_tbl.round(4).to_csv(C.TBL + "/B_loadings_weights.csv", index=False)

model.cross_loadings.round(4).to_csv(C.TBL + "/B_cross_loadings.csv")
rel = model.reliability()
rel.round(4).to_csv(C.TBL + "/B_reliability_validity.csv")
model.fornell_larcker().round(4).to_csv(C.TBL + "/B_fornell_larcker.csv")
model.htmt().round(4).to_csv(C.TBL + "/B_htmt.csv")
model.full_collinearity_vif().round(4).to_frame().to_csv(C.TBL + "/B_full_collinearity_vif.csv")
fit = model.model_fit()
pd.Series(fit).round(4).to_csv(C.TBL + "/B_model_fit.csv")

# inner VIF
ivif = model.inner_vif()
ivrows = [[lv, p, v] for lv, d in ivif.items() for p, v in d.items()]
pd.DataFrame(ivrows, columns=["Outcome", "Predictor", "InnerVIF"]).round(4).to_csv(C.TBL + "/C_inner_vif.csv", index=False)

# ---------------- Bootstrap ----------------
# We collect: structural paths, outer loadings, indirect effects
path_keys = [(a, b) for (a, b) in C.STRUCTURAL_PATHS]
boot_paths = {k: np.empty(B) for k in path_keys}
boot_load = {(lv, ind): np.empty(B) for lv in model.lv_names for ind in C.CONSTRUCTS[lv]}
# indirect effects via BSAT
med_specs = {"UE->BSAT->BSUC": ("UE", "BSAT", "BSUC"), "UX->BSAT->BSUC": ("UX", "BSAT", "BSUC")}
boot_ind = {m: np.empty(B) for m in med_specs}
boot_direct = {"UE->BSUC": np.empty(B), "UX->BSUC": np.empty(B)}

idx = np.arange(N)
for b in range(B):
    s = df.iloc[RNG.choice(idx, N, replace=True)]
    try:
        mb = PLSSEM(C.CONSTRUCTS, C.STRUCTURAL_PATHS).fit(s)
    except Exception:
        for k in path_keys:
            boot_paths[k][b] = np.nan
        continue
    for (a, bb) in path_keys:
        boot_paths[(a, bb)][b] = mb.path_coef[bb].get(a, np.nan)
    for lv in mb.lv_names:
        for k, ind in enumerate(C.CONSTRUCTS[lv]):
            boot_load[(lv, ind)][b] = abs(mb.loadings[lv][k])
    for m, (x, med, y) in med_specs.items():
        a_coef = mb.path_coef[med].get(x, np.nan)
        b_coef = mb.path_coef[y].get(med, np.nan)
        boot_ind[m][b] = a_coef * b_coef
    boot_direct["UE->BSUC"][b] = mb.path_coef["BSUC"].get("UE", np.nan)
    boot_direct["UX->BSUC"][b] = mb.path_coef["BSUC"].get("UX", np.nan)


def ci_perc(arr, lo=2.5, hi=97.5):
    arr = arr[~np.isnan(arr)]
    return np.percentile(arr, lo), np.percentile(arr, hi)


def boot_summary(orig, arr):
    arr = arr[~np.isnan(arr)]
    se = arr.std(ddof=1)
    t = orig / se if se > 0 else np.nan
    # two-sided p from bootstrap t (normal approx)
    from scipy import stats as st
    p = 2 * (1 - st.norm.cdf(abs(t))) if se > 0 else np.nan
    lo, hi = np.percentile(arr, [2.5, 97.5])
    return se, t, p, lo, hi


# ---------------- PART C / I: structural paths ----------------
struct_rows = []
for (a, bb) in path_keys:
    orig = model.path_coef[bb][a]
    se, t, p, lo, hi = boot_summary(orig, boot_paths[(a, bb)])
    sig = (lo > 0) or (hi < 0)
    struct_rows.append([f"{a} -> {bb}", orig, se, t, p, lo, hi,
                        "Supported" if sig and p < 0.05 else "Not supported"])
struct = pd.DataFrame(struct_rows, columns=["Path", "Beta", "SE", "t", "p", "CI2.5", "CI97.5", "Decision"])
struct.round(4).to_csv(C.TBL + "/C_structural_paths.csv", index=False)

# bootstrapped loadings significance
lrows = []
for lv in model.lv_names:
    for k, ind in enumerate(C.CONSTRUCTS[lv]):
        orig = abs(model.loadings[lv][k])
        se, t, p, lo, hi = boot_summary(orig, boot_load[(lv, ind)])
        lrows.append([lv, ind, orig, se, t, p, lo, hi])
pd.DataFrame(lrows, columns=["Construct", "Indicator", "Loading", "SE", "t", "p", "CI2.5", "CI97.5"]).round(4).to_csv(C.TBL + "/B_loading_significance.csv", index=False)

# ---------------- PART D: mediation ----------------
med_rows = []
for m, (x, med, y) in med_specs.items():
    a_coef = model.path_coef[med][x]
    b_coef = model.path_coef[y][med]
    ind = a_coef * b_coef
    direct = model.path_coef[y][x]
    total = ind + direct
    se, t, p, lo, hi = boot_summary(ind, boot_ind[m])
    vaf = ind / total if total != 0 else np.nan
    sig_ind = (lo > 0) or (hi < 0)
    # mediation type (Zhao et al. 2010)
    if not sig_ind:
        mtype = "No mediation (no indirect effect)"
    else:
        # direct significance
        d_se, d_t, d_p, d_lo, d_hi = boot_summary(direct, boot_direct[f"{x}->{y}"])
        d_sig = (d_lo > 0) or (d_hi < 0)
        if d_sig:
            mtype = "Complementary (partial)" if ind * direct > 0 else "Competitive (partial)"
        else:
            mtype = "Indirect-only (full mediation)"
    med_rows.append([m, a_coef, b_coef, ind, direct, total, se, lo, hi,
                     (vaf if abs(vaf) < 10 else np.nan), mtype])
med = pd.DataFrame(med_rows, columns=["Mediation", "a(X->M)", "b(M->Y)", "Indirect", "Direct",
                                      "Total", "SE_indirect", "CI2.5", "CI97.5", "VAF", "Type"])
med.round(4).to_csv(C.TBL + "/D_mediation.csv", index=False)

# ---------------- PART E: R2, f2, Q2, PLSpredict ----------------
r2tbl = pd.DataFrame({
    "Construct": list(model.r2.keys()),
    "R2": list(model.r2.values()),
    "R2_adj": [model.r2_adj[k] for k in model.r2],
}).round(4)
r2tbl.to_csv(C.TBL + "/E_r2.csv", index=False)

f2 = model.f_squared()
f2tbl = pd.DataFrame([[f"{p}", o, v] for (p, o), v in f2.items()],
                     columns=["Predictor", "Outcome", "f2"]).round(4)
f2tbl.to_csv(C.TBL + "/E_f2.csv", index=False)

# ---- Q2 via blindfolding (cross-validated redundancy), omission distance d=7 ----
def blindfold_q2(model, df, d=7):
    Xs = model.Xs
    Ncase = Xs.shape[0]
    out = {}
    for lv in model.lv_names:
        if not model.pred[lv]:
            continue
        cols = model.cols[lv]
        block = Xs[:, cols]
        preds = model.pred[lv]
        Xp = model.scores_[preds].values
        SSO = 0.0; SSE = 0.0
        # cross-validated redundancy: predict each indicator using structural prediction of LV
        # build predicted LV from predecessors (OLS) leaving out blindfold groups
        for g in range(d):
            omit = np.arange(Ncase) % d == g
            keep = ~omit
            # structural model on kept rows
            Xd = np.column_stack([np.ones(keep.sum()), Xp[keep]])
            ylv = model.scores_[lv].values[keep]
            beta, *_ = np.linalg.lstsq(Xd, ylv, rcond=None)
            lv_pred_omit = np.column_stack([np.ones(omit.sum()), Xp[omit]]) @ beta
            for kk, ci in enumerate(cols):
                l = model.loadings[lv][kk]
                # mean of indicator on kept rows
                mean_keep = block[keep, kk].mean()
                pred_ind = mean_keep + l * lv_pred_omit  # redundancy prediction
                actual = block[omit, kk]
                SSE += ((actual - pred_ind) ** 2).sum()
                SSO += ((actual - mean_keep) ** 2).sum()
        out[lv] = 1 - SSE / SSO
    return out

q2 = blindfold_q2(model, df)
pd.Series(q2, name="Q2_redundancy").round(4).to_csv(C.TBL + "/E_q2.csv")

# ---- PLSpredict: 10-fold prediction of BSUC indicators; compare PLS vs LM benchmark ----
from sklearn.model_selection import KFold
def plspredict(model, df, target="BSUC", k=10):
    inds = C.CONSTRUCTS[target]
    exo = ["UE", "UX"]  # antecedents driving the model
    Xall = df[C.INDICATORS].astype(float).values
    kf = KFold(n_splits=k, shuffle=True, random_state=7)
    res = {ind: {"pls_e": [], "lm_e": [], "y": []} for ind in inds}
    allinds = C.INDICATORS
    exo_cols = [allinds.index(i) for lv in exo for i in C.CONSTRUCTS[lv]]
    for tr, te in kf.split(Xall):
        mtr = PLSSEM(C.CONSTRUCTS, C.STRUCTURAL_PATHS).fit(df.iloc[tr])
        # PLS prediction: exo composite scores -> endo -> indicators
        # compute exo composite scores on test using training weights & standardisation
        def comp_score(lv, rows):
            cols = mtr.cols[lv]
            xs = (Xall[rows][:, cols] - mtr.Xmean[cols]) / mtr.Xstd[cols]
            return xs @ mtr.outer_weights[lv]
        # train structural for target via two-step: UE,UX->BSAT->BSUC and direct
        sc_tr = mtr.scores_
        # predict BSUC score from UE,UX,BSAT path model using training betas
        # use reduced-form: BSUC ~ UE,UX,BSAT
        ytr = sc_tr["BSUC"].values
        Ztr = np.column_stack([np.ones(len(tr)), sc_tr[["UE","UX","BSAT"]].values])
        beta, *_ = np.linalg.lstsq(Ztr, ytr, rcond=None)
        ue_te = comp_score("UE", te); ux_te = comp_score("UX", te)
        # BSAT predicted from UE,UX
        bsat_tr = sc_tr["BSAT"].values
        Zb = np.column_stack([np.ones(len(tr)), sc_tr[["UE","UX"]].values])
        betab, *_ = np.linalg.lstsq(Zb, bsat_tr, rcond=None)
        bsat_te = np.column_stack([np.ones(len(te)), ue_te, ux_te]) @ betab
        bsuc_score_te = np.column_stack([np.ones(len(te)), ue_te, ux_te, bsat_te]) @ beta
        for ind in inds:
            kk = C.CONSTRUCTS[target].index(ind)
            l = mtr.loadings[target][kk]
            mean_tr = df.iloc[tr][ind].mean()
            pred = mean_tr + l * bsuc_score_te * df.iloc[tr][ind].std(ddof=1)
            actual = df.iloc[te][ind].values
            res[ind]["pls_e"].extend(actual - pred)
            res[ind]["y"].extend(actual)
            # LM benchmark: predict indicator from all exogenous indicators
            from numpy.linalg import lstsq
            Xtr = np.column_stack([np.ones(len(tr)), Xall[tr][:, exo_cols]])
            ytr_i = df.iloc[tr][ind].values
            blm, *_ = lstsq(Xtr, ytr_i, rcond=None)
            Xte = np.column_stack([np.ones(len(te)), Xall[te][:, exo_cols]])
            predlm = Xte @ blm
            res[ind]["lm_e"].extend(actual - predlm)
    rows = []
    for ind in inds:
        e = np.array(res[ind]["pls_e"]); elm = np.array(res[ind]["lm_e"]); y = np.array(res[ind]["y"])
        rmse = np.sqrt((e**2).mean()); mae = np.abs(e).mean()
        mape = np.abs(e / np.where(y==0, np.nan, y)).mean()*100
        rmse_lm = np.sqrt((elm**2).mean()); mae_lm = np.abs(elm).mean()
        rows.append([ind, rmse, mae, mape, rmse_lm, mae_lm, rmse - rmse_lm])
    return pd.DataFrame(rows, columns=["Indicator","PLS_RMSE","PLS_MAE","PLS_MAPE","LM_RMSE","LM_MAE","RMSE_diff(PLS-LM)"])

pp = plspredict(model, df)
pp.round(4).to_csv(C.TBL + "/E_plspredict.csv", index=False)

# ---------------- PART F: IPMA ----------------
# Importance = total effect on BSUC; Performance = rescaled mean (0-100)
def ipma(model, df, target="BSUC"):
    # total effects on target
    pc = model.path_coef
    total = {}
    # direct
    for x in ["UE", "UX", "BSAT"]:
        direct = pc[target].get(x, 0.0)
        indirect = 0.0
        if x in ("UE", "UX"):
            indirect = pc["BSAT"].get(x, 0.0) * pc[target].get("BSAT", 0.0)
        total[x] = direct + indirect
    # performance: mean of construct rescaled to 0-100 on 1-7 scale
    comp = C.composites(df)
    perf = {x: (comp[x].mean() - 1) / (7 - 1) * 100 for x in ["UE", "UX", "BSAT"]}
    rows = [[x, total[x], perf[x]] for x in ["UE", "UX", "BSAT"]]
    return pd.DataFrame(rows, columns=["Construct", "Importance(TotalEffect)", "Performance(0-100)"])

ipma_tbl = ipma(model, df)
ipma_tbl.round(4).to_csv(C.TBL + "/F_ipma.csv", index=False)

# Save composite scores & residuals for supplementary
C.composites(df).round(4).to_csv(C.TBL + "/P_composite_scores.csv", index=False)
resid_df = pd.DataFrame({lv: model.residuals[lv] for lv in model.residuals})
resid_df.round(4).to_csv(C.TBL + "/P_structural_residuals.csv", index=False)

# Persist bootstrap distributions of paths (subset) for figures
np.savez(C.TBL + "/_boot_paths.npz", **{f"{a}__{b}": boot_paths[(a, b)] for (a, b) in path_keys},
         **{f"ind__{m}": boot_ind[m] for m in med_specs})

print("== PLS analysis complete ==")
print("\nStructural paths:\n", struct.round(4).to_string(index=False))
print("\nMediation:\n", med.round(4).to_string(index=False))
print("\nR2:\n", r2tbl.to_string(index=False))
print("\nQ2:", {k: round(v, 4) for k, v in q2.items()})
print("\nPLSpredict:\n", pp.round(4).to_string(index=False))
print("\nIPMA:\n", ipma_tbl.round(3).to_string(index=False))
