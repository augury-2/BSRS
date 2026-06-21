"""
02_measurement_model.py
Estimate the PLS-SEM measurement (outer) model and assess reliability and
validity. Cross-validate the custom engine against the `plspm` package.
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
# UE, UX -> BSAT -> BSUC  (+ direct UE,UX -> BSUC)
PATHS = {
    "BSAT": ["UE", "UX"],
    "BSUC": ["UE", "UX", "BSAT"],
}

model = PLSSEM(df, BLOCKS, PATHS)

# ---------- Outer loadings ----------
load_rows = []
for c, items in BLOCKS.items():
    for it in items:
        load_rows.append({"Construct": c, "Item": it,
                          "Loading": model.loadings[it]})
loadings = pd.DataFrame(load_rows)
loadings.to_csv(f"{OUT}/T2_outer_loadings.csv", index=False)
print("=== OUTER LOADINGS ===")
print(loadings.round(3).to_string(index=False))

# ---------- Reliability & convergent validity ----------
rel = model.reliability[["n_items", "Cronbach_alpha", "rho_A", "rho_c_CR", "AVE"]]
rel.to_csv(f"{OUT}/T3_reliability.csv")
print("\n=== RELIABILITY & CONVERGENT VALIDITY ===")
print(rel.round(3).to_string())

# ---------- Outer VIF ----------
ovif = model.outer_vif()
ovif.to_csv(f"{OUT}/T2b_outer_vif.csv", index=False)
print("\nMax outer VIF = %.3f" % ovif["VIF"].max())

# ---------- Discriminant validity ----------
FL = model.fornell_larcker()
FL.to_csv(f"{OUT}/T4_fornell_larcker.csv")
print("\n=== FORNELL-LARCKER (diag = sqrt(AVE)) ===")
print(FL.round(3).to_string())

HTMT = model.htmt()
HTMT.to_csv(f"{OUT}/T5_htmt.csv")
print("\n=== HTMT ===")
print(HTMT.round(3).to_string())
print("Max HTMT (off-diag) = %.3f" %
      HTMT.values[~np.eye(len(HTMT), dtype=bool)].max())

CL = model.cross_loadings()
CL.to_csv(f"{OUT}/T6_cross_loadings.csv")
print("\n=== CROSS-LOADINGS (each item should load highest on own construct) ===")
print(CL.round(3).to_string())

# ---------- Validate against plspm ----------
print("\n=== VALIDATION vs plspm ===")
try:
    import plspm.config as c
    from plspm.plspm import Plspm
    from plspm.mode import Mode
    from plspm.scheme import Scheme

    structure = c.Structure()
    structure.add_path(["UE", "UX"], ["BSAT"])
    structure.add_path(["UE", "UX", "BSAT"], ["BSUC"])
    config = c.Config(structure.path(), default_scale=c.Scale.NUM)
    for con, items in BLOCKS.items():
        config.add_lv(con, Mode.A, *[c.MV(it) for it in items])
    pls = Plspm(df, config, Scheme.PATH)
    pls_outer = pls.outer_model()
    # compare loadings
    comp = []
    for c_, items in BLOCKS.items():
        for it in items:
            mine = abs(model.loadings[it])
            theirs = abs(pls_outer.loc[it, "loading"])
            comp.append(abs(mine - theirs))
    print("Max |loading| difference (custom vs plspm): %.4f" % max(comp))
    uni = pls.unidimensionality()
    print("plspm reliability (validation):")
    print(uni[["cronbach_alpha", "dillon_goldstein_rho"]].round(3).to_string())
    pls.path_coefficients().to_csv(f"{OUT}/validation_plspm_paths.csv")
    print("\nplspm path coefficients saved for cross-check.")
except Exception as e:
    print("plspm validation skipped:", repr(e))

# save model artifacts for downstream scripts
model.scores.to_csv(f"{OUT}/construct_scores.csv", index=False)
print("\nSaved construct scores and measurement tables.")
