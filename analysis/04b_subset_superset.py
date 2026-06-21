"""
04b_subset_superset.py
Intermediate-solution subset/superset analysis and the Fiss-style configuration
table for HIGH Brand Success (BSUC) in the metaverse.

Subset/superset analysis (Ragin fs/QCA): for every non-empty combination of the
*presence* of the causal conditions, treat the AND (set intersection) of those
conditions as a candidate sufficient term and report its raw consistency, PRI
consistency, and raw coverage with respect to the outcome. Less restrictive
expressions (fewer conditions) are supersets; more restrictive ones (more
conditions) are subsets.
"""
import os
import itertools
import pandas as pd
import numpy as np
import fsqca_engine as fz

OUT = "analysis/outputs"
os.makedirs(OUT, exist_ok=True)

cal = pd.read_csv(f"{OUT}/calibrated_data.csv")
CONDS = ["UE", "UX", "BSAT"]
OUTCOME = "BSUC"
Y = cal[OUTCOME].values

# ---------- subset/superset analysis (presence only) ----------
rows = []
for k in range(1, len(CONDS) + 1):
    for combo in itertools.combinations(CONDS, k):
        memb = np.ones(len(cal))
        for c in combo:
            memb = np.minimum(memb, cal[c].values)
        cons = fz.consistency_suff(memb, Y)
        pri = fz.pri_consistency(memb, Y)
        cov = fz.coverage_suff(memb, Y)
        rows.append({
            "Combination": " * ".join(combo),
            "n_conditions": k,
            "Raw_consistency": round(cons, 3),
            "PRI_consistency": round(pri, 3),
            "Raw_coverage": round(cov, 3),
        })
ss = pd.DataFrame(rows).sort_values(
    ["Raw_consistency", "n_conditions"], ascending=[False, True]).reset_index(drop=True)
ss.to_csv(f"{OUT}/T16b_subset_superset.csv", index=False)
print("=== INTERMEDIATE SOLUTION: SUBSET/SUPERSET ANALYSIS (outcome = high BSUC) ===")
print(ss.to_string(index=False))

# ---------- Fiss configuration table for high BSUC ----------
# Single intermediate solution: UE * UX * BSAT, all core.
inter_impl = [(1, 1, 1)]
cfg, sol_cov, sol_cons = fz.solution_metrics(inter_impl, cal, CONDS, OUTCOME)
print("\n=== CONFIGURATION ANALYSIS FOR HIGH BSUC (intermediate solution) ===")
print(cfg.round(3).to_string(index=False))
print(f"Overall solution coverage = {sol_cov:.3f} | consistency = {sol_cons:.3f}")

config_rows = []
for cond in CONDS:
    config_rows.append({"Condition": cond, "Configuration 1": "\u25cf (core present)"})
config_rows.append({"Condition": "Raw coverage", "Configuration 1": f"{cfg.iloc[0]['raw_coverage']:.3f}"})
config_rows.append({"Condition": "Unique coverage", "Configuration 1": f"{cfg.iloc[0]['unique_coverage']:.3f}"})
config_rows.append({"Condition": "Consistency", "Configuration 1": f"{cfg.iloc[0]['consistency']:.3f}"})
config_rows.append({"Condition": "Overall solution coverage", "Configuration 1": f"{sol_cov:.3f}"})
config_rows.append({"Condition": "Overall solution consistency", "Configuration 1": f"{sol_cons:.3f}"})
pd.DataFrame(config_rows).to_csv(f"{OUT}/T13b_configuration_high_bsuc.csv", index=False)
print("\nSaved subset/superset and configuration tables.")
