# BSRS analysis pipeline (PLS-SEM + fsQCA)

Reproducible analysis of `Responses.xlsx` (N = 312, 7-point Likert).
Constructs: **UE** (User Engagement), **UX** (User Experience),
**BSAT** (Brand-System Satisfaction), **BSUC** (Brand-System Use Continuance,
outcome). `ATT_1`/`ATT_2` are attention-check items and are excluded from the
models (see `../RESULTS.md`).

## Setup

```bash
pip install -r analysis/requirements.txt   # scikit-learn pinned <1.6
```

## Run order (from the repository root)

```bash
PYTHONPATH=analysis python analysis/01_screening.py          # screening, EFA, CMB
PYTHONPATH=analysis python analysis/02_measurement_model.py  # measurement model + plspm cross-check
PYTHONPATH=analysis python analysis/03_structural_model.py   # paths, bootstrap, f2, Q2, SRMR, mediation, IPMA
PYTHONPATH=analysis python analysis/03b_plspredict.py        # out-of-sample PLSpredict (10-fold CV)
PYTHONPATH=analysis python analysis/04_fsqca.py              # calibration, necessity, sufficiency, robustness
PYTHONPATH=analysis python analysis/05_figures.py            # all 300-dpi figures
```

Numeric tables are written to `analysis/outputs/*.csv` (and `*.json` summaries);
figures to `analysis/figures/*.png`. The narrative write-up is in `../RESULTS.md`.

## Engines

- `pls_engine.py` — transparent Mode A (reflective) PLS-SEM (Wold/Lohmöller,
  factorial inner scheme); loadings/weights, reliability (α, ρ_A, ρ_c), AVE,
  HTMT, Fornell-Larcker, cross-loadings, VIF, R²/f²/Q², SRMR, and nonparametric
  bootstrap. Validated against `plspm` (max loading discrepancy 0.003).
- `fsqca_engine.py` — direct-method calibration, set-theoretic consistency /
  coverage / PRI, necessity analysis, truth-table construction, and
  Quine-McCluskey minimisation (complex / parsimonious / intermediate solutions).

## Note: plspm + pandas 3.x

The cross-validation in `02_measurement_model.py` uses `plspm`, which contains a
trailing-comma `.loc` indexing call that breaks on pandas >= 3. If you hit a
`ValueError: zip() argument 2 is longer than argument 1`, patch the installed
package once:

```python
# site-packages/plspm/inner_model.py  (~line 75)
# -    ivs = path.loc[dv,][path.loc[dv,] == 1].index
# +    ivs = path.loc[dv, :][path.loc[dv, :] == 1].index
```

This affects only the optional external validation, not the custom engine results.
