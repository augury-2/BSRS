import pandas as pd
import numpy as np
from scipy import stats
from plssem import PLSSEM

pd.set_option('display.width', 220)
pd.set_option('display.max_columns', 100)
np.set_printoptions(suppress=True)

df = pd.read_excel("MTVS.xlsx", sheet_name="Sheet1")

measurement = {
    "UE":   ["UE1", "UE2", "UE3", "UE4", "UE5"],
    "UX":   ["UX1", "UX2", "UX3", "UX4", "UX5"],
    "BSAT": ["BSAT1", "BSAT2", "BSAT3", "BSAT4"],
    "BSUC": ["BSUC1", "BSUC2", "BSUC3", "BSUC4"],
}
all_items = [i for v in measurement.values() for i in v]

# ---------- Outlier / distribution check ----------
print("="*70)
print("OUTLIER & DISTRIBUTION CHECK (item level)")
print("="*70)
desc = pd.DataFrame({
    "mean": df[all_items + ["ATT_1","ATT_2"]].mean(),
    "sd": df[all_items + ["ATT_1","ATT_2"]].std(ddof=1),
    "min": df[all_items + ["ATT_1","ATT_2"]].min(),
    "max": df[all_items + ["ATT_1","ATT_2"]].max(),
    "skew": df[all_items + ["ATT_1","ATT_2"]].skew(),
    "kurt": df[all_items + ["ATT_1","ATT_2"]].kurt(),
})
print(desc.round(3))

# Mahalanobis distance multivariate outliers
Xm = df[all_items].values.astype(float)
mean = Xm.mean(axis=0)
cov = np.cov(Xm, rowvar=False)
inv = np.linalg.inv(cov)
d2 = np.array([ (row-mean) @ inv @ (row-mean) for row in Xm ])
crit = stats.chi2.ppf(0.999, df=len(all_items))
print(f"\nMahalanobis D^2: max={d2.max():.2f}, chi2 crit(.001,{len(all_items)}df)={crit:.2f}, n flagged={np.sum(d2>crit)}")

# ---------- Composites ----------
df["UE_comp"]   = df[measurement["UE"]].mean(axis=1)
df["UX_comp"]   = df[measurement["UX"]].mean(axis=1)
df["BSAT_comp"] = df[measurement["BSAT"]].mean(axis=1)
df["BSUC_comp"] = df[measurement["BSUC"]].mean(axis=1)

print("\n" + "="*70)
print("COMPOSITE DESCRIPTIVES & CORRELATIONS")
print("="*70)
comps = ["UE_comp","UX_comp","BSAT_comp","BSUC_comp"]
cdesc = pd.DataFrame({"mean": df[comps].mean(), "sd": df[comps].std(ddof=1)})
print(cdesc.round(3))
print("\nCorrelation matrix (composites) + ATT:")
corr_vars = comps + ["ATT_1","ATT_2"]
print(df[corr_vars].corr().round(3))

# ---------- PLS-SEM measurement model ----------
structural = {
    "BSAT": ["UE", "UX"],
    "BSUC": ["UE", "UX", "BSAT"],
}
model = PLSSEM(df, measurement, structural).fit()

print("\n" + "="*70)
print("OUTER LOADINGS")
print("="*70)
rows = []
for c in measurement:
    for i in measurement[c]:
        rows.append((c, i, model.loadings[c][i]))
load_df = pd.DataFrame(rows, columns=["Construct","Item","Loading"])
print(load_df.round(4).to_string(index=False))

print("\n" + "="*70)
print("RELIABILITY & AVE")
print("="*70)
print(model.reliability().round(4))

print("\n" + "="*70)
print("HTMT")
print("="*70)
print(model.htmt().round(4))

print("\n" + "="*70)
print("FORNELL-LARCKER (sqrt AVE on diagonal)")
print("="*70)
print(model.fornell_larcker().round(4))

print("\n" + "="*70)
print("FULL COLLINEARITY VIF (CMB check)")
print("="*70)
print(model.full_collinearity_vif().round(4))

print("\n" + "="*70)
print("STRUCTURAL PATHS & R2 (point estimates)")
print("="*70)
for endo, paths in model.paths.items():
    for p, b in paths.items():
        print(f"  {p:5s} -> {endo:5s}: beta = {b:.4f}")
print("R2:", {k: round(v,4) for k,v in model.r2.items()})
print("R2 adj:", {k: round(v,4) for k,v in model.r2_adj.items()})

# save composites for fsQCA
df.to_csv("data_with_composites.csv", index=False)
print("\nSaved data_with_composites.csv")
