# Results

This section reports the empirical findings in two stages. First, a variance‑based
structural equation model (partial least squares; PLS‑SEM) is used to test the
net, symmetric effects of the antecedents on brand‑system continuance. Second, a
fuzzy‑set qualitative comparative analysis (fsQCA) is used to identify the
configurations of conditions that are sufficient for high (and for low)
continuance. The combination follows the now‑established recommendation in the
information‑systems literature to triangulate correlational (PLS‑SEM) and
configurational (fsQCA) logics, because the two approaches answer complementary
questions: PLS‑SEM estimates the *average marginal* contribution of each
antecedent, whereas fsQCA recovers the *combinations* of antecedents that are
jointly sufficient for the outcome and explicitly allows for equifinality and
causal asymmetry (Ragin, 2008; Woodside, 2013; Pappas & Woodside, 2021).

Throughout, the constructs are:

| Code | Construct | Items |
|------|-----------|-------|
| **UE** | User Engagement | UE1–UE5 |
| **UX** | User Experience | UX1–UX5 |
| **BSAT** | Brand‑System Satisfaction | BSAT1–BSAT4 |
| **BSUC** | Brand‑System Use Continuance (outcome) | BSUC1–BSUC4 |

> **Note on the two ATT items.** The instrument also contained two items labelled
> `ATT_1` and `ATT_2`. Inspection of their distributions and inter‑item behaviour
> shows that they do not behave as a reflective construct: `ATT_1` is almost
> invariant (M = 5.90, SD = 0.53; ≈ 95% of respondents selected the same point),
> `ATT_2` is low and right‑skewed (M = 2.10), and the two correlate at
> *r* = −.005 with each other and ≈ 0 with every substantive item (see Figure A1).
> This is the signature of *attention / quality‑control* items rather than a
> latent variable. They were therefore used only for data screening and were
> **excluded from the measurement and structural models** and from the fsQCA. A
> robustness model that forced them into a latent variable produced a construct
> with no convergent validity (AVE ≈ 0, non‑significant loadings) and changed none
> of the substantive conclusions.

---

## 1. Sample, data screening, and common method bias

The analysis is based on **N = 312** complete responses measured on seven‑point
Likert scales. There were **no missing values** across the 20 items and **no
straight‑line / invariant response patterns** (all within‑respondent SDs > 0), so
the full sample was retained.

Because PLS‑SEM is a non‑parametric method, multivariate normality is not
required; nonetheless, distributional properties were examined. Shapiro–Wilk
tests rejected univariate normality for all items (*p* < .001), confirming that a
variance‑based estimator is the appropriate analytical choice over covariance‑based
SEM (Hair et al., 2019). Item‑level descriptive statistics are reported in
**Table 1**.

**Table 1. Item descriptive statistics (N = 312).**

| Item | Mean | SD | Median | Min | Max | Skewness | Kurtosis |
|------|------|----|--------|-----|-----|----------|----------|
| UE1 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| UE2 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| UE3 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| UE4 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| UE5 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| UX1 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| UX2 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| UX3 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| UX4 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| UX5 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| BSAT1 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| BSAT2 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| BSAT3 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| BSAT4 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| BSUC1 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| BSUC2 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| BSUC3 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |
| BSUC4 | 4.00 | 2.01 | 4 | 1 | 7 | 0.00 | −1.25 |

*Full numeric precision is provided in `analysis/outputs/T1_item_descriptives.csv`.*

The sampling adequacy of the item set was excellent (Kaiser–Meyer–Olkin = **0.903**)
and Bartlett's test of sphericity was significant (χ²(153) = 3300.5, *p* < .001),
confirming that the correlation matrix is suitable for factor‑analytic treatment.
An exploratory factor analysis (principal‑axis extraction, promax rotation)
recovered a clean **four‑factor structure** that maps exactly onto UE, UX, BSAT
and BSUC, with every substantive item loading > 0.77 on its intended factor and
< 0.13 on all others.

**Common method bias.** Harman's single‑factor test indicated that the first
unrotated factor accounted for **34.4%** of the variance—well below the 50%
threshold—so common method variance is unlikely to be a serious threat
(Podsakoff et al., 2003). This is corroborated by the full collinearity
assessment in the structural model (all inner VIF ≤ 1.35; Section 3 and
Kock, 2015), and by the discriminant‑validity evidence reported below.

> **Transparency note on data provenance.** The 18 substantive items each exhibit
> *identical* marginal moments (mean = 4.000, SD = 2.006, skew = 0, excess
> kurtosis = −1.25), which are exactly the moments of a discrete uniform
> distribution on {1,…,7}. Combined with a realistic, block‑structured correlation
> matrix (Figure A1), this pattern is consistent with data generated by a
> Gaussian‑copula‑type simulation rather than with raw field data. The analyses
> below are reported exactly as the data dictate; if these are synthetic or
> pilot data, the substantive interpretation should be treated as illustrative of
> the analytical pipeline rather than as confirmed empirical fact. This is flagged
> here in the interest of research integrity.

---

## 2. Measurement model assessment

Reflective measurement quality was assessed following the standard sequence for
PLS‑SEM (Hair et al., 2019, 2022): (i) indicator reliability, (ii) internal
consistency reliability, (iii) convergent validity, and (iv) discriminant
validity. The estimation used Mode A (reflective) measurement with the path
weighting scheme. As an external check, the entire measurement model was
re‑estimated with the open‑source `plspm` package; the two implementations agreed
to within 0.003 on every loading and produced identical reliability and AVE
values, confirming that the estimates are not an artefact of a single
implementation.

### 2.1 Indicator reliability and convergent validity

All standardized outer loadings lie between **0.812 and 0.879** (Figure 7),
comfortably above the 0.708 benchmark, so each indicator shares the majority of
its variance with its construct. Average variance extracted (AVE) ranges from
**0.692 to 0.747**, exceeding the 0.50 criterion and establishing convergent
validity for all four constructs (Table 2).

**Table 2. Reliability and convergent validity.**

| Construct | # items | Cronbach's α | ρ_A | Composite reliability (ρ_c) | AVE |
|-----------|:------:|:-----------:|:----:|:---------------------------:|:----:|
| UE   | 5 | 0.889 | 0.892 | 0.918 | 0.692 |
| UX   | 5 | 0.892 | 0.895 | 0.921 | 0.699 |
| BSAT | 4 | 0.885 | 0.887 | 0.921 | 0.743 |
| BSUC | 4 | 0.887 | 0.888 | 0.922 | 0.747 |

Internal consistency is strong and, importantly, **not excessive**: Cronbach's α
(0.885–0.892), the Dijkstra–Henseler ρ_A (0.887–0.895), and composite reliability
ρ_c (0.918–0.922) all sit in the recommended 0.70–0.95 band, indicating reliable
but non‑redundant items. Indicator‑level collinearity is unproblematic (maximum
outer VIF = 2.46 < 3.3). The full loading table is in
`analysis/outputs/T2_outer_loadings.csv`.

> **Figure 7. Indicator outer loadings by construct** (dashed line = 0.708
> threshold). *File:* `analysis/figures/Fig7_outer_loadings.png`.

### 2.2 Discriminant validity

Discriminant validity was established with three complementary criteria.

**Fornell–Larcker criterion (Table 3, Figure 6).** For every construct the square
root of the AVE (diagonal) exceeds its correlations with all other constructs
(off‑diagonal).

**Table 3. Fornell–Larcker matrix** (diagonal in **bold** = √AVE).

|        | UE | UX | BSAT | BSUC |
|--------|:----:|:----:|:----:|:----:|
| **UE**   | **0.832** | | | |
| **UX**   | 0.365 | **0.836** | | |
| **BSAT** | 0.300 | 0.450 | **0.862** | |
| **BSUC** | 0.265 | 0.341 | 0.545 | **0.865** |

**Heterotrait–monotrait ratio (HTMT; Table 4, Figure 5).** All HTMT values fall
between 0.30 and **0.615**, far below the conservative 0.85 threshold
(Henseler et al., 2015). Bootstrap confidence intervals (5,000 resamples) for
every HTMT excluded 1.

**Table 4. HTMT ratios.**

|        | UE | UX | BSAT | BSUC |
|--------|:----:|:----:|:----:|:----:|
| UE   | — | | | |
| UX   | 0.407 | — | | |
| BSAT | 0.334 | 0.503 | — | |
| BSUC | 0.298 | 0.381 | 0.615 | — |

**Cross‑loadings.** Every indicator loads highest on its own construct, with a gap
of at least 0.40 relative to the next‑highest cross‑loading
(`analysis/outputs/T6_cross_loadings.csv`).

Taken together, the three criteria provide consistent evidence of discriminant
validity. The measurement model is therefore sound, and the structural model can
be interpreted with confidence.

> **Figure 5. HTMT heatmap.** *File:* `analysis/figures/Fig5_HTMT.png`.
> **Figure 6. Fornell–Larcker matrix heatmap.** *File:* `analysis/figures/Fig6_FornellLarcker.png`.

---

## 3. Structural model assessment

### 3.1 Collinearity and model fit

Inner‑model collinearity is negligible: all predictor‑side VIFs lie between 1.15
and **1.35** (Table 5), ruling out lateral collinearity and supporting the earlier
conclusion that common method bias does not distort the path estimates
(Kock, 2015). The standardized root mean square residual (**SRMR = 0.047**) is
below the 0.08 cutoff, indicating good approximate fit between the empirical and
model‑implied correlation matrices.

**Table 5. Inner‑model collinearity (VIF).**

| Predictor → Outcome | VIF |
|---------------------|:----:|
| UE → BSAT  | 1.15 |
| UX → BSAT  | 1.15 |
| UE → BSUC  | 1.19 |
| UX → BSUC  | 1.35 |
| BSAT → BSUC | 1.29 |

### 3.2 Explanatory and predictive power

The model explains a meaningful share of variance in the two endogenous
constructs (Table 6, Figure 3): **R² = 0.224** for satisfaction (BSAT) and
**R² = 0.315** for continuance (BSUC). Blindfolding (omission distance = 7) yielded
cross‑validated redundancy **Q² = 0.160** (BSAT) and **0.228** (BSUC), both well
above zero, establishing predictive relevance.

**Table 6. Variance explained and predictive relevance.**

| Construct | R² | Adjusted R² | Q² (blindfolding) |
|-----------|:----:|:----:|:----:|
| BSAT | 0.224 | 0.219 | 0.160 |
| BSUC | 0.315 | 0.308 | 0.228 |

> **Figure 3. R² and Q² of the endogenous constructs.** *File:*
> `analysis/figures/Fig3_R2_Q2.png`.

A formal **out‑of‑sample PLSpredict** analysis (Shmueli et al., 2019; 10‑fold
cross‑validation) confirmed predictive validity for the key target construct: the
prediction error statistic Q²_predict was **positive for all four BSUC
indicators** (0.035–0.067), and the PLS path model produced a lower RMSE than the
naïve linear‑regression benchmark for **three of the four** indicators (Table 7).
This pattern indicates at least **medium out‑of‑sample predictive power**.

**Table 7. PLSpredict (10‑fold CV) for the BSUC indicators.**

| Indicator | Q²_predict | RMSE (PLS) | RMSE (LM) | PLS < LM? |
|-----------|:----:|:----:|:----:|:----:|
| BSUC1 | 0.052 | 1.951 | 1.946 | No |
| BSUC2 | 0.057 | 1.945 | 1.981 | Yes |
| BSUC3 | 0.036 | 1.967 | 2.006 | Yes |
| BSUC4 | 0.067 | 1.935 | 1.953 | Yes |

### 3.3 Path coefficients and hypothesis tests

Path significance was assessed with **bootstrapping (5,000 resamples)**; Table 8
reports standardized coefficients, standard errors, *t*‑statistics, two‑tailed
*p*‑values, 95% percentile confidence intervals, and *f²* effect sizes. The
estimated model is depicted in Figure 1, and the path estimates with their
confidence intervals in Figure 2.

**Table 8. Structural path coefficients (bootstrap, 5,000 resamples).**

| Hypothesis | Path | β | SE | *t* | *p* | 95% CI | *f²* | Decision |
|:----------:|------|:----:|:----:|:----:|:----:|:--------------:|:----:|:--------:|
| H1 | UE → BSAT  | 0.157 | 0.054 | 2.89 | .004 | [0.052, 0.266] | 0.028 | **Supported** |
| H2 | UX → BSAT  | 0.393 | 0.052 | 7.59 | <.001 | [0.291, 0.494] | 0.172 | **Supported** |
| H5 | BSAT → BSUC | 0.476 | 0.047 | 10.15 | <.001 | [0.382, 0.566] | 0.256 | **Supported** |
| H3 | UE → BSUC  | 0.088 | 0.048 | 1.82 | .069 | [−0.004, 0.185] | 0.010 | Not supported |
| H4 | UX → BSUC  | 0.095 | 0.054 | 1.78 | .076 | [−0.008, 0.203] | 0.010 | Not supported |

Three results stand out. **First, satisfaction is the proximal driver of
continuance.** BSAT → BSUC is by far the strongest path (β = 0.476, *p* < .001)
and carries a medium‑to‑large effect (*f²* = 0.256). **Second, experience
dominates engagement as an antecedent of satisfaction.** UX → BSAT (β = 0.393,
*f²* = 0.172, medium) is roughly 2.5× the size of UE → BSAT (β = 0.157,
*f²* = 0.028, small), although both are significant. **Third, neither antecedent
exerts a significant *direct* effect on continuance** once satisfaction is
accounted for (H3 and H4 both have confidence intervals that straddle zero and
negligible *f²* ≈ 0.01). This already foreshadows a mediation story, examined
formally next.

> **Figure 1. PLS‑SEM structural model** with standardized path coefficients
> (solid = significant at *p* < .05, dashed = n.s.; *p* < .05, ** p < .01,
> *** p < .001), and R² for the endogenous constructs. *File:*
> `analysis/figures/Fig1_structural_model.png`.
> **Figure 2. Path estimates with 95% bootstrap confidence intervals.** *File:*
> `analysis/figures/Fig2_path_CIs.png`.

> **Figure 4. f² effect sizes** for all structural paths (reference lines at 0.02,
> 0.15, 0.35). *File:* `analysis/figures/Fig4_f2.png`.

### 3.4 Mediation analysis

Following Zhao et al. (2010) and Nitzl et al. (2016), mediation was tested on the
**bootstrapped indirect effects** rather than by the discredited causal‑steps
procedure. Both specific indirect paths through satisfaction are significant
(Table 9): UE → BSAT → BSUC (indirect = 0.075, *p* = .007, 95% CI [0.024, 0.132])
and UX → BSAT → BSUC (indirect = 0.187, *p* < .001, 95% CI [0.131, 0.251]).

Because in each case the indirect effect is significant while the corresponding
**direct** effect is not (cf. H3, H4 in Table 8), the data indicate
**full (indirect‑only) mediation**: satisfaction fully transmits the influence of
both user experience and user engagement onto continuance. Substantively, neither
a good experience nor active engagement *per se* keeps users on the
brand‑system—they do so **only to the extent that they generate satisfaction**.

**Table 9. Specific indirect effects and total effects on BSUC.**

| Indirect path | Indirect | SE | *t* | *p* | 95% CI | Direct | Total | Type |
|---------------|:----:|:----:|:----:|:----:|:--------------:|:----:|:----:|:----:|
| UE → BSAT → BSUC | 0.075 | 0.027 | 2.72 | .007 | [0.024, 0.132] | 0.088 (n.s.) | 0.162 | Full |
| UX → BSAT → BSUC | 0.187 | 0.030 | 6.15 | <.001 | [0.131, 0.251] | 0.095 (n.s.) | 0.282 | Full |

The **total effects** on continuance rank the antecedents as BSAT (0.476) >
UX (0.282) > UE (0.162), reinforcing that satisfaction is the dominant lever and
experience the dominant upstream antecedent.

### 3.5 Importance–performance map analysis (IPMA)

An IPMA was conducted with BSUC as the target. The *importance* dimension (total
effects) reproduces the ranking above (BSAT > UX > UE; Figure 8). The
*performance* dimension is uninformative in these data because every construct's
rescaled mean sits at the scale midpoint (≈ 50/100), a direct consequence of the
uniform item marginals noted in Section 1. The IPMA is therefore reported for
completeness but **performance‑based prioritization should not be inferred from
this particular sample**; the importance ranking, however, is robust.

> **Figure 8. Importance–performance map (target: BSUC).** *File:*
> `analysis/figures/Fig8_IPMA.png`.

---

## 4. Configurational analysis (fsQCA)

PLS‑SEM estimates the *independent, average* contribution of each antecedent. To
complement this with a *configurational* and *asymmetric* view—i.e., which
*combinations* of conditions are sufficient for high continuance, and whether the
recipe for *low* continuance is simply the mirror image—an fsQCA was conducted
with UE, UX and BSAT as conditions and BSUC as the outcome
(Ragin, 2008; Fiss, 2011; Pappas & Woodside, 2021).

### 4.1 Calibration

Construct scores (item means) were calibrated into fuzzy‑set membership using the
**direct method**, with the three qualitative anchors set at the 95th percentile
(full membership), the 50th percentile (cross‑over / point of maximum ambiguity)
and the 5th percentile (full non‑membership) of each construct (Table 10). Cases
falling exactly on the cross‑over were nudged by 0.001 to avoid loss
(Ragin, 2008). Figure 9 overlays the raw distributions with the resulting
membership functions.

**Table 10. Calibration anchors (direct method, percentile‑based).**

| Construct | Full‑in (P95) | Cross‑over (P50) | Full‑out (P5) |
|-----------|:----:|:----:|:----:|
| UE   | 6.60 | 3.90 | 1.40 |
| UX   | 6.80 | 4.00 | 1.20 |
| BSAT | 6.61 | 4.25 | 1.25 |
| BSUC | 6.75 | 4.00 | 1.25 |

> **Figure 9. fsQCA calibration**: raw composite distributions (bars) and
> fuzzy‑set membership functions (curves). *File:*
> `analysis/figures/Fig9_calibration.png`.

### 4.2 Analysis of necessary conditions

No single condition is **necessary** for high continuance: the highest necessity
consistency is for BSAT (0.751), still below the conventional 0.90 threshold
(Table 11, Figure 11). The same holds for the negation of the outcome, where the
highest necessity consistency is for ~BSAT (0.784). The absence of any necessary
condition is itself an informative result: high continuance does not *require* any
one antecedent in isolation, which is precisely the equifinality premise that
motivates the sufficiency analysis.

**Table 11. Analysis of necessary conditions (consistency threshold = 0.90).**

| Condition | Outcome = high BSUC | | Outcome = ~BSUC | |
|-----------|:----:|:----:|:----:|:----:|
|  | Consistency | Coverage | Consistency | Coverage |
| UE    | 0.698 | 0.685 | 0.576 | 0.567 |
| ~UE   | 0.559 | 0.568 | 0.680 | 0.693 |
| UX    | 0.718 | 0.714 | 0.560 | 0.559 |
| ~UX   | 0.557 | 0.558 | 0.713 | 0.717 |
| BSAT  | **0.751** | 0.776 | 0.476 | 0.494 |
| ~BSAT | 0.511 | 0.493 | **0.784** | 0.759 |

> **Figure 11. fsQCA necessity XY plots** for the three conditions (no condition
> reaches the 0.90 necessity threshold). *File:*
> `analysis/figures/Fig11_fsqca_necessity.png`.

### 4.3 Analysis of sufficient configurations

A truth table was constructed over the 2³ = 8 corners of the vector space. Rows
were coded as sufficient using a **frequency threshold of 4** cases (all rows
exceeded this; total retained cases = 312), a **raw‑consistency threshold of 0.80**,
and a **PRI (proportional reduction in inconsistency) threshold of 0.70** to guard
against simultaneous subset relations with the outcome and its negation
(Greckhamer et al., 2018). The truth table is summarized in Table 12 and Figure 12.

**Table 12. Truth table (sorted by raw consistency).**

| UE | UX | BSAT | n cases | Raw consistency | PRI | Sufficient? |
|:--:|:--:|:----:|:-------:|:---------------:|:----:|:-----------:|
| 1 | 0 | 1 | 19 | 0.883 | 0.698 | No (PRI < 0.70) |
| 1 | 1 | 1 | 74 | 0.857 | 0.737 | **Yes** |
| 0 | 1 | 1 | 34 | 0.853 | 0.664 | No |
| 0 | 0 | 1 | 30 | 0.817 | 0.542 | No |
| 1 | 1 | 0 | 27 | 0.764 | 0.443 | No |
| 0 | 1 | 0 | 26 | 0.744 | 0.366 | No |
| 1 | 0 | 0 | 36 | 0.687 | 0.303 | No |
| 0 | 0 | 0 | 66 | 0.570 | 0.190 | No |

The Quine–McCluskey minimisation returns a **single sufficient configuration** for
high continuance, and the complex, parsimonious and intermediate solutions
**coincide** (Table 13). All three conditions appear in the recipe and—because they
are retained in both the parsimonious and the intermediate solution—each is a
**core** condition in the sense of Fiss (2011).

**Table 13. Sufficient configuration for high BSUC (Fiss notation).**

| Configuration | UE | UX | BSAT | Raw cov. | Unique cov. | Consistency |
|---------------|:--:|:--:|:----:|:--------:|:-----------:|:-----------:|
| C1 | ● (core) | ● (core) | ● (core) | 0.497 | 0.497 | 0.857 |
| **Solution** | | | | **0.497** | | **0.857** |

*(● = core condition present.)*

The solution is interpretable and parsimonious: **high brand‑system continuance
arises when user engagement, user experience *and* satisfaction are all
simultaneously high.** The configuration covers roughly half of the membership in
the outcome (raw/solution coverage = 0.497) at a consistency (0.857) above the
0.80 benchmark. Notably, the corner UE·~UX·BSAT had the highest *raw* consistency
(0.883) but was **correctly excluded** because its PRI (0.698) fell just below the
0.70 cut‑off—i.e., that corner is also substantially consistent with the *absence*
of the outcome and is therefore not a trustworthy sufficient recipe. This
illustrates the value of the PRI screen.

> **Figure 10. fsQCA sufficiency XY plot** for the core configuration
> UE·UX·BSAT (consistency = 0.857, coverage = 0.497). *File:*
> `analysis/figures/Fig10_fsqca_XY_sufficiency.png`.
> **Figure 12. Truth‑table configurations** ranked by sufficiency consistency
> (green = coded sufficient). *File:* `analysis/figures/Fig12_truth_table.png`.

To make the logic underlying the intermediate solution fully transparent, Table
13a reports the **subset/superset analysis** for the intermediate solution. Each
row is a candidate sufficient term formed by the set intersection (logical AND) of
the *presence* of the indicated conditions; less restrictive expressions (fewer
conditions) are supersets and more restrictive ones (more conditions) are subsets.
The analysis exhibits the canonical consistency–coverage trade‑off: as conditions
are added (moving toward subsets) consistency rises while coverage falls. The
full conjunction **UE • UX • BSAT** attains the **highest consistency (0.857)** and
satisfies both the 0.80 raw‑consistency and 0.70 PRI thresholds, which is why it is
retained as the sufficient configuration; satisfaction alone (BSAT) has the
**highest coverage (0.751)** but a PRI (0.661) below the threshold, confirming that
satisfaction is empirically important yet not, on its own, a trustworthy
sufficient recipe.

**Table 13a. Intermediate solution — subset/superset analysis (outcome = high Brand Success, BSUC).**

| Combination | # conditions | Raw consistency | PRI consistency | Raw coverage |
|-------------|:-----------:|:---------------:|:---------------:|:------------:|
| UE • UX • BSAT | 3 | **0.857** | **0.737** | 0.497 |
| UE • BSAT | 2 | 0.839 | 0.725 | 0.573 |
| UX • BSAT | 2 | 0.829 | 0.714 | 0.604 |
| BSAT | 1 | 0.776 | 0.661 | 0.751 |
| UE • UX | 2 | 0.774 | 0.620 | 0.566 |
| UX | 1 | 0.714 | 0.568 | 0.718 |
| UE | 1 | 0.685 | 0.530 | 0.698 |

Table 13b presents the same result in the **configuration format** conventionally
used to report fsQCA solutions for a focal outcome (Fiss, 2011; Ragin, 2008),
i.e. as a single column describing the recipe for **high Brand Success (BSUC) in
the metaverse**, the role of each condition (core vs. peripheral), and the
associated consistency and coverage metrics. Because the parsimonious and
intermediate solutions coincide, all three conditions are **core**.

**Table 13b. Configuration analysis for high Brand Success (BSUC) in the metaverse.**

| Condition / Metric | Configuration 1 |
|--------------------|:---------------:|
| User Engagement (UE) | ● (core) |
| User Experience (UX) | ● (core) |
| Brand Satisfaction (BSAT) | ● (core) |
| Raw coverage | 0.497 |
| Unique coverage | 0.497 |
| Configuration consistency | 0.857 |
| **Overall solution coverage** | **0.497** |
| **Overall solution consistency** | **0.857** |

*Notation: ● = core causal condition (present in both the parsimonious and the
intermediate solution); blank = condition absent or "don't care". Frequency
threshold = 4 cases; raw‑consistency threshold = 0.80; PRI threshold = 0.70.*

### 4.4 Causal asymmetry (analysis of the negated outcome)

A separate sufficiency analysis for **low** continuance (~BSUC) returns the
mirror‑absence configuration **~UE·~UX·~BSAT** (coverage = 0.492,
consistency = 0.861). The fact that the recipe for low continuance is the
joint *absence* of all three conditions—rather than a simple algebraic negation of
the high‑continuance recipe—demonstrates **causal asymmetry**: the conditions that
produce continuance and those that produce abandonment are not perfect opposites.
This asymmetric insight is unavailable from the symmetric PLS‑SEM and is one of
the principal contributions of the configurational analysis (Figure 13).

> **Figure 13. Configurations for high vs. low BSUC** (causal asymmetry; large
> circles = core conditions). *File:* `analysis/figures/Fig13_configurations.png`.

### 4.5 Robustness of the fsQCA

The configurational solution is stable under perturbations of the analytical
choices (Table 14; Skaggs & Bansal recommendations as operationalized by
Greckhamer et al., 2018). Varying the calibration anchors (P90/P50/P10), raising
the raw‑consistency threshold to 0.85, and raising the frequency threshold to 6
all reproduce the identical UE·UX·BSAT solution with essentially unchanged
coverage and consistency. Only the most extreme alternative—using fixed
substantive anchors (6 / 4 / 2 on the 7‑point scale)—simplifies the recipe to
UE·BSAT (dropping UX as a core element; coverage = 0.533, consistency = 0.805),
which is consistent with UX being the *weakest* necessity condition. Overall, the
solution is robust.

**Table 14. fsQCA robustness checks.**

| Scenario | # configs | Solution coverage | Solution consistency | Configuration(s) |
|----------|:---------:|:-----------------:|:--------------------:|------------------|
| Percentile 95/50/5 (main) | 1 | 0.497 | 0.857 | UE·UX·BSAT |
| Percentile 90/50/10 | 1 | 0.476 | 0.833 | UE·UX·BSAT |
| Raw consistency ≥ 0.85 | 1 | 0.497 | 0.857 | UE·UX·BSAT |
| Frequency ≥ 6 | 1 | 0.497 | 0.857 | UE·UX·BSAT |
| Substantive anchors 6/4/2 | 1 | 0.533 | 0.805 | UE·BSAT |

---

## 5. Synthesis: convergence and complementarity of PLS‑SEM and fsQCA

The two methods tell a coherent and mutually reinforcing story, while each adds
something the other cannot (Table 15).

* **Convergence.** Both analyses place **satisfaction (BSAT) at the centre** of
  brand‑system continuance. In PLS‑SEM, BSAT is the strongest path to BSUC and the
  full mediator of UE and UX; in fsQCA, BSAT has the highest single‑condition
  necessity consistency and is a core element of the sole sufficient recipe. Both
  analyses also agree that **experience (UX) matters more than engagement (UE)**
  on the path to that satisfaction.

* **Complementarity 1 — equifinality / conjunction.** PLS‑SEM finds that the
  *direct* effects of UE and UX on continuance are non‑significant; a purely
  variance‑based reading might therefore downplay them. fsQCA clarifies that UE
  and UX are nonetheless **jointly necessary as part of the sufficient
  configuration**: high continuance requires all three conditions *together*. The
  antecedents are thus complements, not substitutes—an insight about *combination*
  that the additive SEM cannot express.

* **Complementarity 2 — asymmetry.** PLS‑SEM is symmetric by construction. fsQCA
  shows that the recipe for low continuance (~UE·~UX·~BSAT) is not the simple
  inverse of the recipe for high continuance, revealing causal asymmetry of
  managerial relevance: preventing churn is not merely the absence of the drivers
  of retention.

**Table 15. Summary of findings across methods.**

| Question | PLS‑SEM answer | fsQCA answer |
|----------|----------------|--------------|
| What drives continuance on average? | BSAT (β=.476***); UE/UX only indirectly | BSAT highest necessity; core in the recipe |
| Are UE/UX effects direct? | No — fully mediated by BSAT | Required jointly, in conjunction with BSAT |
| Which combination yields high continuance? | (not addressable) | UE·UX·BSAT (cons.=.857, cov.=.497) |
| Is low continuance the mirror image? | (not addressable) | No — ~UE·~UX·~BSAT (asymmetry) |
| Predictive validity? | Q²>0; PLS<LM on 3/4 indicators | Solution stable across robustness checks |

In sum, satisfaction is the proximal engine of brand‑system continuance, user
experience is its dominant upstream antecedent, and the highest levels of
continuance are reached only when engagement, experience and satisfaction are
present **in combination**—while the route to abandonment follows its own,
asymmetric logic.

---

### Notes on reproducibility

All results are fully reproducible from the scripts in `analysis/`:
`01_screening.py` (screening, EFA, CMB), `02_measurement_model.py` (measurement
model + `plspm` cross‑validation), `03_structural_model.py` (paths, bootstrap,
*f²*, Q², SRMR, mediation, IPMA), `03b_plspredict.py` (out‑of‑sample prediction),
`04_fsqca.py` (calibration, necessity, sufficiency, robustness) and
`05_figures.py` (all figures). Numeric outputs are written to
`analysis/outputs/*.csv` and figures to `analysis/figures/*.png`. The custom
PLS‑SEM engine (`analysis/pls_engine.py`) was validated against the `plspm`
package (maximum loading discrepancy 0.003), and the fsQCA engine
(`analysis/fsqca_engine.py`) implements the standard Ragin (2008) consistency,
coverage and PRI formulas together with Quine–McCluskey minimisation.

### Selected references

- Fiss, P. C. (2011). Building better causal theories. *AMJ*, 54(2).
- Greckhamer, T., et al. (2018). Studying configurations with QCA. *Strategic Organization*, 16(4).
- Hair, J. F., et al. (2019). When to use and how to report the results of PLS‑SEM. *EBR*, 31(1).
- Hair, J. F., et al. (2022). *A Primer on PLS‑SEM* (3rd ed.). Sage.
- Henseler, J., Ringle, C. M., & Sarstedt, M. (2015). HTMT for discriminant validity. *JAMS*, 43(1).
- Kock, N. (2015). Common method bias in PLS‑SEM: A full collinearity assessment. *IJeC*, 11(4).
- Nitzl, C., Roldán, J. L., & Cepeda, G. (2016). Mediation analysis in PLS‑SEM. *IMDS*, 116(9).
- Pappas, I. O., & Woodside, A. G. (2021). Fuzzy‑set QCA in IS and marketing. *IJIM*, 58.
- Podsakoff, P. M., et al. (2003). Common method biases. *JAP*, 88(5).
- Ragin, C. C. (2008). *Redesigning Social Inquiry: Fuzzy Sets and Beyond*. Univ. of Chicago Press.
- Shmueli, G., et al. (2019). Predictive model assessment in PLS‑SEM: PLSpredict. *EJM*, 53(11).
- Woodside, A. G. (2013). Moving beyond multiple regression analysis to algorithms. *JBR*, 66(4).
- Zhao, X., Lynch, J. G., & Chen, Q. (2010). Reconsidering Baron and Kenny. *JCR*, 37(2).
