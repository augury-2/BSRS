"""
fsQCA for the BSRS study.

Conditions : UE, UX, BSAT (construct scores = mean of items)
Outcome    : BSUC (brand success / continuance)

Steps:
  1. Direct-method calibration to fuzzy membership (full-in p95, crossover p50,
     full-out p5 anchors of the 7-point scales).
  2. Analysis of necessity for each condition (and its negation).
  3. Truth table construction with frequency + consistency thresholds.
  4. Sufficiency analysis -> solutions with raw/unique coverage & consistency.

Implemented from scratch in numpy/pandas following Ragin (2008) and
Schneider & Wagemann (2012).  Outputs to analysis/outputs/.
"""
import os
import numpy as np
import pandas as pd
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
os.makedirs(OUT, exist_ok=True)
DATA = os.path.join(HERE, "..", "Original collected reponses.xlsx")

BLOCKS = {
    "UE":   ["UE1", "UE2", "UE3", "UE4", "UE5"],
    "UX":   ["UX1", "UX2", "UX3", "UX4", "UX5"],
    "BSAT": ["BSAT1", "BSAT2", "BSAT3", "BSAT4"],
    "BSUC": ["BSUC1", "BSUC2", "BSUC3", "BSUC4"],
}
CONDITIONS = ["UE", "UX", "BSAT"]
OUTCOME = "BSUC"


def calibrate(x, full_in, crossover, full_out):
    """Direct method calibration (Ragin 2008) using log-odds metric."""
    x = np.asarray(x, float)
    fuzzy = np.zeros_like(x)
    # deviation from crossover
    for i, v in enumerate(x):
        if v >= crossover:
            # scale to upper anchor
            if full_in == crossover:
                fuzzy[i] = 1.0
            else:
                dev = (v - crossover) / (full_in - crossover)
                # map dev in [0,1] -> log odds 0..~ +inf ; use Ragin scalar 3
                odds = np.exp(dev * 3.0) - 1 + 1e-9
                # convert: membership above 0.5
                fuzzy[i] = 0.5 + 0.5 * (1 - np.exp(-dev * 3.0))
        else:
            dev = (crossover - v) / (crossover - full_out) if crossover != full_out else 1.0
            fuzzy[i] = 0.5 - 0.5 * (1 - np.exp(-dev * 3.0))
    return np.clip(fuzzy, 0.0001, 0.9999)


def consistency(cond, outcome):
    return np.sum(np.minimum(cond, outcome)) / np.sum(cond)


def coverage(cond, outcome):
    return np.sum(np.minimum(cond, outcome)) / np.sum(outcome)


def main():
    df = pd.read_excel(DATA)
    sc = pd.DataFrame({k: df[v].mean(axis=1) for k, v in BLOCKS.items()})

    # ---- calibration anchors (percentiles of each construct)
    cal = {}
    anchors = []
    for c in CONDITIONS + [OUTCOME]:
        fi, cr, fo = np.percentile(sc[c], [95, 50, 5])
        cal[c] = calibrate(sc[c], fi, cr, fo)
        anchors.append(dict(Variable=c, Full_in_p95=fi, Crossover_p50=cr, Full_out_p5=fo))
    cal = pd.DataFrame(cal)
    anchors_df = pd.DataFrame(anchors)
    cal.to_csv(os.path.join(OUT, "fsqca_calibrated.csv"), index=False)
    anchors_df.to_csv(os.path.join(OUT, "fsqca_calibration_anchors.csv"), index=False)

    out = cal[OUTCOME].values

    # ---- necessity analysis (condition and negation), for outcome and ~outcome
    nec_rows = []
    for c in CONDITIONS:
        for label, cond in [(c, cal[c].values), ("~" + c, 1 - cal[c].values)]:
            nec_rows.append(dict(Condition=label, Outcome="BSUC",
                                 Consistency=consistency(cond, out),
                                 Coverage=coverage(cond, out)))
            nec_rows.append(dict(Condition=label, Outcome="~BSUC",
                                 Consistency=consistency(cond, 1 - out),
                                 Coverage=coverage(cond, 1 - out)))
    nec_df = pd.DataFrame(nec_rows)
    nec_df.to_csv(os.path.join(OUT, "fsqca_necessity.csv"), index=False)

    # ---- truth table
    # membership of each case in each of 2^k corners
    corners = list(product([1, 0], repeat=len(CONDITIONS)))  # 1=present,0=absent
    rows = []
    for corner in corners:
        membership = np.ones(len(df))
        label_parts = []
        for ci, c in enumerate(CONDITIONS):
            m = cal[c].values if corner[ci] == 1 else 1 - cal[c].values
            membership = np.minimum(membership, m)
            label_parts.append(c if corner[ci] == 1 else "~" + c)
        n_cases = int(np.sum(membership > 0.5))
        if np.sum(membership) > 0:
            cons = np.sum(np.minimum(membership, out)) / np.sum(membership)
        else:
            cons = np.nan
        rows.append(dict(Configuration=" * ".join(label_parts),
                         **{c: corner[i] for i, c in enumerate(CONDITIONS)},
                         Cases_gt_0_5=n_cases, Consistency=cons))
    tt = pd.DataFrame(rows).sort_values("Consistency", ascending=False)
    tt.to_csv(os.path.join(OUT, "fsqca_truth_table.csv"), index=False)

    # ---- sufficiency: rows passing freq>=3 and consistency>=0.80 coded outcome=1
    FREQ, CONS = 3, 0.80
    def code_row(r):
        if r["Cases_gt_0_5"] < FREQ:
            return "?"          # logical remainder
        return 1 if r["Consistency"] >= CONS else 0
    tt["Outcome_code"] = tt.apply(code_row, axis=1)

    suff_rows = []
    for _, r in tt.iterrows():
        if r["Outcome_code"] == 1:
            # build configuration membership
            membership = np.ones(len(df))
            for c in CONDITIONS:
                membership = np.minimum(
                    membership, cal[c].values if r[c] == 1 else 1 - cal[c].values)
            raw_cov = coverage(membership, out)
            cons = consistency(membership, out)
            suff_rows.append(dict(Configuration=r["Configuration"],
                                  Raw_coverage=raw_cov, Consistency=cons))
    suff_df = pd.DataFrame(suff_rows)
    suff_df.to_csv(os.path.join(OUT, "fsqca_sufficiency.csv"), index=False)

    # overall solution coverage/consistency if any
    if len(suff_rows):
        # union (max) of configuration memberships
        union = np.zeros(len(df))
        for _, r in tt.iterrows():
            if r["Outcome_code"] == 1:
                membership = np.ones(len(df))
                for c in CONDITIONS:
                    membership = np.minimum(
                        membership, cal[c].values if r[c] == 1 else 1 - cal[c].values)
                union = np.maximum(union, membership)
        sol = dict(Solution_coverage=coverage(union, out),
                   Solution_consistency=consistency(union, out))
    else:
        sol = dict(Solution_coverage=np.nan, Solution_consistency=np.nan)
    pd.DataFrame([sol]).to_csv(os.path.join(OUT, "fsqca_solution.csv"), index=False)

    # console
    pd.set_option("display.width", 160)
    print("=== Calibration anchors ===\n", anchors_df.round(3), "\n")
    print("=== Necessity (BSUC) ===\n",
          nec_df[nec_df.Outcome == "BSUC"].round(3).to_string(index=False), "\n")
    print("=== Truth table ===\n", tt.round(3).to_string(index=False), "\n")
    print("=== Sufficient configurations (freq>=3, cons>=0.80) ===")
    if len(suff_rows):
        print(suff_df.round(3).to_string(index=False))
    else:
        print("  NONE - no configuration meets the consistency threshold.")
    print("\n=== Solution ===\n", sol, "\n")


if __name__ == "__main__":
    main()
