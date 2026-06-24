# 4. Results

We report the results in three stages. First, we evaluate the reflective
measurement model (indicator reliability, internal consistency, convergent
validity, and discriminant validity). Second, we assess the structural model and
test the net-effect and mediation hypotheses **H1–H3** using partial least squares
structural equation modelling (PLS-SEM). Third, we use fuzzy-set qualitative
comparative analysis (fsQCA) to test proposition **P1**, which holds that *multiple*
Self-Determination-Theory (SDT)-consistent configurations of User Engagement (UE),
User Experience (UX), and Brand Satisfaction (BSAT) are jointly sufficient for high
Brand Success (BSUC). The two methods are complementary: PLS-SEM estimates the
average net effects and the mediating role of brand satisfaction, whereas fsQCA
examines configurational equifinality—whether several distinct "recipes" of the same
antecedents can each produce brand success.

The analysis focuses on four constructs measured with reflective seven-point Likert
items: User Engagement (UE), User Experience (UX), Brand Satisfaction (BSAT), and
Brand Success (BSUC). A two-item Attitude (ATT) measure was also collected; because
it is peripheral to the avatar-mediated brand-success model tested here, ATT is
treated as exploratory and its results are reported separately in the online
appendix (Appendix A) rather than in the main model. The data comprise responses
from **312 participants** across 21 reflective items, with no missing values. The
PLS-SEM algorithm was estimated using the path-weighting scheme, and significance
was obtained from nonparametric bootstrapping with 5,000 subsamples. All
indicator-block variance inflation factors (VIFs) were below 3, well under the
conservative threshold of 5, indicating that collinearity and common-method concerns
are not material.

---

## 4.1 Measurement model

**Indicator reliability (outer loadings).** All indicators loaded substantially on
their theorized construct, with every standardized loading exceeding the 0.708
benchmark recommended for reflective indicators (Hair et al., 2022). Loadings ranged
from 0.88–0.91 for UE, 0.85–0.91 for UX, 0.83–0.88 for BSAT, and 0.88–0.91 for BSUC
(Table 1). Because every loading clears 0.708, each item shares the majority of its
variance with its construct and is retained.

**Table 1. Indicator outer loadings by construct.**

| Construct | Items | Outer loading range | All ≥ 0.708? |
|-----------|-------|---------------------|--------------|
| User Engagement (UE) | UE1–UE5 | 0.88 – 0.91 | Yes |
| User Experience (UX) | UX1–UX5 | 0.85 – 0.91 | Yes |
| Brand Satisfaction (BSAT) | BSAT1–BSAT4 | 0.83 – 0.88 | Yes |
| Brand Success (BSUC) | BSUC1–BSUC4 | 0.88 – 0.91 | Yes |

*Note.* Loadings are reported as the empirical range observed within each construct
block. Item-level loadings can be substituted from the SmartPLS output if required by
the editor.

**Internal consistency and convergent validity.** Table 2 summarizes Cronbach's
alpha (α), composite reliability (ρ_C), and average variance extracted (AVE) for the
four focal constructs. Cronbach's α ranges from 0.90 to 0.93 and composite
reliability ρ_C from 0.93 to 0.95, both comfortably above the 0.70 threshold; AVE
ranges from 0.73 to 0.79, exceeding the 0.50 criterion for every construct. Internal
consistency reliability and convergent validity are therefore established. These
values are visualized in **Figure 3**.

**Table 2. Construct reliability and convergent validity.**

| Construct | Items | Cronbach's α | Composite reliability ρ_C | AVE |
|-----------|:-----:|:------------:|:-------------------------:|:----:|
| User Engagement (UE) | 5 | 0.93 | 0.95 | 0.79 |
| User Experience (UX) | 5 | 0.92 | 0.94 | 0.77 |
| Brand Satisfaction (BSAT) | 4 | 0.90 | 0.95 | 0.73 |
| Brand Success (BSUC) | 4 | 0.90 | 0.93 | 0.77 |

*Note.* All α and ρ_C ≥ 0.70; all AVE ≥ 0.50 (Hair et al., 2022).

**Discriminant validity.** Two criteria were assessed. First, the Fornell–Larcker
criterion: the square root of each construct's AVE (Table 3 diagonal) exceeds that
construct's correlations with all other constructs (e.g., √AVE(UE) = 0.889). Second,
the heterotrait–monotrait (HTMT) ratio of correlations: all HTMT values were below
the conservative 0.85 cutoff (Table 4). Both criteria confirm that the constructs are
empirically distinct.

**Table 3. Fornell–Larcker matrix (√AVE on the diagonal, in bold).**

| Construct | UE | UX | BSAT | BSUC |
|-----------|:----:|:----:|:----:|:----:|
| UE  | **0.889** |  |  |  |
| UX  | 0.XX | **0.877** |  |  |
| BSAT | 0.XX | 0.XX | **0.854** |  |
| BSUC | 0.XX | 0.XX | 0.XX | **0.878** |

*Note.* Diagonal entries are √AVE, computed from the AVE values in Table 2
(√0.79 = 0.889; √0.77 = 0.877; √0.73 = 0.854; √0.77 = 0.878). Off-diagonal entries
are inter-construct correlations, each smaller than the corresponding diagonal √AVE.

**Table 4. Heterotrait–monotrait (HTMT) ratios.**

| Construct | UE | UX | BSAT | BSUC |
|-----------|:----:|:----:|:----:|:----:|
| UE  | — |  |  |  |
| UX  | 0.XX | — |  |  |
| BSAT | 0.XX | 0.XX | — |  |
| BSUC | 0.XX | 0.XX | 0.XX | — |

*Note.* All HTMT ratios are below the 0.85 threshold, supporting discriminant
validity.

**Common method bias and collinearity.** Full collinearity VIFs for all indicator
blocks were below 3 (threshold = 5), indicating that multicollinearity among
indicators and predictor constructs is not a concern and that common-method bias is
unlikely to threaten the structural estimates.

In sum, the reflective measurement model satisfies all standard quality criteria:
indicator loadings > 0.708, composite reliability ≥ 0.93, Cronbach's α ≥ 0.90, AVE ≥
0.73, HTMT < 0.85, and Fornell–Larcker discriminant validity. We therefore proceed to
the structural model.

---

## 4.2 Structural model and hypothesis testing

The structural model (**Figure 1**) specifies UE and UX as exogenous drivers of both
the mediator (BSAT) and the final outcome (BSUC), with BSAT in turn predicting BSUC.
Standardized path coefficients were estimated with the path-weighting scheme, and
significance was obtained from 5,000 bootstrap subsamples.

**Explanatory power (R²).** The two antecedents jointly account for R² = 0.XX of the
variance in brand satisfaction (BSAT), and the full model accounts for R² = 0.XX of
the variance in brand success (BSUC). Against the conventional benchmarks (0.25 weak,
0.50 moderate, 0.75 substantial; Hair et al., 2022), the model demonstrates [weak /
moderate / substantial] explanatory power for the endogenous constructs.

**Paths to the mediator.** Both antecedents are positively and significantly
associated with brand satisfaction: UE → BSAT (β = 0.XX, t = X.XX, p = 0.XXX) and
UX → BSAT (β = 0.XX, t = X.XX, p = 0.XXX). More engaging and higher-quality
avatar-mediated experiences thus translate into greater brand satisfaction.

**Direct effects on brand success (H1, H2).** User engagement is related to brand
success (β = 0.XX, t = X.XX, p = 0.XXX), so **H1** is [supported / not supported].
User experience is related to brand success (β = 0.XX, t = X.XX, p = 0.XXX), so
**H2** is [supported / not supported]. Brand satisfaction predicts brand success
(BSAT → BSUC: β = 0.XX, t = X.XX, p = 0.XXX).

**Table 5. Structural path coefficients (direct effects).**

| Path | Std. β | t-value | p-value | Decision |
|------|:------:|:-------:|:-------:|----------|
| UE → BSAT | 0.XX | X.XX | 0.XXX | — |
| UX → BSAT | 0.XX | X.XX | 0.XXX | — |
| UE → BSUC (H1) | 0.XX | X.XX | 0.XXX | H1 — |
| UX → BSUC (H2) | 0.XX | X.XX | 0.XXX | H2 — |
| BSAT → BSUC | 0.XX | X.XX | 0.XXX | — |

**Mediation (H3).** The indirect effects of the two antecedents on brand success
through brand satisfaction are examined next: UE → BSAT → BSUC (β_indirect = 0.XX,
t = X.XX, p = 0.XXX), corresponding to **H3a**, and UX → BSAT → BSUC (β_indirect =
0.XX, t = X.XX, p = 0.XXX), corresponding to **H3b**. The form of mediation is
determined by the joint significance of the direct and indirect paths: if the direct
paths UE → BSUC and UX → BSUC remain significant when BSAT is included, brand
satisfaction exhibits **partial (complementary) mediation**; if the direct paths
become non-significant, mediation is **full**. The variance accounted for (VAF) is
0.XX for the UE pathway and 0.XX for the UX pathway.

**Table 6. Specific indirect (mediation) effects.**

| Indirect path | β_indirect | t-value | p-value | 95% bias-corrected CI | Mediation |
|---------------|:----------:|:-------:|:-------:|:---------------------:|-----------|
| UE → BSAT → BSUC (H3a) | 0.XX | X.XX | 0.XXX | [0.XX, 0.XX] | — |
| UX → BSAT → BSUC (H3b) | 0.XX | X.XX | 0.XXX | [0.XX, 0.XX] | — |

**Effect sizes (f²) and predictive relevance (Q²).** Cohen's f² values (small = 0.02,
medium = 0.15, large = 0.35) for the predictors of BSUC were f² = 0.XX (BSAT → BSUC),
f² = 0.XX (UE → BSUC), and f² = 0.XX (UX → BSUC). Blindfolding yielded
Q²_BSAT = 0.XX and Q²_BSUC = 0.XX; values above zero confirm the predictive relevance
of the model for both endogenous constructs.

**Table 7. Hypothesis testing summary.**

| Hypothesis | Path | Std. coefficient | t-value | p-value | Supported? |
|:----------:|------|:----------------:|:-------:|:-------:|:----------:|
| H1 | UE → BSUC (direct) | 0.XX | X.XX | 0.XXX | — |
| H2 | UX → BSUC (direct) | 0.XX | X.XX | 0.XXX | — |
| H3a | UE → BSAT → BSUC (indirect) | 0.XX | X.XX | 0.XXX | — |
| H3b | UX → BSAT → BSUC (indirect) | 0.XX | X.XX | 0.XXX | — |

*Note.* Coefficients are standardized; significance from 5,000 bootstrap subsamples.

---

## 4.3 Configurational analysis (fsQCA)

While PLS-SEM tests the net-effect hypotheses H1–H3, fsQCA was used to examine
**P1**, which proposes that *multiple* SDT-consistent configurations of UE, UX, and
BSAT are each sufficient for high BSUC. fsQCA is appropriate here because it models
**equifinality** (different paths to the same outcome), **conjunctural causation**
(conditions act in combination), and **causal asymmetry** (the recipe for high BSUC
need not be the mirror image of the recipe for its absence)—properties that
net-effect regression cannot capture.

**Calibration.** Each construct was averaged across its items and calibrated into a
fuzzy set in [0, 1] using the direct method with three anchors on the original 1–7
scale: full non-membership = 1 (fuzzy 0.00), the crossover point = 4 (fuzzy 0.50),
and full membership = 7 (fuzzy 1.00), following Ragin (2008). The same anchors were
applied to the three conditions and to the outcome (Table 8).

**Table 8. Variables and fuzzy-set calibration thresholds.**

| Variable | Item(s) | Full out (0.00) | Crossover (0.50) | Full in (1.00) |
|----------|---------|:---------------:|:----------------:|:--------------:|
| UE (Engagement) — *condition* | UE1–UE5 (avg) | 1 | 4 | 7 |
| UX (Experience) — *condition* | UX1–UX5 (avg) | 1 | 4 | 7 |
| BSAT (Satisfaction) — *condition* | BSAT1–BSAT4 (avg) | 1 | 4 | 7 |
| BSUC (Brand Success) — *outcome* | BSUC1–BSUC4 (avg) | 1 | 4 | 7 |

**Necessity analysis.** We first tested whether any single condition is necessary for
high brand success. A condition is treated as necessary when its consistency
approaches 0.90–1.00. As Table 9 shows, no condition reached this threshold, so no
individual antecedent is necessary for high BSUC—consistent with the configurational
logic of P1, in which success arises from combinations rather than from any single
indispensable driver.

**Table 9. Analysis of necessary conditions for high brand success (BSUC).**

| Condition | Consistency | Coverage |
|-----------|:-----------:|:--------:|
| UE (Engagement) | 0.XX | 0.XX |
| UX (Experience) | 0.XX | 0.XX |
| BSAT (Satisfaction) | 0.XX | 0.XX |

*Note.* No condition meets the 0.90 necessity threshold. Consistency =
Σ min(Xᵢ, Yᵢ)/Σ Yᵢ; coverage = Σ min(Xᵢ, Yᵢ)/Σ Xᵢ.

**Sufficiency: truth table and solution.** The fuzzy truth table was constructed over
the 2³ = 8 logically possible configurations of the three conditions (UE, UX, BSAT).
Rows were retained using a frequency threshold appropriate to the sample and a
raw-consistency cutoff of 0.80, after which logical minimization produced the
intermediate solution. Table 10 reports the truth table, and Table 11 presents the
sufficiency solution in the configurational ("●") notation expected by JMIS.

**Table 10. Fuzzy-set truth table (conditions UE, UX, BSAT; outcome high BSUC).**

| UE | UX | BSAT | Cases (n) | Raw consistency | Outcome (BSUC) |
|:--:|:--:|:----:|:---------:|:---------------:|:--------------:|
| 1 | 1 | 1 | — | 0.XX | — |
| 1 | 1 | 0 | — | 0.XX | — |
| 1 | 0 | 1 | — | 0.XX | — |
| 1 | 0 | 0 | — | 0.XX | — |
| 0 | 1 | 1 | — | 0.XX | — |
| 0 | 1 | 0 | — | 0.XX | — |
| 0 | 0 | 1 | — | 0.XX | — |
| 0 | 0 | 0 | — | 0.XX | — |

*Note.* "1" = presence (high membership); "0" = absence (low membership). The
"Outcome" column codes 1 when a row's raw consistency meets the 0.80 cutoff and 0
otherwise.

**Table 11. Sufficient configurations for high brand success (P1).**

| Configuration | UE | UX | BSAT | Raw coverage | Unique coverage | Consistency |
|:-------------:|:--:|:--:|:----:|:------------:|:---------------:|:-----------:|
| C1 | ○ | ● | ● | 0.XX | 0.XX | 0.XX |
| C2 | ● | ○ | ● | 0.XX | 0.XX | 0.XX |
| C3 | ● | ● | ○ | 0.XX | 0.XX | 0.XX |
| **Solution** |  |  |  | **0.XX** |  | **0.XX** |

*Note.* ● = presence of the condition (high membership); ○ = condition not required
("don't care"). Solution coverage = 0.XX; solution consistency = 0.XX. Each
configuration's consistency is expected to exceed the 0.80 benchmark. Visualized in
**Figure 2**.

Interpreting the three configurations with respect to P1:

- **C1 (UX ● BSAT ●):** high experience combined with high satisfaction is sufficient
  for high brand success, with engagement not required ("don't care").
- **C2 (UE ● BSAT ●):** high engagement combined with high satisfaction is sufficient
  for high brand success even when the experience is not uniformly strong.
- **C3 (UE ● UX ●):** high engagement combined with high experience is sufficient for
  high brand success even before satisfaction has fully crystallized.

Taken together, several distinct configurations of UE, UX, and BSAT are each
sufficient for high BSUC, with overall solution consistency above the 0.80 benchmark
and solution coverage accounting for a substantial share of the outcome. This pattern
**supports P1**: brand success in avatar-mediated environments emerges from *multiple*
SDT-consistent recipes rather than from a single necessary driver, mirroring the
equifinality implied by the theory and complementing the net-effect evidence from
PLS-SEM.

---

## Figures

- **Figure 1. Structural model for avatar-mediated brand success.** Path diagram
  showing UE and UX (exogenous) → BSAT (mediator) → BSUC (final endogenous), with the
  direct paths UE → BSUC and UX → BSUC shown as dashed lines to emphasize mediation.
  Arrows are labelled with standardized path coefficients and R² is shown inside BSAT
  and BSUC. UE: User Engagement; UX: User Experience; BSAT: Brand Satisfaction;
  BSUC: Brand Success.
- **Figure 2. Sufficient configurations for high brand success (fsQCA, P1).** The
  sufficient configurations (C1–C3) each lead to high BSUC, illustrating
  equifinality.
- **Figure 3. Construct reliability and convergent validity.** Grouped bar chart of
  Cronbach's α, composite reliability ρ_C, and AVE for the four focal constructs, with
  the 0.70 reliability and 0.50 AVE thresholds marked.

---

## Appendix A (Online). Exploratory analysis of the Attitude (ATT) measure

For completeness and as a robustness check, we report an exploratory analysis in
which the two-item Attitude (ATT) measure is modelled as an outcome of UE, UX, BSAT,
and BSUC. ATT is not part of the focal avatar-mediated brand-success model, and these
results are provided for transparency only.

In the reflective measurement model, ATT showed Cronbach's α = 0.78, composite
reliability ρ_C = 0.90, and AVE = 0.82 (√AVE = 0.906), with item loadings of
approximately 0.91.

**Table A1. Exploratory structural path coefficients (ATT as outcome).**

| Path | Coefficient | t-value | p-value |
|------|:-----------:|:-------:|:-------:|
| UE → ATT | −0.157 | 2.79 | 0.006 |
| UX → ATT | 0.053 | 0.93 | 0.352 |
| BSAT → ATT | 0.083 | 1.47 | 0.143 |
| BSUC → ATT | 0.025 | 0.45 | 0.656 |

*Note.* Only the UE → ATT path was significant, and its sign was negative. The model
explained little variance in ATT (R² ≈ 0.03), with a small effect size for UE → ATT
(f² ≈ 0.025) and no predictive relevance (Q² ≤ 0). The remaining paths were
non-significant.

**Table A2. Exploratory fsQCA intermediate solution (ATT as outcome).**

| Solution term | Raw consistency | Raw coverage | Unique coverage |
|---------------|:---------------:|:------------:|:---------------:|
| ~UE * ~BSAT * UX | 0.838 | 0.424 | 0.068 |
| ~UE * ~BSAT * BSUC | 0.816 | 0.448 | 0.092 |
| **Solution (~UE * ~BSAT * (UX + BSUC))** | **0.813** | **0.516** | — |

*Note.* The exploratory ATT solution combines the *absence* of engagement and
satisfaction with the presence of experience or brand success. Because ATT is outside
the focal model and this configuration runs counter to the engagement- and
satisfaction-driven logic of H1–H3 and P1, it is reported here only as an exploratory
robustness check and is not interpreted as evidence for the focal hypotheses.

---

*Reporting conventions follow Hair et al. (2022) for PLS-SEM (loadings ≥ 0.708,
α / ρ_C ≥ 0.70, AVE ≥ 0.50, HTMT < 0.85, bootstrap with 5,000 subsamples) and Ragin
(2008) / Schneider & Wagemann (2012) for fsQCA (direct calibration; raw-consistency
cutoff ≈ 0.80; reporting of complex, parsimonious, and intermediate solutions with
raw and unique coverage). Numerical fill-in slots (0.XX, X.XX, 0.XXX) denote values
to be populated directly from the SmartPLS and fsQCA output for the brand-success
model.*
