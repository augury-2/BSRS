"""
04_fsqca.py
Fuzzy-set QCA of high Brand-System continuance (BSUC).
Conditions: UE (engagement), UX (experience), BSAT (satisfaction).
Pipeline: calibration -> descriptives -> necessity -> truth table ->
complex/parsimonious/intermediate sufficiency -> core/peripheral ->
robustness (alternative anchors & consistency cutoffs).
"""
import os
import json
import itertools
import numpy as np
import pandas as pd
import fsqca_engine as fz

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
# composite (averaged) indicators per construct -> calibration base
comp = pd.DataFrame({c: df[items].mean(axis=1) for c, items in BLOCKS.items()})
CONDS = ["UE", "UX", "BSAT"]
OUTCOME = "BSUC"

# ---------- calibration anchors (percentile direct method) ----------
def anchors(series, lo=0.05, mid=0.50, hi=0.95):
    return (series.quantile(hi), series.quantile(mid), series.quantile(lo))

cal = pd.DataFrame(index=comp.index)
anchor_log = {}
for c in BLOCKS:
    fi, cr, fo = anchors(comp[c])
    anchor_log[c] = {"full_in_p95": fi, "crossover_p50": cr, "full_out_p5": fo}
    cal[c] = fz.calibrate(comp[c].values, fi, cr, fo)

pd.DataFrame(anchor_log).T.to_csv(f"{OUT}/T14_calibration_anchors.csv")
print("=== CALIBRATION ANCHORS (percentile direct method) ===")
print(pd.DataFrame(anchor_log).T.round(3).to_string())
cal.to_csv(f"{OUT}/calibrated_data.csv", index=False)

# ---------- necessity ----------
nec, nec_neg = fz.necessity_analysis(cal, OUTCOME, CONDS)
nec.to_csv(f"{OUT}/T15_necessity_high.csv", index=False)
nec_neg.to_csv(f"{OUT}/T15b_necessity_low.csv", index=False)
print("\n=== NECESSARY CONDITIONS for HIGH BSUC (threshold cons >= 0.90) ===")
print(nec.round(3).to_string(index=False))
print("\n=== NECESSARY CONDITIONS for LOW (~BSUC) ===")
print(nec_neg.round(3).to_string(index=False))

# ---------- truth table ----------
# frequency cutoff: retain configurations with enough cases (n=312 -> use >=4),
# consistency cutoff 0.80, PRI cutoff 0.70 (Pappas & Woodside 2021)
FREQ, CONS, PRI = 4, 0.80, 0.70
tt, corners = fz.truth_table(cal, OUTCOME, CONDS,
                             freq_cutoff=FREQ, cons_cutoff=CONS, pri_cutoff=PRI)
tt_sorted = tt.sort_values("raw_consistency", ascending=False).reset_index(drop=True)
tt_sorted.to_csv(f"{OUT}/T16_truth_table.csv", index=False)
print(f"\n=== TRUTH TABLE (freq>={FREQ}, raw cons>={CONS}, PRI>={PRI}) ===")
print(tt_sorted.round(3).to_string(index=False))

# ---------- sufficiency: complex / parsimonious / intermediate ----------
k = len(CONDS)
def corner_to_tuple(row):
    return tuple(int(row[c]) for c in CONDS)

observed = tt[tt["status"] != "remainder"]
minterms = [corner_to_tuple(r) for _, r in observed[observed["OUT"] == 1].iterrows()]
remainders = [corner_to_tuple(r) for _, r in tt[tt["status"] == "remainder"].iterrows()]

# Complex (conservative): NO remainders used
complex_impl = fz.quine_mccluskey(minterms, dont_cares=[])
# Parsimonious: ALL remainders allowed as don't-cares
parsi_impl = fz.quine_mccluskey(minterms, dont_cares=remainders)
# Intermediate: only "easy" counterfactuals consistent with directional
# expectation that the PRESENCE of each condition contributes to high BSUC.
# Easy remainders = remainders that are supersets (in presence) of a parsimonious
# implicant and consistent with expectations (no condition expected absent).
def easy_remainders(parsi, remainders):
    easy = []
    for r in remainders:
        # consistent with "presence contributes": allow remainder only if it does
        # not require any condition to be ABSENT beyond what parsimonious allows
        for p in parsi:
            if all((pv == "-") or (pv == rv) for pv, rv in zip(p, r)):
                # directional: presence (1) expected; a remainder adding a 1 is easy
                easy.append(r)
                break
    return list(set(easy))

easy = easy_remainders(parsi_impl, remainders)
inter_impl = fz.quine_mccluskey(minterms, dont_cares=easy)

def report(name, impl):
    cfg, scov, scons = fz.solution_metrics(impl, cal, CONDS, OUTCOME)
    print(f"\n=== {name} SOLUTION ===")
    print(cfg.round(3).to_string(index=False))
    print(f"Solution coverage = {scov:.3f} | Solution consistency = {scons:.3f}")
    return cfg, scov, scons

cx_cfg, cx_cov, cx_cons = report("COMPLEX", complex_impl)
pa_cfg, pa_cov, pa_cons = report("PARSIMONIOUS", parsi_impl)
in_cfg, in_cov, in_cons = report("INTERMEDIATE", inter_impl)

cx_cfg.to_csv(f"{OUT}/T17_complex_solution.csv", index=False)
pa_cfg.to_csv(f"{OUT}/T18_parsimonious_solution.csv", index=False)
in_cfg.to_csv(f"{OUT}/T19_intermediate_solution.csv", index=False)

# ---------- core vs peripheral (Fiss 2011) ----------
# core = condition appears in BOTH intermediate AND parsimonious solution term
# peripheral = appears only in intermediate
def literal_set(impl):
    s = set()
    for term in impl:
        for val, name in zip(term, CONDS):
            if val != "-":
                s.add((name, val))
    return s

parsi_lits = literal_set(parsi_impl)
core_peripheral = []
for term in inter_impl:
    for val, name in zip(term, CONDS):
        if val != "-":
            role = "core" if (name, val) in parsi_lits else "peripheral"
            core_peripheral.append({
                "Configuration": fz.implicant_to_expr(term, CONDS),
                "Condition": ("" if val == 1 else "~") + name,
                "Role": role,
            })
cp = pd.DataFrame(core_peripheral)
cp.to_csv(f"{OUT}/T20_core_peripheral.csv", index=False)
print("\n=== CORE vs PERIPHERAL (Fiss 2011) ===")
print(cp.to_string(index=False))

# ---------- also analyse NEGATED outcome (asymmetry) ----------
caln = cal.copy()
tt_neg, _ = fz.truth_table(
    pd.concat([cal[CONDS], pd.Series(1 - cal[OUTCOME].values, name=OUTCOME,
                                     index=cal.index)], axis=1),
    OUTCOME, CONDS, freq_cutoff=FREQ, cons_cutoff=CONS, pri_cutoff=PRI)
neg_minterms = [tuple(int(r[c]) for c in CONDS)
                for _, r in tt_neg[(tt_neg["OUT"] == 1) &
                                   (tt_neg["status"] != "remainder")].iterrows()]
neg_remainders = [tuple(int(r[c]) for c in CONDS)
                  for _, r in tt_neg[tt_neg["status"] == "remainder"].iterrows()]
neg_impl = fz.quine_mccluskey(neg_minterms, dont_cares=[])
calneg = pd.concat([cal[CONDS], pd.Series(1 - cal[OUTCOME].values, name=OUTCOME,
                                          index=cal.index)], axis=1)
if neg_impl:
    neg_cfg, neg_cov, neg_cons = fz.solution_metrics(neg_impl, calneg, CONDS, OUTCOME)
    neg_cfg.to_csv(f"{OUT}/T21_negated_outcome_solution.csv", index=False)
    print("\n=== SOLUTION for LOW BSUC (~BSUC) [asymmetry check] ===")
    print(neg_cfg.round(3).to_string(index=False))
    print(f"Solution coverage = {neg_cov:.3f} | consistency = {neg_cons:.3f}")
else:
    neg_cov = neg_cons = float("nan")
    print("\nNo sufficient configuration for ~BSUC at current thresholds.")

# ---------- robustness: alternative anchors & cutoffs ----------
robust_rows = []
scenarios = [
    ("Percentile 90/50/10", 0.90, 0.50, 0.10, 4, 0.80),
    ("Percentile 95/50/5 (main)", 0.95, 0.50, 0.05, 4, 0.80),
    ("Substantive 6/4/2 (Likert)", None, None, None, 4, 0.80),
    ("Higher cons cutoff 0.85", 0.95, 0.50, 0.05, 4, 0.85),
    ("Higher freq cutoff 6", 0.95, 0.50, 0.05, 6, 0.80),
]
for label, hi, mid, lo, fq, cs in scenarios:
    cal2 = pd.DataFrame(index=comp.index)
    for c in BLOCKS:
        if hi is None:
            fi, cr, fo = 6.0, 4.0, 2.0
        else:
            fi, cr, fo = (comp[c].quantile(hi), comp[c].quantile(mid),
                          comp[c].quantile(lo))
        cal2[c] = fz.calibrate(comp[c].values, fi, cr, fo)
    tt2, _ = fz.truth_table(cal2, OUTCOME, CONDS, freq_cutoff=fq,
                            cons_cutoff=cs, pri_cutoff=PRI)
    mt2 = [tuple(int(r[c]) for c in CONDS)
           for _, r in tt2[(tt2["OUT"] == 1) & (tt2["status"] != "remainder")].iterrows()]
    impl2 = fz.quine_mccluskey(mt2, dont_cares=[])
    if impl2:
        cfg2, cov2, cons2 = fz.solution_metrics(impl2, cal2, CONDS, OUTCOME)
        terms2 = "; ".join(cfg2["Configuration"].tolist())
    else:
        cov2 = cons2 = np.nan
        terms2 = "(none)"
    robust_rows.append({
        "Scenario": label, "n_configs": len(impl2),
        "Sol_coverage": cov2, "Sol_consistency": cons2,
        "Configurations": terms2,
    })
robust = pd.DataFrame(robust_rows)
robust.to_csv(f"{OUT}/T22_robustness.csv", index=False)
print("\n=== ROBUSTNESS (alternative calibrations & cutoffs) ===")
print(robust.round(3).to_string(index=False))

# ---------- persist summary ----------
summary = {
    "frequency_cutoff": FREQ, "consistency_cutoff": CONS, "PRI_cutoff": PRI,
    "complex": {"coverage": round(float(cx_cov), 3), "consistency": round(float(cx_cons), 3),
                "n_configs": len(complex_impl)},
    "parsimonious": {"coverage": round(float(pa_cov), 3), "consistency": round(float(pa_cons), 3),
                     "n_configs": len(parsi_impl)},
    "intermediate": {"coverage": round(float(in_cov), 3), "consistency": round(float(in_cons), 3),
                     "n_configs": len(inter_impl)},
    "negated_outcome": {"coverage": round(float(neg_cov), 3) if neg_cov == neg_cov else None,
                        "consistency": round(float(neg_cons), 3) if neg_cons == neg_cons else None},
}
with open(f"{OUT}/fsqca_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\nSaved fsQCA outputs.")
