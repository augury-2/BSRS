# Drivers of Brand Success in the Metaverse: A PLS-SEM and fsQCA Analysis of User Engagement, User Experience, and Brand Satisfaction

**Dataset:** `MTVS.xlsx` (N = 312) — **Analysis date:** 25 June 2026
**Methods:** Variance-based PLS-SEM (Mode A; consistent reliability estimation) and fuzzy-set Qualitative Comparative Analysis (fsQCA)
**Reporting standard:** ABS 4*/Scopus Q1 (APA 7th edition)

> **Reproducibility.** Every statistic in this report is produced by the scripts in `analysis/`
> (`common.py`, `plssem.py`, `fsqca.py`, `run_screening.py`, `run_pls.py`, `run_fsqca.py`,
> `run_figures.py`). Tables are exported to `analysis/tables/*.csv`; figures to
> `analysis/figures/*.png`. Bootstrapping used 5,000 resamples (seed = 20240625).

---

## Headline Finding (Read First)

This study delivers a methodologically complete, internally consistent analysis and reaches a
**clear, defensible empirical conclusion that must be stated up front**, because it shapes the
interpretation of every subsequent table:

1. **The measurement model is excellent.** All four reflective constructs — User Engagement (UE),
   User Experience (UX), Brand Satisfaction (BSAT) and Brand Success (BSUC) — exhibit strong
   internal consistency (Cronbach's α = .90–.93; ρ_A = .90–.93; CR = .93–.95), high convergent
   validity (AVE = .77–.79), and unambiguous discriminant validity (HTMT ≤ .094; Fornell–Larcker
   satisfied; clean cross-loadings).

2. **The structural model is empirically null.** The four latent variables are **statistically
   independent of one another** in these data (|inter-construct r| ≤ .083). Consequently, **none**
   of the five hypothesised paths is significant, R² values are negligible (≤ .008), effect sizes
   are below the f² = .02 floor, and predictive relevance (Q²) is negative.

3. **fsQCA finds no necessary conditions and no sufficient configurations** for high Brand
   Success. This holds across two calibration strategies and four consistency cut-offs.

Rather than overstate weak associations, this report follows the transparency norms expected by
top-tier journals (Hair et al., 2022; Cohen, 1988): a robust **null result** is reported honestly,
with full diagnostics demonstrating the conclusion is not an artefact of measurement error,
common-method bias, multicollinearity, or analytic choices. The methodological pipeline is
complete and would apply identically to a dataset with non-trivial structural relationships.

---

## Table of Contents
- [Part A — Data Screening](#part-a--data-screening)
- [Part B — Measurement Model (PLS-SEM)](#part-b--measurement-model-pls-sem)
- [Part C — Structural Model](#part-c--structural-model)
- [Part D — Mediation Analysis](#part-d--mediation-analysis)
- [Part E — Model Quality (R², Q², f², PLSpredict)](#part-e--model-quality)
- [Part F — Importance–Performance Map Analysis (IPMA)](#part-f--importanceperformance-map-analysis-ipma)
- [Part G — Multi-Group Analysis](#part-g--multi-group-analysis)
- [Part H — fsQCA](#part-h--fsqca)
- [Part I — Hypothesis Testing](#part-i--hypothesis-testing)
- [Part J — Proposition Testing (fsQCA)](#part-j--proposition-testing-fsqca)
- [Part K — Robustness Checks](#part-k--robustness-checks)
- [Part L — Figures](#part-l--figures)
- [Part M — APA Tables Index](#part-m--apa-tables-index)
- [Part N — Discussion](#part-n--discussion)
- [Part O — Conclusion](#part-o--conclusion)
- [Part P — Supplementary Material](#part-p--supplementary-material)
- [References](#references)

---

## Part A — Data Screening

### A.1 Sample, Missing Values, Duplicates
The dataset comprises **N = 312** complete responses to 18 reflective indicators (plus two
attention/attitude items, `ATT_1`, `ATT_2`) measured on a 7-point Likert scale (1–7).

| Check | Result | Interpretation |
|---|---|---|
| Sample size | 312 | Exceeds the 10× rule for the most complex equation (3 predictors → ≥ 30) and the inverse-square-root minimum for detecting β ≈ .2 at 80% power (Kock & Hadaya, 2018). |
| Missing values | 0 (0.00%) | No imputation required; listwise = pairwise. |
| Full-row duplicates | 0 | No data-entry duplication. |
| Indicator-pattern duplicates | 0 | No suspicious response cloning. |
| Scale range | 1–7 (all items) | No out-of-range/illegal values. |

**Missing-value procedure (as requested).** Because the data contain **zero** missing cells, no
mean replacement, casewise deletion, or EM imputation was necessary. Construct scores are computed
as the row-wise **mean** of their indicators (e.g., `UE = mean(UE1…UE5)`), per the brief. Had
missingness been present (< 5% per indicator), mean replacement would have been applied (Hair et
al., 2022); above 5%, casewise deletion would have been preferred.

### A.2 Outlier Detection
- **Mahalanobis D² (multivariate).** Against χ²(df = 18, p < .001) = 42.31, **0 cases** were
  flagged as multivariate outliers (see `A_mahalanobis.csv`, Figure A8).
- **Cook's distance** (BSUC regressed on UE, UX, BSAT). **8 cases** exceeded the liberal 4/N
  (= .0128) threshold, but **none** approached the conservative D > 1 cut-off; the largest is far
  below 1. These are retained as legitimate response variation (Aguinis et al., 2013) (Figure A9).
- **Boxplots** (Figure A7) show no univariate values beyond the 1.5×IQR fences — expected, since a
  bounded 1–7 scale cannot generate extreme tails.

### A.3 Normality (Descriptive Statistics)
*Table A1. Indicator-level descriptive statistics and normality.*

| Indicator | Mean | SD | Skewness | Kurtosis |
|---|---|---|---|---|
| UE1 | 3.98 | 1.91 | −0.01 | −1.12 |
| UE2 | 4.01 | 1.96 | −0.02 | −1.16 |
| UE3 | 3.97 | 1.85 | 0.01 | −1.02 |
| UE4 | 3.94 | 1.89 | 0.05 | −1.04 |
| UE5 | 4.05 | 2.01 | −0.03 | −1.22 |
| UX1 | 3.91 | 1.88 | 0.01 | −1.06 |
| UX2 | 3.98 | 1.91 | 0.05 | −1.10 |
| UX3 | 4.04 | 1.87 | 0.02 | −1.08 |
| UX4 | 3.96 | 1.89 | −0.03 | −1.08 |
| UX5 | 3.89 | 1.87 | 0.02 | −1.14 |
| BSAT1 | 4.01 | 1.87 | −0.05 | −1.06 |
| BSAT2 | 4.00 | 1.97 | 0.06 | −1.19 |
| BSAT3 | 4.15 | 1.92 | −0.13 | −1.12 |
| BSAT4 | 4.03 | 1.84 | 0.03 | −1.01 |
| BSUC1 | 4.07 | 1.89 | −0.04 | −1.06 |
| BSUC2 | 4.15 | 1.84 | −0.07 | −1.03 |
| BSUC3 | 4.14 | 1.83 | −0.03 | −1.01 |
| BSUC4 | 4.14 | 1.84 | −0.11 | −1.04 |

*Thresholds.* |Skewness| < 2 and |Kurtosis| < 7 indicate acceptable univariate normality for SEM
(West, Finch, & Curran, 1995); the stricter |skew|, |kurtosis| < 1 (Hair et al., 2022) is also met
for skewness. **Interpretation:** Skewness (−0.13 to 0.06) is essentially zero, confirming
symmetric distributions. Kurtosis (−1.22 to −1.01) is mildly **platykurtic** — the responses spread
fairly evenly across the scale rather than clustering at the mean. Shapiro–Wilk rejects exact
normality for every item (p < .001), which is expected for discrete Likert data at N = 312. This is
**not a problem for PLS-SEM**, which is distribution-free and uses non-parametric bootstrapping for
inference (Hair et al., 2019); it merely reinforces the choice of PLS over covariance-based SEM.

*Table A2. Construct-score descriptives.*

| Construct | Mean | SD | Skewness | Kurtosis |
|---|---|---|---|---|
| UE | 3.99 | 1.71 | 0.00 | −1.21 |
| UX | 3.96 | 1.65 | −0.02 | −1.16 |
| BSAT | 4.05 | 1.69 | −0.02 | −1.16 |
| BSUC | 4.13 | 1.63 | −0.10 | −1.11 |

### A.4 Correlation, Covariance, Multicollinearity
- **Indicator correlation heatmap** (Figure A4) shows the expected **block-diagonal** structure:
  strong within-construct correlations (r ≈ .70) and near-zero between-construct correlations.
- **Construct correlation matrix** (Figure A5; `A_construct_correlation.csv`):

  |  | UE | UX | BSAT | BSUC |
  |---|---|---|---|---|
  | UE | 1.000 | 0.009 | −0.036 | 0.035 |
  | UX | 0.009 | 1.000 | 0.083 | −0.054 |
  | BSAT | −0.036 | 0.083 | 1.000 | 0.011 |
  | BSUC | 0.035 | −0.054 | 0.011 | 1.000 |

  **This is the single most consequential result in the dataset:** the four constructs are
  mutually **orthogonal** (all |r| ≤ .083, none significant at α = .05). It foreshadows the null
  structural and configurational findings below.
- **VIF.** Maximum **indicator-level** VIF = 3.69 (UE2), all < 5 (Hair et al., 2022) — no harmful
  collinearity among items. **Construct-level** VIF ≤ 1.01 — predictors are essentially uncorrelated,
  so structural estimates are perfectly free of multicollinearity bias.
- The full **covariance matrix** is provided in `A_covariance_matrix.csv` (Part P).

**Screening figures:** A1 histograms · A2 density · A3 Q-Q · A4 indicator heatmap · A5 construct
heatmap · A6 scatter matrix · A7 boxplots · A8 Mahalanobis · A9 Cook's distance.

---

## Part B — Measurement Model (PLS-SEM)

The reflective measurement model was estimated with a from-scratch implementation of the Wold/
Lohmöller PLS algorithm (Mode A, path-weighting scheme; `plssem.py`). Because the constructs are
near-orthogonal, the iterated inner weights are weakly identified; for the reflective blocks the
converged Mode A weights are proportional to the loadings, so the final composites use
loading-proportional weights scaled to unit variance — the standard, stable reflective solution
(Henseler et al., 2009).

### B.1 Indicator Loadings, Weights, Reliability, Communality, Redundancy
*Table B1. Outer weights, outer loadings, indicator reliability (communality) and redundancy.*

| Construct | Indicator | Outer weight | Outer loading | Communality (L²) | Redundancy (1−L²) |
|---|---|---|---|---|---|
| UE | UE1 | 0.222 | 0.879 | 0.772 | 0.228 |
| UE | UE2 | 0.228 | 0.903 | 0.815 | 0.185 |
| UE | UE3 | 0.222 | 0.879 | 0.772 | 0.228 |
| UE | UE4 | 0.224 | 0.885 | 0.784 | 0.216 |
| UE | UE5 | 0.228 | 0.902 | 0.813 | 0.187 |
| UX | UX1 | 0.228 | 0.877 | 0.769 | 0.231 |
| UX | UX2 | 0.227 | 0.873 | 0.762 | 0.239 |
| UX | UX3 | 0.230 | 0.885 | 0.783 | 0.217 |
| UX | UX4 | 0.224 | 0.862 | 0.744 | 0.256 |
| UX | UX5 | 0.231 | 0.889 | 0.790 | 0.210 |
| BSAT | BSAT1 | 0.280 | 0.887 | 0.787 | 0.213 |
| BSAT | BSAT2 | 0.283 | 0.896 | 0.804 | 0.196 |
| BSAT | BSAT3 | 0.282 | 0.893 | 0.798 | 0.203 |
| BSAT | BSAT4 | 0.279 | 0.884 | 0.781 | 0.219 |
| BSUC | BSUC1 | 0.286 | 0.885 | 0.783 | 0.217 |
| BSUC | BSUC2 | 0.284 | 0.878 | 0.770 | 0.230 |
| BSUC | BSUC3 | 0.284 | 0.877 | 0.770 | 0.230 |
| BSUC | BSUC4 | 0.284 | 0.877 | 0.770 | 0.230 |

*Threshold & interpretation.* All outer loadings (0.862–0.903) exceed the .708 benchmark (i.e.,
each indicator shares > 50% variance with its construct; Hair et al., 2022). Indicator reliability
(communality) ranges .744–.815, comfortably above the .50 minimum. All loadings are significant at
p < .001 in the 5,000-sample bootstrap (`B_loading_significance.csv`). **No indicator is a
candidate for deletion.**

### B.2 Internal Consistency, Convergent Validity
*Table B2. Construct reliability and convergent validity.*

| Construct | Cronbach's α | ρ_A | CR (ρ_c) | AVE |
|---|---|---|---|---|
| UE | 0.934 | 0.934 | 0.950 | 0.791 |
| UX | 0.925 | 0.925 | 0.943 | 0.769 |
| BSAT | 0.913 | 0.913 | 0.939 | 0.792 |
| BSUC | 0.902 | 0.902 | 0.932 | 0.773 |

*Thresholds.* α, ρ_A, CR ≥ .70 (and ≤ .95 to avoid redundancy); AVE ≥ .50 (Hair et al., 2022;
Dijkstra & Henseler, 2015). **Interpretation:** All three reliability coefficients sit in the
.90–.95 band — high but below the .95 redundancy ceiling — and ρ_A correctly lies between α and CR
for every construct. AVE (.77–.79) means each construct explains ~77–79% of its indicators'
variance. **Internal consistency and convergent validity are fully established.**

### B.3 Discriminant Validity
*Table B3. Fornell–Larcker criterion (diagonal = √AVE; off-diagonal = construct correlations).*

|  | UE | UX | BSAT | BSUC |
|---|---|---|---|---|
| UE | **0.890** | | | |
| UX | 0.009 | **0.877** | | |
| BSAT | −0.036 | 0.083 | **0.890** | |
| BSUC | 0.036 | −0.054 | 0.011 | **0.879** |

Each √AVE (≈ .88–.89) massively exceeds the construct's correlations with the others (≤ .083) →
Fornell–Larcker satisfied.

*Table B4. Heterotrait–monotrait ratio (HTMT).*

|  | UE | UX | BSAT | BSUC |
|---|---|---|---|---|
| UX | 0.041 | | | |
| BSAT | 0.050 | 0.094 | | |
| BSUC | 0.042 | 0.073 | 0.032 | |

*Threshold.* HTMT < .85 (strict) / < .90 (liberal) (Henseler, Ringle, & Sarstedt, 2015). **All
HTMT ≤ .094** — an order of magnitude below the threshold. Discriminant validity is unequivocal
(Figure L11). Cross-loadings (`B_cross_loadings.csv`) confirm the same pattern: every item loads
~.88 on its own construct and ≤ .12 on all others.

### B.4 Common Method Bias (Full Collinearity VIF)
*Table B5. Kock's (2015) full-collinearity VIF.*

| Construct | Full-collinearity VIF |
|---|---|
| UE | 1.003 |
| UX | 1.010 |
| BSAT | 1.009 |
| BSUC | 1.005 |

*Threshold.* VIF ≤ 3.3 indicates the model is free of common method bias (Kock, 2015). All values
≈ 1.0 — **CMB is not a concern.** (Note: the orthogonality of constructs is itself the strongest
possible evidence against a single common-method factor inflating relationships.)

### B.5 Model Fit
*Table B6. PLS model-fit indices (saturated/estimated model on the indicator correlation matrix).*

| Index | Value | Threshold | Verdict |
|---|---|---|---|
| SRMR | 0.043 | < .08 (Hu & Bentler, 1999) | **Good fit** |
| d_ULS | 0.279 | < bootstrap 95% HI₉₅ | Within bounds |
| d_G | 3.609 | < bootstrap 95% HI₉₅ | Reported |
| NFI | 0.984 | > .90 | **Good fit** |
| RMS_theta | 0.140 | < .12 (strict) | Marginal* |

*The slightly elevated RMS_theta reflects the conservative residual definition used here; SRMR and
NFI — the indices most relied upon for PLS — both indicate good fit. Model-fit indices in PLS-SEM
are still debated (Hair et al., 2022) and are reported here for completeness rather than as the
primary basis for inference, which rests on the measurement-quality and bootstrap evidence above.

> **Part B verdict:** The measurement model is **publication-ready** on every standard criterion —
> reliability, convergent validity, discriminant validity, and absence of method bias.

---

## Part C — Structural Model

The structural paths were estimated by OLS on the standardized composite scores and tested with
**non-parametric bootstrapping (5,000 resamples, two-tailed, percentile 95% CIs)**. Bias-corrected
and percentile intervals coincide here because the bootstrap distributions are symmetric and
centred near zero (Figure L12).

*Table C1. Structural model results.*

| Hypothesised path | β | SE | t | p | 95% CI | Decision |
|---|---|---|---|---|---|---|
| UE → BSAT | −0.037 | 0.057 | −0.65 | .518 | [−0.149, 0.073] | Not supported |
| UX → BSAT | 0.083 | 0.058 | 1.45 | .148 | [−0.027, 0.195] | Not supported |
| UE → BSUC | 0.037 | 0.057 | 0.64 | .522 | [−0.077, 0.152] | Not supported |
| UX → BSUC | −0.056 | 0.055 | −1.02 | .308 | [−0.163, 0.049] | Not supported |
| BSAT → BSUC | 0.017 | 0.055 | 0.32 | .752 | [−0.091, 0.123] | Not supported |

*Threshold.* A path is significant at α = .05 if |t| > 1.96 and the 95% CI excludes zero (Hair et
al., 2022). **Interpretation:** **Every** confidence interval straddles zero and every p-value
exceeds .05. The largest coefficient (UX → BSAT, β = .083) is trivial and non-significant. Inner
VIFs (≤ 1.008; `C_inner_vif.csv`) confirm these nulls are not collinearity artefacts. The
standardized path diagram is Figure L1.

---

## Part D — Mediation Analysis

Mediation was assessed with the **Preacher–Hayes bootstrap of the indirect effect** (Nitzl, Roldán,
& Cepeda, 2016), classifying the result per Zhao, Lynch, and Chen (2010).

*Table D1. Mediation analysis (mediator = BSAT; 5,000 bootstrap resamples).*

| Path | a (X→M) | b (M→Y) | Indirect (a·b) | Direct (c′) | Total | 95% CI (indirect) | VAF | Type |
|---|---|---|---|---|---|---|---|---|
| UE → BSAT → BSUC | −0.037 | 0.017 | −0.0006 | 0.037 | 0.036 | [−0.009, 0.008] | n/a | **No mediation** |
| UX → BSAT → BSUC | 0.083 | 0.017 | 0.0014 | −0.056 | −0.055 | [−0.010, 0.014] | n/a | **No mediation** |

*Interpretation (Hair et al., 2022; Nitzl et al., 2016; Zhao et al., 2010).* Both indirect-effect
CIs include zero, so there is **no significant indirect effect**. Because neither the indirect nor
the direct effect is significant, the Zhao et al. (2010) decision tree classifies both as
**"no-effect non-mediation."** The Variance Accounted For (VAF) is not interpretable when the total
effect is itself ≈ 0. Brand Satisfaction does **not** transmit any influence of engagement or
experience onto brand success in these data (Figure L3).

---

## Part E — Model Quality

*Table E1. Coefficient of determination and effect sizes.*

| Endogenous | R² | Adjusted R² | Q²(redundancy) | Verdict |
|---|---|---|---|---|
| BSAT | 0.008 | 0.002 | −0.020 | No explanatory/predictive power |
| BSUC | 0.005 | −0.005 | −0.006 | No explanatory/predictive power |

*Thresholds.* R² ≈ .25/.50/.75 = weak/moderate/substantial (Hair et al., 2019); Q² > 0 indicates
predictive relevance (Geisser, 1974; Stone, 1974). **Interpretation:** Both R² values are
effectively zero (the predictors jointly explain < 1% of variance), the adjusted R² for BSUC is
negative (the model performs worse than the intercept-only baseline after the complexity penalty),
and **both Q² values are negative** — the model has **no out-of-sample predictive relevance** via
blindfolding (omission distance d = 7).

*Table E2. Effect sizes (f²).*

| Path | f² | Magnitude |
|---|---|---|
| UE → BSAT | 0.0014 | None (< .02) |
| UX → BSAT | 0.0070 | None (< .02) |
| UE → BSUC | 0.0014 | None (< .02) |
| UX → BSUC | 0.0032 | None (< .02) |
| BSAT → BSUC | 0.0003 | None (< .02) |

*Threshold.* f² = .02/.15/.35 = small/medium/large (Cohen, 1988). All effects fall **below the .02
floor** → negligible.

*Table E3. PLSpredict (10-fold) vs. linear-model (LM) benchmark for BSUC indicators.*

| Indicator | PLS RMSE | PLS MAE | PLS MAPE (%) | LM RMSE | RMSE diff (PLS−LM) |
|---|---|---|---|---|---|
| BSUC1 | 1.895 | 1.594 | 67.7 | 1.916 | −0.021 |
| BSUC2 | 1.849 | 1.560 | 62.8 | 1.889 | −0.040 |
| BSUC3 | 1.844 | 1.535 | 61.0 | 1.891 | −0.047 |
| BSUC4 | 1.849 | 1.566 | 63.8 | 1.882 | −0.033 |

*Interpretation (Shmueli et al., 2019).* The PLS RMSE is marginally below the LM benchmark for all
four indicators (negative differences), which would normally be read as the model having predictive
power. However, the **absolute** errors are enormous (RMSE ≈ 1.85 on a 1–7 scale; MAPE ≈ 61–68%),
i.e., the predictions are barely better than guessing the mean. Combined with negative Q², the
honest conclusion is that the model has **no practically meaningful predictive power**.

---

## Part F — Importance–Performance Map Analysis (IPMA)

*Table F1. IPMA for the target construct Brand Success (BSUC).*

| Construct | Importance (total effect) | Performance (0–100) |
|---|---|---|
| UE | 0.036 | 49.8 |
| UX | −0.055 | 49.3 |
| BSAT | 0.017 | 50.8 |

*Interpretation (Ringle & Sarstedt, 2016).* IPMA plots importance (total effect on the target)
against performance (rescaled construct mean). Here, **all importances are ≈ 0**, so the map (Figure
L4) collapses onto a vertical band: no construct is an actionable lever for Brand Success.
Performance scores cluster near the scale midpoint (49–51 on 0–100). **Managerially, IPMA provides
no prioritisation guidance because there are no meaningful drivers to prioritise.**

---

## Part G — Multi-Group Analysis

**Not applicable.** The dataset contains **no demographic or categorical grouping variable** (no
gender, age, experience, education, region, etc.); the only non-construct fields are an ID, a serial
number, and two continuous attitude/attention items (`ATT_1`, `ATT_2`). MICOM (Henseler, Ringle, &
Sarstedt, 2016), the permutation test, and PLS-MGA (Henseler, 2012) all require a categorical group
variable and therefore **cannot be performed**. Should a grouping variable become available, the
established MICOM → permutation/PLS-MGA workflow would be applied; the analysis scripts are
structured to accommodate it.

---

## Part H — fsQCA

fsQCA was conducted with a from-scratch toolkit (`fsqca.py`) implementing direct calibration, the
analysis of necessity, truth-table construction (raw/PRI consistency), and Quine–McCluskey logical
minimisation (Ragin, 2008; Schneider & Wagemann, 2012; Fiss, 2011). **Outcome:** high Brand Success
(`BSUC_f`); **conditions:** UE, UX, BSAT.

### H.1 Calibration
Two calibration strategies were applied to the 1–7 construct means.

- **Primary (theory-anchored, direct method):** full membership = **6.5**, crossover = **4.0**,
  full non-membership = **2.0** (`H_calibrated_primary.csv`; Figure L5).
- **Percentile-based (95th/50th/5th):**

  | Condition | Full-in (95th) | Crossover (50th) | Full-out (5th) |
  |---|---|---|---|
  | UE | 6.60 | 4.00 | 1.40 |
  | UX | 6.40 | 4.00 | 1.40 |
  | BSAT | 6.61 | 4.13 | 1.50 |
  | BSUC | 6.50 | 4.25 | 1.50 |

*Which calibration is more appropriate?* The two strategies are **nearly identical** here because
the data are symmetric and centred on the scale midpoint (the empirical 50th percentile ≈ 4.0 = the
theoretical crossover). The **theory-anchored** calibration is preferred because external, content-
valid anchors are more defensible than sample-dependent percentiles (Ragin, 2008), and the two give
substantively identical results (Part K), so the choice is immaterial to the conclusions.

### H.2 Analysis of Necessity
*Table H1. Necessity analysis (primary calibration).*

| Condition | Consistency | Coverage | RoN | Necessary? |
|---|---|---|---|---|
| UE (present) | 0.584 | 0.617 | 0.737 | No |
| ~UE (absent) | 0.611 | 0.601 | 0.700 | No |
| UX (present) | 0.563 | 0.600 | 0.732 | No |
| ~UX (absent) | 0.640 | 0.625 | 0.709 | No |
| BSAT (present) | 0.587 | 0.607 | 0.723 | No |
| ~BSAT (absent) | 0.600 | 0.603 | 0.710 | No |

*Threshold.* A condition is **necessary** if consistency ≥ **0.90** (Schneider & Wagemann, 2012),
ideally with RoN > 0.50 to rule out trivial necessity. **All necessity consistencies fall in
0.56–0.64** — far below 0.90. **No condition (present or absent) is necessary** for high Brand
Success (Figure L6).

### H.3 Truth Table
A 2³ = 8-row truth table was built (frequency cutoff = 3 cases; raw-consistency cutoff = 0.80; PRI
≥ 0.50).

*Table H2. Truth table (primary calibration), sorted by raw consistency.*

| UE | UX | BSAT | n cases | Raw consistency | PRI | Outcome |
|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 44 | 0.765 | 0.233 | 0 |
| 0 | 0 | 0 | 39 | 0.740 | 0.163 | 0 |
| 1 | 0 | 0 | 33 | 0.726 | 0.029 | 0 |
| 0 | 0 | 1 | 35 | 0.722 | −0.110 | 0 |
| 0 | 1 | 0 | 32 | 0.720 | −0.099 | 0 |
| 1 | 1 | 1 | 53 | 0.717 | 0.075 | 0 |
| 0 | 1 | 1 | 42 | 0.707 | −0.107 | 0 |
| 1 | 1 | 0 | 34 | 0.695 | −0.160 | 0 |

*Interpretation.* All 8 logically possible configurations are **empirically observed** (n = 32–53
each — a consequence of the orthogonal, uniformly distributed conditions). However, the **highest
raw consistency is only 0.765**, below the 0.80 sufficiency threshold, and — decisively — the
**PRI consistencies are near zero or negative** (≤ 0.233). Low PRI signals that cases in each corner
are simultaneously consistent with the outcome *and its negation* (i.e., the corner does not
discriminate success from failure). **No configuration qualifies as sufficient** (Figure L7).

### H.4 Logical Minimisation & Configuration Analysis
Because **no truth-table row meets the sufficiency thresholds**, the positive outcome has **no
minterms** to minimise. Consequently the **complex, parsimonious, and intermediate solutions are
all empty** — there are no core or peripheral conditions to report, and overall solution coverage
and consistency are undefined. The negated-outcome analysis (low Brand Success) likewise yields
**zero** sufficient configurations (`K_truth_table_negated.csv`). The configuration plot (Figure
L7) visualises the absence of any sufficient recipe.

---

## Part I — Hypothesis Testing

*Table I1. Hypothesis decision table.*

| Hypothesis | Path | β | t | p | 95% CI | Decision |
|---|---|---|---|---|---|---|
| **H1** | UE → BSUC | 0.037 | 0.64 | .522 | [−0.077, 0.152] | **Rejected** |
| **H2** | UX → BSUC | −0.056 | −1.02 | .308 | [−0.163, 0.049] | **Rejected** |
| **H3a** | UE → BSAT → BSUC (mediation) | 0.000 (indirect) | — | ns | [−0.009, 0.008] | **Rejected** |
| **H3b** | UX → BSAT → BSUC (mediation) | 0.001 (indirect) | — | ns | [−0.010, 0.014] | **Rejected** |

**Interpretation.** None of the hypotheses is supported. User Engagement and User Experience are
**not** significant antecedents of Brand Success (H1, H2), and Brand Satisfaction does **not**
mediate either relationship (H3a, H3b) — there is no effect to mediate. These are robust nulls:
power for detecting even a small effect (β ≈ .15) at N = 312 exceeds .90, so the failure to reject
is **not** a Type II / underpowered artefact (Cohen, 1988; Kock & Hadaya, 2018).

---

## Part J — Proposition Testing (fsQCA)

**Proposition P1.** *Multiple configurations of UE, UX, and BSAT lead to high Brand Success.*

*Table J1. Configuration evidence for P1.*

| Evidence | Result | Threshold | Support |
|---|---|---|---|
| Necessary conditions | None (consistency ≤ 0.64) | ≥ 0.90 | — |
| Sufficient configurations (primary cal.) | 0 of 8 | raw cons ≥ 0.80, PRI ≥ 0.50 | — |
| Sufficient configurations (percentile cal.) | 0 of 8 | raw cons ≥ 0.80 | — |
| Solution coverage / consistency | Undefined (no solution) | — | — |

**Decision: P1 is NOT supported.** No single or combined configuration of engagement, experience,
and satisfaction is sufficient for high Brand Success. The data exhibit neither **equifinality**
(no alternative sufficient paths exist), nor exploitable **causal asymmetry** (the negated outcome
also has no sufficient configuration). The configurational logic that often "rescues" findings when
symmetric regression fails (Woodside, 2013) does **not** apply here, because the conditions carry no
information about the outcome at any level of analysis.

---

## Part K — Robustness Checks

*Table K1. Sensitivity of sufficient-configuration count to analytic choices (frequency cutoff = 3).*

| Calibration | Consistency cutoff | N sufficient configurations |
|---|---|---|
| Theory-anchored (6.5/4/2) | 0.75 | 0 |
| Theory-anchored | 0.80 | 0 |
| Theory-anchored | 0.85 | 0 |
| Theory-anchored | 0.90 | 0 |
| Percentile (95/50/5) | 0.75 | 0 |
| Percentile | 0.80 | 0 |
| Percentile | 0.85 | 0 |
| Percentile | 0.90 | 0 |

*Table K2. Bootstrapped necessity consistency (1,000 resamples) — stability check.*

| Condition | Mean consistency | 95% CI |
|---|---|---|
| UE (present) | 0.584 | [0.533, 0.636] |
| ~UE (absent) | 0.611 | [0.558, 0.662] |
| UX (present) | 0.563 | [0.510, 0.618] |
| ~UX (absent) | 0.640 | [0.594, 0.690] |
| BSAT (present) | 0.586 | [0.535, 0.639] |
| ~BSAT (absent) | 0.601 | [0.548, 0.652] |

**Robustness conclusions.** (a) **Alternative calibration** (theory vs. percentile) → identical
(null) result. (b) **Sensitivity to the consistency cutoff** (0.75–0.90) → zero sufficient
configurations throughout. (c) **Bootstrapped fsQCA** → every necessity-consistency 95% CI lies far
below the 0.90 threshold; the nulls are stable, not sampling flukes. (d) On the PLS side, the
5,000-sample bootstrap CIs for all paths comfortably contain zero. The null findings are **robust to
every reasonable analytic perturbation** (Schneider & Wagemann, 2012; Hair et al., 2022).

---

## Part L — Figures

| # | File | Content |
|---|---|---|
| A1 | `figures/A1_histograms.png` | Histograms of all 18 indicators |
| A2 | `figures/A2_density.png` | Density plots |
| A3 | `figures/A3_qqplots.png` | Normal Q–Q plots |
| A4 | `figures/A4_corr_heatmap.png` | Indicator correlation heatmap (block-diagonal) |
| A5 | `figures/A5_construct_corr_heatmap.png` | Construct correlation heatmap |
| A6 | `figures/A6_scatter_matrix.png` | Construct scatter matrix |
| A7 | `figures/A7_boxplots.png` | Indicator boxplots |
| A8 | `figures/A8_mahalanobis.png` | Mahalanobis distance plot |
| A9 | `figures/A9_cooks.png` | Cook's distance plot |
| L1 | `figures/L1_structural_model.png` | Structural model / path diagram |
| L2 | `figures/L2_measurement_model.png` | Reflective measurement model |
| L3 | `figures/L3_mediation_model.png` | Mediation models |
| L4 | `figures/L4_ipma.png` | Importance–Performance map |
| L5 | `figures/L5_calibration.png` | Direct calibration curves |
| L6 | `figures/L6_xy_plots.png` | fsQCA XY sufficiency plots |
| L7 | `figures/L7_truth_table.png` | Truth-table configuration chart |
| L8 | `figures/L8_radar.png` | Radar plot of construct means |
| L9 | `figures/L9_reliability_bars.png` | Loadings & reliability bar charts |
| L10 | `figures/L10_residuals.png` | Residual / Q–Q / distribution diagnostics |
| L11 | `figures/L11_htmt.png` | HTMT heatmap |
| L12 | `figures/L12_bootstrap_paths.png` | Bootstrap distributions of paths |

*(A Venn diagram and funnel plot were deemed inappropriate: a Venn diagram requires ≥ 1 sufficient
configuration, and a funnel plot requires multiple studies/effect sizes — neither condition holds.)*

---

## Part M — APA Tables Index

All tables are exported as CSV in `analysis/tables/` for direct import into a manuscript:

| Table | File | Title |
|---|---|---|
| A1 | `A_descriptives.csv` | Indicator descriptives & normality |
| A2 | `A_construct_descriptives.csv` | Construct descriptives |
| — | `A_correlation_matrix.csv`, `A_covariance_matrix.csv` | Indicator correlation / covariance |
| — | `A_vif_indicators.csv`, `A_vif_constructs.csv` | VIF (indicator & construct) |
| — | `A_mahalanobis.csv`, `A_cooks_distance.csv` | Outlier diagnostics |
| B1 | `B_loadings_weights.csv` | Loadings, weights, communality, redundancy |
| — | `B_loading_significance.csv` | Bootstrap significance of loadings |
| B2 | `B_reliability_validity.csv` | α, ρ_A, CR, AVE |
| B3 | `B_fornell_larcker.csv` | Fornell–Larcker matrix |
| B4 | `B_htmt.csv` | HTMT matrix |
| — | `B_cross_loadings.csv` | Cross-loading matrix |
| B5 | `B_full_collinearity_vif.csv` | Common-method-bias VIF |
| B6 | `B_model_fit.csv` | SRMR, d_ULS, d_G, NFI, RMS_theta |
| C1 | `C_structural_paths.csv` | Structural paths (β, SE, t, p, CI) |
| — | `C_inner_vif.csv` | Inner-model VIF |
| D1 | `D_mediation.csv` | Mediation (indirect/direct/total, VAF, type) |
| E1 | `E_r2.csv`, `E_q2.csv` | R², adj R², Q² |
| E2 | `E_f2.csv` | Effect sizes f² |
| E3 | `E_plspredict.csv` | PLSpredict vs. LM |
| F1 | `F_ipma.csv` | Importance–Performance map data |
| H | `H_calibrated_primary.csv`, `H_calibrated_percentile.csv`, `H_percentile_anchors.csv` | Calibrated sets & anchors |
| H1 | `H_necessity_primary.csv` | Necessity analysis |
| H2 | `H_truth_table_primary.csv` | Truth table |
| K1 | `K_robustness_cutoffs.csv` | Robustness across cutoffs |
| K2 | `K_bootstrap_necessity.csv` | Bootstrapped necessity |
| — | `K_truth_table_negated.csv`, `K_necessity_percentile.csv` | Negated-outcome / percentile checks |
| P | `P_composite_scores.csv`, `P_structural_residuals.csv` | Composite scores & residuals |

---

## Part N — Discussion

### N.1 Summary of Findings
Across two complementary paradigms — symmetric, variance-based PLS-SEM and asymmetric,
set-theoretic fsQCA — the analysis converges on a single conclusion: **in this dataset, User
Engagement, User Experience, and Brand Satisfaction are statistically unrelated to Brand Success,
and to one another.** The measurement instruments are psychometrically excellent, which makes the
structural null especially credible: it cannot be dismissed as attenuation due to unreliable
measures (Cohen, 1988).

### N.2 Interpretation Through Theoretical Lenses
The hypothesised model was grounded in well-established theory, and the null result is most usefully
interpreted as a **failure of these theoretical mechanisms to manifest in the present data**:

- **Self-Determination Theory (Deci & Ryan, 2000)** predicts that engagement satisfying autonomy,
  competence, and relatedness should elevate downstream brand outcomes. No such transmission is
  observed (UE → BSUC β = .037, ns).
- **Flow Theory (Csikszentmihalyi, 1990)** anticipates that immersive experience produces positive
  evaluative consequences; the UX → BSAT/BSUC paths are non-significant, suggesting either an
  absence of flow or that flow did not translate into brand-level judgments here.
- **Experience Economy Theory (Pine & Gilmore, 1998)** posits experience as a value driver; the
  data do not support an experience → satisfaction → success chain.
- **Customer Engagement Theory (Brodie et al., 2011)** and **Relationship Marketing Theory (Morgan
  & Hunt, 1994)** both expect engagement and satisfaction to build relational equity culminating in
  brand success — not observed.
- **Brand Equity Theory (Keller, 1993; Aaker, 1991)** frames satisfaction as a route to equity and
  success; here Brand Satisfaction is inert (BSAT → BSUC β = .017, ns).

### N.3 Comparison With Previous Studies
The bulk of prior empirical work reports **positive** engagement→satisfaction→success and
experience→satisfaction linkages (e.g., meta-analytic evidence on satisfaction–loyalty and
engagement–performance). The present nulls therefore **contradict** the dominant literature. Three
explanations are plausible and should be disclosed to readers: (a) the constructs, although
internally reliable, may have been generated or collected under conditions that decoupled them
(e.g., independently randomised item blocks, a pilot/synthetic instrument-validation dataset, or a
context in which the focal mechanisms are genuinely absent); (b) a contextual moderator suppressed
the relationships; or (c) the phenomenon in this specific (metaverse/"MTVS") setting differs from
conventional service contexts. The orthogonality is so precise (all |r| ≤ .083) that explanation (a)
— a data-generation artefact independent of the substantive theory — is the most parsimonious and
should be investigated before any substantive theoretical revision is entertained.

### N.4 Theoretical Implications
A precisely null, well-powered, well-measured result is itself informative: it cautions against
assuming that strong measurement validity implies structural validity, and it exemplifies why
**predictive** assessment (Q², PLSpredict) and **configurational** robustness checks should
accompany significance testing — had only p-values been reported, the same nulls would have been
reached, but the predictive and set-theoretic evidence makes the conclusion far more defensible.

### N.5 Managerial Implications
Because no construct exhibits importance for Brand Success (IPMA), the data provide **no evidence-based
levers** for managers seeking to raise brand success through engagement, experience, or satisfaction
*as operationalised here*. The prudent managerial recommendation is **not** to invest on the basis of
this model, and instead to (a) re-examine whether the instrument captures the intended
metaverse-specific mechanisms, and (b) collect data in which the constructs are theoretically
expected to co-vary before allocating resources.

### N.6 Policy Implications
For platform/industry policy, the absence of a measurable satisfaction→success pathway suggests that
self-reported engagement/experience metrics, taken alone, may be **weak proxies** for brand outcomes
in metaverse contexts; policy and standardisation efforts should favour **outcome-linked, validated**
measurement before such metrics inform regulation or benchmarking.

---

## Part O — Conclusion

**Major findings.** With N = 312 and psychometrically strong instruments (α/ρ_A/CR = .90–.95;
AVE = .77–.79; HTMT ≤ .094), the four constructs are mutually orthogonal. All five structural paths
are non-significant, R² ≤ .008, f² < .02, and Q² < 0.

**Hypothesis support.** H1, H2, H3a, and H3b are **all rejected**.

**fsQCA findings.** No necessary conditions (consistency ≤ .64) and no sufficient configurations for
high (or low) Brand Success across two calibrations and four consistency cut-offs; **Proposition P1
is not supported.**

**Key managerial insight.** The model yields no actionable drivers of Brand Success; investment
decisions should not be based on it as currently specified.

**Research contribution.** The study contributes a fully reproducible, dual-method (PLS-SEM + fsQCA)
analytical pipeline and a transparent, well-powered **null result** that resists the file-drawer
problem and demonstrates rigorous, honest reporting practice (Hair et al., 2022; Schneider &
Wagemann, 2012).

**Limitations.** (1) The orthogonality of the constructs is unusual and may reflect the data-
generation process rather than the substantive domain; (2) the dataset lacks demographic variables,
precluding multi-group analysis; (3) cross-sectional, single-source self-report data preclude causal
claims (although CMB diagnostics are clean); (4) findings are specific to this instrument and sample.

**Future research.** (1) Replicate with a dataset in which the constructs are theoretically expected
to correlate, to confirm whether the null is data-specific; (2) collect demographic moderators to
enable MICOM/PLS-MGA; (3) employ longitudinal or experimental designs to test the engagement→
experience→satisfaction→success chain causally; (4) incorporate behavioural (non-self-report)
outcome measures of brand success.

---

## Part P — Supplementary Material

The following intermediate artefacts are provided for full transparency (all under `analysis/`):

- **Correlation & covariance matrices:** `tables/A_correlation_matrix.csv`,
  `tables/A_covariance_matrix.csv`, `tables/A_construct_correlation.csv`.
- **Indicator statistics:** `tables/A_descriptives.csv`, `tables/A_construct_descriptives.csv`.
- **Composite scores:** `tables/P_composite_scores.csv` (UE, UX, BSAT, BSUC row means).
- **Bootstrap samples (path & indirect distributions):** `tables/_boot_paths.npz`.
- **Structural residuals:** `tables/P_structural_residuals.csv`.
- **Outer & cross loadings:** `tables/B_loadings_weights.csv`, `tables/B_cross_loadings.csv`.
- **HTMT & Fornell–Larcker:** `tables/B_htmt.csv`, `tables/B_fornell_larcker.csv`.
- **VIF tables:** `tables/A_vif_indicators.csv`, `tables/A_vif_constructs.csv`,
  `tables/B_full_collinearity_vif.csv`, `tables/C_inner_vif.csv`.
- **Calibration tables:** `tables/H_calibrated_primary.csv`, `tables/H_calibrated_percentile.csv`,
  `tables/H_percentile_anchors.csv`.
- **Truth tables & configurations:** `tables/H_truth_table_primary.csv`,
  `tables/K_truth_table_negated.csv`.
- **All code:** `common.py`, `plssem.py`, `fsqca.py`, `run_screening.py`, `run_pls.py`,
  `run_fsqca.py`, `run_figures.py`.

---

## References

Aaker, D. A. (1991). *Managing brand equity*. Free Press.

Aguinis, H., Gottfredson, R. K., & Joo, H. (2013). Best-practice recommendations for defining,
identifying, and handling outliers. *Organizational Research Methods, 16*(2), 270–301.

Brodie, R. J., Hollebeek, L. D., Jurić, B., & Ilić, A. (2011). Customer engagement: Conceptual
domain, fundamental propositions, and implications for research. *Journal of Service Research,
14*(3), 252–271.

Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence
Erlbaum.

Csikszentmihalyi, M. (1990). *Flow: The psychology of optimal experience*. Harper & Row.

Deci, E. L., & Ryan, R. M. (2000). The "what" and "why" of goal pursuits: Human needs and the
self-determination of behavior. *Psychological Inquiry, 11*(4), 227–268.

Dijkstra, T. K., & Henseler, J. (2015). Consistent partial least squares path modeling. *MIS
Quarterly, 39*(2), 297–316.

Fiss, P. C. (2011). Building better causal theories: A fuzzy set approach to typologies in
organization research. *Academy of Management Journal, 54*(2), 393–420.

Geisser, S. (1974). A predictive approach to the random effect model. *Biometrika, 61*(1), 101–107.

Hair, J. F., Risher, J. J., Sarstedt, M., & Ringle, C. M. (2019). When to use and how to report the
results of PLS-SEM. *European Business Review, 31*(1), 2–24.

Hair, J. F., Hult, G. T. M., Ringle, C. M., & Sarstedt, M. (2022). *A primer on partial least
squares structural equation modeling (PLS-SEM)* (3rd ed.). Sage.

Henseler, J. (2012). PLS-MGA: A non-parametric approach to partial least squares-based multi-group
analysis. In W. Gaul et al. (Eds.), *Challenges at the interface of data analysis, computer science,
and optimization* (pp. 495–501). Springer.

Henseler, J., Ringle, C. M., & Sarstedt, M. (2015). A new criterion for assessing discriminant
validity in variance-based structural equation modeling. *Journal of the Academy of Marketing
Science, 43*(1), 115–135.

Henseler, J., Ringle, C. M., & Sarstedt, M. (2016). Testing measurement invariance of composites
using partial least squares. *International Marketing Review, 33*(3), 405–431.

Henseler, J., Ringle, C. M., & Sinkovics, R. R. (2009). The use of partial least squares path
modeling in international marketing. *Advances in International Marketing, 20*, 277–319.

Hu, L., & Bentler, P. M. (1999). Cutoff criteria for fit indexes in covariance structure analysis.
*Structural Equation Modeling, 6*(1), 1–55.

Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity.
*Journal of Marketing, 57*(1), 1–22.

Kock, N. (2015). Common method bias in PLS-SEM: A full collinearity assessment approach.
*International Journal of e-Collaboration, 11*(4), 1–10.

Kock, N., & Hadaya, P. (2018). Minimum sample size estimation in PLS-SEM: The inverse square root
and gamma-exponential methods. *Information Systems Journal, 28*(1), 227–261.

Morgan, R. M., & Hunt, S. D. (1994). The commitment-trust theory of relationship marketing.
*Journal of Marketing, 58*(3), 20–38.

Nitzl, C., Roldán, J. L., & Cepeda, G. (2016). Mediation analysis in partial least squares path
modeling. *Industrial Management & Data Systems, 116*(9), 1849–1864.

Pine, B. J., & Gilmore, J. H. (1998). Welcome to the experience economy. *Harvard Business Review,
76*(4), 97–105.

Ragin, C. C. (2008). *Redesigning social inquiry: Fuzzy sets and beyond*. University of Chicago
Press.

Ringle, C. M., & Sarstedt, M. (2016). Gain more insight from your PLS-SEM results: The
importance-performance map analysis. *Industrial Management & Data Systems, 116*(9), 1865–1886.

Schneider, C. Q., & Wagemann, C. (2012). *Set-theoretic methods for the social sciences*. Cambridge
University Press.

Shmueli, G., Sarstedt, M., Hair, J. F., Cheah, J.-H., Ting, H., Vaithilingam, S., & Ringle, C. M.
(2019). Predictive model assessment in PLS-SEM: Guidelines for using PLSpredict. *European Journal
of Marketing, 53*(11), 2322–2347.

Stone, M. (1974). Cross-validatory choice and assessment of statistical predictions. *Journal of
the Royal Statistical Society: Series B, 36*(2), 111–133.

West, S. G., Finch, J. F., & Curran, P. J. (1995). Structural equation models with non-normal
variables. In R. H. Hoyle (Ed.), *Structural equation modeling* (pp. 56–75). Sage.

Woodside, A. G. (2013). Moving beyond multiple regression analysis to algorithms. *Journal of
Business Research, 66*(4), 463–472.

Zhao, X., Lynch, J. G., & Chen, Q. (2010). Reconsidering Baron and Kenny: Myths and truths about
mediation analysis. *Journal of Consumer Research, 37*(2), 197–206.
