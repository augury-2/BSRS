# MTVS Study — PLS-SEM & fsQCA Analysis

Reproducible analysis of `MTVS.xlsx` (N = 312): User Engagement (UE), User Experience (UX),
Brand Satisfaction (BSAT), Brand Success (BSUC).

## Contents
| File | Purpose |
|---|---|
| `REPORT.md` | **Publication-ready manuscript** (Parts A–P): Results, Discussion, Conclusion, Supplementary, References (APA 7). Start here. |
| `common.py` | Data loading, construct (mean) composites, model specification. |
| `plssem.py` | From-scratch PLS-SEM estimator (Mode A): loadings, weights, reliability (α, ρ_A, CR), AVE, HTMT, Fornell–Larcker, VIF, f², model fit. |
| `fsqca.py` | From-scratch fsQCA toolkit: direct calibration, necessity, truth table (raw/PRI consistency), Quine–McCluskey minimisation. |
| `run_screening.py` | Part A — data screening + figures A1–A9. |
| `run_pls.py` | Parts B/C/D/E/F/I — measurement & structural model, 5,000-sample bootstrap, mediation, R²/Q²/f²/PLSpredict, IPMA. |
| `run_fsqca.py` | Parts H/J/K — calibration, necessity, truth table, minimisation, robustness. |
| `run_figures.py` | Part L — all PLS/fsQCA figures (L1–L12). |
| `tables/` | All result tables (CSV). |
| `figures/` | All figures (PNG, 150 dpi). |

## Reproduce
```bash
pip install pandas numpy scipy matplotlib seaborn openpyxl statsmodels scikit-learn
cd analysis
python run_screening.py   # Part A
python run_pls.py         # Parts B,C,D,E,F,I  (5000 bootstrap; ~3 min)
python run_fsqca.py       # Parts H,J,K
python run_figures.py     # Part L
```
Bootstrap seed = 20240625 (PLS), 99 / 7 (fsQCA, k-fold) for exact reproducibility.

## Headline result
Measurement model excellent (α/ρ_A/CR = .90–.95; AVE = .77–.79; HTMT ≤ .094), but the four
constructs are **mutually orthogonal** (|r| ≤ .083). Therefore all structural paths are
non-significant, R² ≤ .008, Q² < 0, and fsQCA finds no necessary conditions and no sufficient
configurations. All hypotheses (H1–H3) and Proposition P1 are **not supported**. See `REPORT.md`.
