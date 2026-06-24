"""
03b_plspredict.py
Out-of-sample predictive validity (PLSpredict; Shmueli et al., 2019).
10-fold cross-validation: for the key target construct (BSUC) indicators, compare
PLS-SEM prediction error against a naive linear-model (LM) benchmark.
Reports Q2_predict, RMSE and MAE per indicator and the PLS-vs-LM comparison.
"""
import os
import json
import numpy as np
import pandas as pd
from pls_engine import PLSSEM

OUT = "analysis/outputs"
os.makedirs(OUT, exist_ok=True)

df = pd.read_excel("Responses.xlsx", sheet_name="responses collected")
df.columns = [c.strip() for c in df.columns]

BLOCKS = {
    "UE":   ["UE1", "UE2", "UE3", "UE4", "UE5"],
    "UX":   ["UX1", "UX2", "UX3", "UX4", "UX5"],
    "BSAT": ["BSAT1", "BSAT2", "BSAT3", "BSAT4"],
    "BSUC": ["BSUC1", "BSUC2", "BSUC3", "BSUC4"],
}
PATHS = {"BSAT": ["UE", "UX"], "BSUC": ["UE", "UX", "BSAT"]}
TARGET = "BSUC"
exo_items = BLOCKS["UE"] + BLOCKS["UX"]   # exogenous indicators as LM predictors
target_items = BLOCKS[TARGET]

rng = np.random.default_rng(2024)
n = len(df)
k = 10
folds = np.array_split(rng.permutation(n), k)

pls_err = {it: [] for it in target_items}
lm_err = {it: [] for it in target_items}

for f in range(k):
    test_idx = folds[f]
    train_idx = np.setdiff1d(np.arange(n), test_idx)
    train = df.iloc[train_idx].reset_index(drop=True)
    test = df.iloc[test_idx].reset_index(drop=True)

    # --- PLS prediction (Shmueli): estimate on train, score exo from test
    m = PLSSEM(train, BLOCKS, PATHS, max_iter=300, tol=1e-7)
    # standardization parameters from training
    tr_items = [i for b in BLOCKS.values() for i in b]
    mu = train[tr_items].mean()
    sd = train[tr_items].std(ddof=1)

    def exo_score(frame, construct):
        items = BLOCKS[construct]
        z = (frame[items] - mu[items]) / sd[items]
        w = m.weights[construct]
        s = z.values @ w
        return (s - s.mean()) / s.std(ddof=1) if s.std(ddof=1) > 0 else s

    # predict mediator then target construct scores using train path coeffs
    ue_s = exo_score(test, "UE")
    ux_s = exo_score(test, "UX")
    bsat_pred = m.path_coef["BSAT"]["UE"] * ue_s + m.path_coef["BSAT"]["UX"] * ux_s
    bsuc_pred = (m.path_coef["BSUC"]["UE"] * ue_s +
                 m.path_coef["BSUC"]["UX"] * ux_s +
                 m.path_coef["BSUC"]["BSAT"] * bsat_pred)
    # map predicted construct score to each indicator: mu + loading*sd*score
    for it in target_items:
        loading = m.loadings[it]
        pred = mu[it] + loading * sd[it] * bsuc_pred
        pls_err[it].extend((test[it].values - pred).tolist())

    # --- LM benchmark: regress each target indicator on exo indicators (train)
    Xtr = np.column_stack([np.ones(len(train))] +
                          [(train[c] - mu[c]) / sd[c] for c in exo_items])
    Xte = np.column_stack([np.ones(len(test))] +
                          [(test[c] - mu[c]) / sd[c] for c in exo_items])
    for it in target_items:
        beta, *_ = np.linalg.lstsq(Xtr, train[it].values, rcond=None)
        pred = Xte @ beta
        lm_err[it].extend((test[it].values - pred).tolist())

rows = []
for it in target_items:
    pe = np.array(pls_err[it])
    le = np.array(lm_err[it])
    obs = df[it].values
    rmse_pls = np.sqrt(np.mean(pe ** 2))
    mae_pls = np.mean(np.abs(pe))
    rmse_lm = np.sqrt(np.mean(le ** 2))
    # Q2_predict = 1 - SSE_pls / SS_mean(of full sample)
    sse = np.sum(pe ** 2)
    sst = np.sum((obs - obs.mean()) ** 2)
    q2_pred = 1 - sse / sst
    rows.append({
        "Indicator": it,
        "Q2_predict": q2_pred,
        "RMSE_PLS": rmse_pls,
        "MAE_PLS": mae_pls,
        "RMSE_LM": rmse_lm,
        "PLS<LM (RMSE)": "Yes" if rmse_pls < rmse_lm else "No",
    })
res = pd.DataFrame(rows)
res.to_csv(f"{OUT}/T13_plspredict.csv", index=False)
print("=== PLSpredict (10-fold CV) for", TARGET, "indicators ===")
print(res.round(4).to_string(index=False))
n_better = (res["PLS<LM (RMSE)"] == "Yes").sum()
all_q2pos = (res["Q2_predict"] > 0).all()
print(f"\nQ2_predict > 0 for all indicators: {all_q2pos}")
print(f"PLS RMSE < LM RMSE for {n_better}/{len(res)} indicators")
with open(f"{OUT}/plspredict_summary.json", "w") as fjson:
    json.dump({"all_q2_positive": bool(all_q2pos),
               "pls_better_than_lm": int(n_better),
               "n_indicators": int(len(res))}, fjson, indent=2)
