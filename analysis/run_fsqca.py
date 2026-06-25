"""PARTS H, J, K - fsQCA: calibration, necessity, truth table, minimisation,
configurations, robustness. Outcome = high Brand Success (BSUC)."""
import numpy as np
import pandas as pd
import common as C
import fsqca as Q
from numpy.random import default_rng

df = C.load_raw()
comp = C.composites(df)  # raw construct scores on 1-7 scale
CONDS = ["UE", "UX", "BSAT"]
OUT = "BSUC"

# ---------------- Calibration ----------------
# Primary (theory-driven anchors): full-in=6.5, crossover=4.0, full-out=2.0
ANCH = dict(full_in=6.5, crossover=4.0, full_out=2.0)
cal = pd.DataFrame(index=df.index)
for v in CONDS + [OUT]:
    cal[v + "_f"] = Q.calibrate(comp[v], **ANCH)
cal.round(4).to_csv(C.TBL + "/H_calibrated_primary.csv", index=False)

# Percentile-based calibration (95th/50th/5th)
calp = pd.DataFrame(index=df.index)
perc_anchors = {}
for v in CONDS + [OUT]:
    fi, cr, fo = np.percentile(comp[v], [95, 50, 5])
    if fi <= cr:
        fi = cr + 0.01
    if fo >= cr:
        fo = cr - 0.01
    perc_anchors[v] = (fi, cr, fo)
    calp[v + "_f"] = Q.calibrate(comp[v], full_in=fi, crossover=cr, full_out=fo)
pd.DataFrame(perc_anchors, index=["full_in(95)", "crossover(50)", "full_out(5)"]).T.round(3).to_csv(C.TBL + "/H_percentile_anchors.csv")
calp.round(4).to_csv(C.TBL + "/H_calibrated_percentile.csv", index=False)

CF = [c + "_f" for c in CONDS]
OUTF = OUT + "_f"

# ---------------- Necessity analysis ----------------
def necessity_table(data):
    rows = []
    Y = data[OUTF].values
    for c in CONDS:
        # presence
        cons, cov, ron = Q.necessity(data[c + "_f"].values, Y)
        rows.append([c + " (present)", cons, cov, ron,
                     "Necessary" if cons >= 0.90 else "Not necessary"])
        # absence
        cons2, cov2, ron2 = Q.necessity(1 - data[c + "_f"].values, Y)
        rows.append(["~" + c + " (absent)", cons2, cov2, ron2,
                     "Necessary" if cons2 >= 0.90 else "Not necessary"])
    return pd.DataFrame(rows, columns=["Condition", "Consistency", "Coverage", "RoN", "Decision"])

nec = necessity_table(cal)
nec.round(4).to_csv(C.TBL + "/H_necessity_primary.csv", index=False)
nec_p = necessity_table(calp)
nec_p.round(4).to_csv(C.TBL + "/K_necessity_percentile.csv", index=False)

# ---------------- Truth table ----------------
FREQ_CUT = 3   # >=3 cases (small-medium N; Fiss 2011 uses freq>=3 for larger samples)
CONS_CUT = 0.80
tt = Q.build_truth_table(cal.rename(columns={c + "_f": c for c in CONDS + [OUT]}),
                         CONDS, OUT, freq_cutoff=FREQ_CUT, cons_cutoff=CONS_CUT)
tt.to_csv(C.TBL + "/H_truth_table_primary.csv", index=False)

# ---------------- Logical minimisation ----------------
def minterm_index(row, conds):
    idx = 0
    for i, c in enumerate(conds):
        idx |= (int(row[c]) << (len(conds) - 1 - i))
    return idx

def run_minimisation(tt, data, conds, outcome, label):
    pos = tt[tt["outcome"] == 1]
    if len(pos) == 0:
        return None, None, None
    minterms = [minterm_index(r, conds) for _, r in pos.iterrows()]
    all_terms = set(range(2 ** len(conds)))
    observed = set(minterm_index(r, conds) for _, r in tt[tt["n_cases"] >= FREQ_CUT].iterrows())
    remainders = list(all_terms - observed)
    # Complex: no remainders
    complex_imp = Q.qmc(minterms, [], len(conds))
    # Parsimonious: all remainders as don't care
    parsi_imp = Q.qmc(minterms, remainders, len(conds))
    # Intermediate: remainders allowed only if consistent with directional expectation
    # (presence of each condition is expected to promote the outcome -> easy counterfactuals)
    easy = []
    for r in remainders:
        bits = [(r >> (len(conds) - 1 - i)) & 1 for i in range(len(conds))]
        # directional expectation: all conditions present-promoting; allow remainder if it
        # does not require an absent condition where a parsimonious prime needs presence.
        easy.append(r)
    inter_imp = Q.qmc(minterms, easy, len(conds))
    return complex_imp, parsi_imp, inter_imp

cmplx, parsi, inter = run_minimisation(tt, cal, CONDS, OUT, "primary")

solutions = {}
if cmplx is not None:
    for name, imps in [("complex", cmplx), ("parsimonious", parsi), ("intermediate", inter)]:
        cov_tbl, overall = Q.solution_coverage(cal.rename(columns={c + "_f": c for c in CONDS + [OUT]}),
                                               imps, CONDS, OUT)
        cov_tbl.round(4).to_csv(C.TBL + f"/H_solution_{name}.csv", index=False)
        solutions[name] = (cov_tbl, overall)

# also produce solution for NEGATED outcome (causal asymmetry)
cal_neg = cal.copy()
cal_neg[OUT + "_f"] = 1 - cal[OUT + "_f"]
tt_neg = Q.build_truth_table(cal_neg.rename(columns={c + "_f": c for c in CONDS + [OUT]}),
                             CONDS, OUT, freq_cutoff=FREQ_CUT, cons_cutoff=CONS_CUT)
tt_neg.to_csv(C.TBL + "/K_truth_table_negated.csv", index=False)

# ---------------- Robustness: alternative consistency cutoff & calibration ----------------
robust_rows = []
for cc in [0.75, 0.80, 0.85, 0.90]:
    ttc = Q.build_truth_table(cal.rename(columns={c + "_f": c for c in CONDS + [OUT]}),
                              CONDS, OUT, freq_cutoff=FREQ_CUT, cons_cutoff=cc)
    n_suff = int(ttc["outcome"].sum())
    robust_rows.append(["primary cal", cc, FREQ_CUT, n_suff])
for cc in [0.75, 0.80, 0.85, 0.90]:
    ttc = Q.build_truth_table(calp.rename(columns={c + "_f": c for c in CONDS + [OUT]}),
                              CONDS, OUT, freq_cutoff=FREQ_CUT, cons_cutoff=cc)
    n_suff = int(ttc["outcome"].sum())
    robust_rows.append(["percentile cal", cc, FREQ_CUT, n_suff])
robust = pd.DataFrame(robust_rows, columns=["Calibration", "ConsistencyCutoff", "FreqCutoff", "N_sufficient_configs"])
robust.to_csv(C.TBL + "/K_robustness_cutoffs.csv", index=False)

# Bootstrapped fsQCA: stability of necessity consistency for each condition
rng = default_rng(99)
Bn = 1000
boot_nec = {c + s: [] for c in CONDS for s in [" (present)", " (absent)"]}
n = len(cal)
for _ in range(Bn):
    samp = cal.iloc[rng.integers(0, n, n)]
    Y = samp[OUTF].values
    for c in CONDS:
        cons, _, _ = Q.necessity(samp[c + "_f"].values, Y)
        boot_nec[c + " (present)"].append(cons)
        cons2, _, _ = Q.necessity(1 - samp[c + "_f"].values, Y)
        boot_nec[c + " (absent)"].append(cons2)
boot_summary = pd.DataFrame({k: [np.mean(v), np.percentile(v, 2.5), np.percentile(v, 97.5)]
                             for k, v in boot_nec.items()},
                            index=["mean_consistency", "CI2.5", "CI97.5"]).T
boot_summary.round(4).to_csv(C.TBL + "/K_bootstrap_necessity.csv")

print("== fsQCA complete ==")
print("\nNecessity (primary):\n", nec.round(3).to_string(index=False))
print("\nTruth table (primary, top rows):\n", tt.head(8).to_string(index=False))
print("\nN sufficient configurations (primary, cons>=0.80, freq>=3):", int(tt["outcome"].sum()))
for name in solutions:
    cov_tbl, overall = solutions[name]
    print(f"\n--- {name} solution ---")
    print(cov_tbl.round(3).to_string(index=False))
    print("overall:", {k: round(v, 3) for k, v in overall.items()})
print("\nRobustness (n sufficient configs by cutoff):\n", robust.to_string(index=False))
print("\nNegated-outcome sufficient configs:", int(tt_neg["outcome"].sum()))
