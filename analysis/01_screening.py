"""
01_screening.py
Data screening, descriptive statistics, normality, common method bias (Harman),
and exploratory factor analysis to validate the a-priori construct assignment.
BSRS study: 312 responses, 20 items, 7-point Likert.
"""
import os
import json
import numpy as np
import pandas as pd
from scipy import stats
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import (
    calculate_kmo,
    calculate_bartlett_sphericity,
)

OUT = "analysis/outputs"
os.makedirs(OUT, exist_ok=True)

df = pd.read_excel("Responses.xlsx", sheet_name="responses collected")
df.columns = [c.strip() for c in df.columns]

# A-priori construct -> items
CONSTRUCTS = {
    "UE":   ["UE1", "UE2", "UE3", "UE4", "UE5"],
    "UX":   ["UX1", "UX2", "UX3", "UX4", "UX5"],
    "BSAT": ["BSAT1", "BSAT2", "BSAT3", "BSAT4"],
    "BSUC": ["BSUC1", "BSUC2", "BSUC3", "BSUC4"],
    "ATT":  ["ATT_1", "ATT_2"],
}
all_items = [i for v in CONSTRUCTS.values() for i in v]

print("N =", len(df), "| items =", len(all_items))
print("Missing values total:", int(df[all_items].isna().sum().sum()))
print("Value range:", int(df[all_items].min().min()), "-", int(df[all_items].max().max()))

# ---- Descriptive statistics per item ----
desc_rows = []
for it in all_items:
    x = df[it].astype(float)
    desc_rows.append({
        "Item": it,
        "Mean": x.mean(),
        "SD": x.std(ddof=1),
        "Median": x.median(),
        "Min": x.min(),
        "Max": x.max(),
        "Skewness": stats.skew(x, bias=False),
        "Kurtosis": stats.kurtosis(x, fisher=True, bias=False),
        "Missing": int(x.isna().sum()),
    })
desc = pd.DataFrame(desc_rows)
desc.to_csv(f"{OUT}/T1_item_descriptives.csv", index=False)
print("\n--- Item descriptives ---")
print(desc.round(3).to_string(index=False))

# ---- Normality (Shapiro) just to document non-normality justifying PLS ----
norm_rows = []
for it in all_items:
    w, p = stats.shapiro(df[it].astype(float))
    norm_rows.append({"Item": it, "Shapiro_W": w, "p": p})
norm = pd.DataFrame(norm_rows)
norm.to_csv(f"{OUT}/T1b_normality.csv", index=False)
print("\nItems with significant non-normality (p<.05):",
      int((norm["p"] < 0.05).sum()), "/", len(all_items))
print("Max |skew| = %.3f | Max |kurtosis| = %.3f"
      % (desc["Skewness"].abs().max(), desc["Kurtosis"].abs().max()))

# ---- Straight-lining / careless responding check ----
row_sd = df[all_items].std(axis=1, ddof=1)
print("\nStraight-liners (row SD == 0):", int((row_sd == 0).sum()))

# ---- KMO & Bartlett ----
X = df[all_items].astype(float).values
kmo_all, kmo_model = calculate_kmo(X)
chi2, p_bart = calculate_bartlett_sphericity(X)
print("\nKMO (overall) = %.3f" % kmo_model)
print("Bartlett chi2 = %.1f, p = %.3g" % (chi2, p_bart))

# ---- Harman's single factor test ----
fa1 = FactorAnalyzer(n_factors=1, rotation=None, method="principal")
fa1.fit(X)
ev_single, _ = fa1.get_eigenvalues()
# variance explained by 1 unrotated factor
fa_all = FactorAnalyzer(n_factors=len(all_items), rotation=None, method="principal")
fa_all.fit(X)
var = fa_all.get_factor_variance()  # (variance, proportional, cumulative)
harman_first = var[1][0] * 100
print("Harman single-factor variance explained = %.2f%%" % harman_first)

# ---- EFA to validate 5-construct structure ----
fa = FactorAnalyzer(n_factors=5, rotation="promax", method="principal")
fa.fit(X)
loadings = pd.DataFrame(fa.loadings_, index=all_items,
                        columns=[f"F{i+1}" for i in range(5)])
loadings.to_csv(f"{OUT}/T1c_efa_loadings.csv")
ev, _ = fa.get_eigenvalues()
print("\nEigenvalues (>1):", [round(e, 3) for e in ev if e > 1])
print("\n--- EFA pattern matrix (promax) ---")
print(loadings.round(3).to_string())

# correlation matrix of items saved
df[all_items].corr().to_csv(f"{OUT}/T1d_item_correlations.csv")

summary = {
    "N": int(len(df)),
    "n_items": len(all_items),
    "missing_total": int(df[all_items].isna().sum().sum()),
    "straight_liners": int((row_sd == 0).sum()),
    "KMO": round(kmo_model, 4),
    "Bartlett_chi2": round(float(chi2), 2),
    "Bartlett_p": float(p_bart),
    "Harman_first_factor_pct": round(float(harman_first), 2),
    "max_abs_skew": round(float(desc["Skewness"].abs().max()), 3),
    "max_abs_kurtosis": round(float(desc["Kurtosis"].abs().max()), 3),
    "n_nonnormal_items": int((norm["p"] < 0.05).sum()),
    "eigenvalues_gt1": [round(float(e), 3) for e in ev if e > 1],
}
with open(f"{OUT}/screening_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\nSaved screening summary ->", f"{OUT}/screening_summary.json")
