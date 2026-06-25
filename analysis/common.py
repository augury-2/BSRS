"""Shared data-loading and helper utilities for the MTVS PLS-SEM / fsQCA study.

Conventions
-----------
* Constructs are reflective; composite (construct) scores are computed as the
  row-mean of their indicators (mean-replacement is unnecessary because the
  data are complete; see PART A).
* All paths are relative to the repository root so scripts are reproducible.
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TBL = os.path.join(HERE, "tables")
FIG = os.path.join(HERE, "figures")
os.makedirs(TBL, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

DATA = os.path.join(ROOT, "MTVS.xlsx")

# Measurement model specification (construct -> reflective indicators)
CONSTRUCTS = {
    "UE":   ["UE1", "UE2", "UE3", "UE4", "UE5"],
    "UX":   ["UX1", "UX2", "UX3", "UX4", "UX5"],
    "BSAT": ["BSAT1", "BSAT2", "BSAT3", "BSAT4"],
    "BSUC": ["BSUC1", "BSUC2", "BSUC3", "BSUC4"],
}
INDICATORS = [i for items in CONSTRUCTS.values() for i in items]
CONTROLS = ["ATT_1", "ATT_2"]

# Structural model: predictor -> outcome
STRUCTURAL_PATHS = [
    ("UE", "BSAT"), ("UX", "BSAT"),
    ("UE", "BSUC"), ("UX", "BSUC"), ("BSAT", "BSUC"),
]


def load_raw():
    return pd.read_excel(DATA, sheet_name="Sheet1")


def load_indicators():
    df = load_raw()
    return df[INDICATORS].astype(float)


def composites(df=None):
    """Construct scores as the mean of their indicators (row-wise)."""
    if df is None:
        df = load_raw()
    return pd.DataFrame({c: df[items].mean(axis=1) for c, items in CONSTRUCTS.items()})


def zscore(a, axis=0):
    a = np.asarray(a, dtype=float)
    return (a - a.mean(axis=axis)) / a.std(axis=axis, ddof=1)


def save_table(df, name, index=True):
    path = os.path.join(TBL, name)
    df.to_csv(path, index=index)
    return path
