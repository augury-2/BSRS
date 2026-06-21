"""
03_structural_model.py
Structural (inner) model assessment: collinearity (inner VIF), path coefficients
with bootstrap inference (5000 resamples; t, p, percentile CIs), R2/adjusted R2,
f2 effect sizes, Q2 (blindfolding), total/indirect effects (mediation), and
model fit (SRMR). Also computes IPMA inputs (importance vs performance).
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
HYP = {("UE", "BSAT"): "H1", ("UX", "BSAT"): "H2",
       ("UE", "BSUC"): "H3", ("UX", "BSUC"): "H4",
       ("BSAT", "BSUC"): "H5"}

model = PLSSEM(df, BLOCKS, PATHS)

# ---------- Inner VIF ----------
ivif = model.inner_vif()
ivif.to_csv(f"{OUT}/T7_inner_vif.csv", index=False)
print("=== INNER VIF ===")
print(ivif.round(3).to_string(index=False))
print("Max inner VIF = %.3f" % ivif["VIF"].max())

# ---------- R2 / adjusted R2 ----------
r2tab = pd.DataFrame({
    "R2": pd.Series(model.r2),
    "R2_adjusted": pd.Series(model.r2_adj),
}).round(4)
r2tab.to_csv(f"{OUT}/T8_r2.csv")
print("\n=== R2 ===")
print(r2tab.to_string())

# ---------- f2 ----------
f2 = model.f2()
f2.to_csv(f"{OUT}/T9_f2.csv", index=False)
print("\n=== f2 EFFECT SIZES ===")
print(f2.round(4).to_string(index=False))

# ---------- Q2 (blindfolding) ----------
q2 = model.q2_blindfold(omission=7)
with open(f"{OUT}/q2.json", "w") as f:
    json.dump({k: round(float(v), 4) for k, v in q2.items()}, f, indent=2)
print("\n=== Q2 (construct cross-validated redundancy) ===")
for k, v in q2.items():
    print(f"  {k}: {v:.4f}")

# ---------- SRMR ----------
srmr = model.srmr()
print("\n=== MODEL FIT ===")
print("SRMR = %.4f" % srmr)

# ---------- Bootstrap ----------
print("\nRunning 5000 bootstrap resamples (this takes a moment)...")
bp, bl, bind = model.bootstrap(n_boot=5000, seed=42)

# direct path results
rows = []
for (frm, to), samples in bp.items():
    orig = model.path_coef[to][frm]
    s = PLSSEM.summarize_boot(orig, samples)
    f2v = f2[(f2["from"] == frm) & (f2["to"] == to)]["f2"].values
    rows.append({
        "Hypothesis": HYP.get((frm, to), ""),
        "Path": f"{frm} -> {to}",
        "Beta": s["estimate"],
        "SE": s["SE"],
        "t": s["t"],
        "p": s["p"],
        "CI_2.5%": s["CI_2.5"],
        "CI_97.5%": s["CI_97.5"],
        "f2": float(f2v[0]) if len(f2v) else np.nan,
        "Supported": "Yes" if (s["p"] < 0.05 and s["CI_2.5"] * s["CI_97.5"] > 0)
                     else "No",
    })
paths_tab = pd.DataFrame(rows)
# order by hypothesis
paths_tab = paths_tab.sort_values("Path").reset_index(drop=True)
paths_tab.to_csv(f"{OUT}/T10_path_coefficients.csv", index=False)
print("\n=== STRUCTURAL PATHS (bootstrap) ===")
print(paths_tab.round(4).to_string(index=False))

# indirect / mediation effects
rows = []
for (exo, med, endo), samples in bind.items():
    orig = model.path_coef[med][exo] * model.path_coef[endo][med]
    s = PLSSEM.summarize_boot(orig, samples)
    # total effect = direct + indirect
    direct = model.path_coef[endo].get(exo, 0.0)
    rows.append({
        "Indirect_path": f"{exo} -> {med} -> {endo}",
        "Indirect_effect": s["estimate"],
        "SE": s["SE"], "t": s["t"], "p": s["p"],
        "CI_2.5%": s["CI_2.5"], "CI_97.5%": s["CI_97.5"],
        "Direct_effect": direct,
        "Total_effect": direct + s["estimate"],
        "Mediation": ("Full" if (abs(direct) < 1e-6 or
                                 (s["CI_2.5"] * s["CI_97.5"] > 0 and
                                  paths_tab.loc[paths_tab["Path"] == f"{exo} -> {endo}",
                                                "Supported"].eq("No").all()))
                      else ("Partial (complementary)"
                            if s["CI_2.5"] * s["CI_97.5"] > 0 else "No mediation")),
    })
med_tab = pd.DataFrame(rows)
med_tab.to_csv(f"{OUT}/T11_mediation.csv", index=False)
print("\n=== INDIRECT / MEDIATION EFFECTS ===")
print(med_tab.round(4).to_string(index=False))

# total effects on BSUC
print("\n=== TOTAL EFFECTS on BSUC ===")
tot = {}
tot["UX"] = model.path_coef["BSUC"]["UX"] + model.path_coef["BSAT"]["UX"] * model.path_coef["BSUC"]["BSAT"]
tot["UE"] = model.path_coef["BSUC"]["UE"] + model.path_coef["BSAT"]["UE"] * model.path_coef["BSUC"]["BSAT"]
tot["BSAT"] = model.path_coef["BSUC"]["BSAT"]
for k, v in tot.items():
    print(f"  {k} -> BSUC total = {v:.4f}")

# ---------- IPMA (Importance-Performance Map) for BSUC ----------
# importance = total effect (unstandardized via standardized here);
# performance = rescaled mean construct score to 0-100
raw = df[[i for b in BLOCKS.values() for i in b]]
perf = {}
for c, items in BLOCKS.items():
    # performance index: mean of items rescaled (x-1)/(7-1)*100
    perf[c] = ((raw[items].mean(axis=1).mean() - 1) / 6) * 100
ipma = pd.DataFrame({
    "Construct": list(tot.keys()),
    "Importance_total_effect": [tot[k] for k in tot],
    "Performance_0_100": [perf[k] for k in tot],
})
ipma.to_csv(f"{OUT}/T12_ipma.csv", index=False)
print("\n=== IPMA (target: BSUC) ===")
print(ipma.round(3).to_string(index=False))

# persist structural summary
summary = {
    "R2": {k: round(float(v), 4) for k, v in model.r2.items()},
    "R2_adj": {k: round(float(v), 4) for k, v in model.r2_adj.items()},
    "Q2": {k: round(float(v), 4) for k, v in q2.items()},
    "SRMR": round(float(srmr), 4),
    "max_inner_VIF": round(float(ivif["VIF"].max()), 3),
}
with open(f"{OUT}/structural_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\nSaved structural model outputs.")
