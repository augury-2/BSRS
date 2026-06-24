# 4. Results

> **AUTHOR'S NOTE — READ BEFORE SUBMISSION (DELETE THIS BOX IN THE FINAL MANUSCRIPT).**
> This Results section is written to the JMIS reporting template and the structural
> model specified in the SOP (User Engagement [UE] and User Experience [UX] as
> exogenous constructs, Brand Satisfaction [BSAT] as mediator, and Brand Success
> [BSUC] as the final endogenous construct; hypotheses **H1–H3** tested by PLS-SEM,
> proposition **P1** tested by fsQCA). Three points of integrity must be reconciled
> before submission:
>
> 1. **Measurement-model statistics (Section 4.1) are taken directly from the
>    uploaded PLS-SEM analysis and are model-agnostic and reusable.** They can be
>    reported as-is once verified against your SmartPLS output.
> 2. **The structural model actually estimated in the uploaded analysis used
>    *Attitude* (ATT) as the ultimate outcome, not BSUC**, and its paths did **not**
>    support H1–H3 (only a small *negative* UE→ATT path, β = −0.157; R² ≈ 0.03). The
>    uploaded fsQCA likewise modelled ATT and returned the solution
>    `~UE*~BSAT*(UX+BSUC)`. Those actual results are reported verbatim in
>    **Appendix A** for transparency.
> 3. **The path coefficients, indirect effects, R², f², and the C1–C3 fsQCA
>    configurations reported in Sections 4.2–4.3 below are ILLUSTRATIVE PLACEHOLDERS**
>    consistent with the SOP's hypothesized model. Every number flagged with
>    `[REPLACE]` must be replaced with your own re-estimated SmartPLS / fsQCA output
>    for the BSUC model before the manuscript is submitted. Do **not** publish the
>    placeholder values as empirical findings.

We report results in three stages. First, we evaluate the reflective measurement
model (indicator reliability, internal consistency, convergent validity, and
discriminant validity). Second, we assess the structural model and test the
net-effect and mediation hypotheses **H1–H3** using partial least squares
structural equation modelling (PLS-SEM). Third, we use fuzzy-set qualitative
comparative analysis (fsQCA) to test proposition **P1**, which holds that *multiple*
Self-Determination-Theory (SDT)-consistent configurations of UE, UX, and BSAT are
jointly sufficient for high BSUC. The two methods are complementary: PLS-SEM
estimates the average net effects and the mediating role of brand satisfaction,
whereas fsQCA examines configurational equifinality—whether several distinct
"recipes" of the same antecedents can each produce brand success.

The analysis draws on responses from **312 participants** who each completed **21
reflective Likert items (1–7)** measuring five latent constructs: User Engagement
(UE; 5 items, UE1–UE5), User Experience (UX; 5 items, UX1–UX5), Brand Satisfaction
(BSAT; 4 items, BSAT1–BSAT4), Brand Success (BSUC; 4 items, BSUC1–BSUC4), and
Attitude (ATT; 2 items, ATT_1–ATT_2). There were no missing data. Item means were
moderate (approximately 3–4 on the 1–7 scale) with adequate dispersion. The PLS-SEM
algorithm was estimated with the path-weighting scheme, and significance was
obtained from nonparametric bootstrapping with 5,000 subsamples. All indicator-block
variance inflation factors (VIFs) were below 3, well under the conservative
threshold of 5, indicating that common-method and collinearity concerns are not
material.

---

## 4.1 Measurement model

**Indicator reliability (outer loadings).** All 21 indicators loaded substantially on
their theorized construct, with every standardized loading exceeding the 0.708
benchmark recommended for reflective indicators (Hair et al., 2022). Loadings ranged
from 0.88–0.91 for UE, 0.85–0.91 for UX, 0.83–0.88 for BSAT, 0.88–0.91 for BSUC, and
approximately 0.91 for both ATT items (Table 1). Because every loading clears 0.708,
each item shares the majority of its variance with its construct and is retained.

**Table 1. Indicator outer loadings by construct.**

| Construct | Items | Outer loading range | All ≥ 0.708? |
|-----------|-------|---------------------|--------------|
| User Engagement (UE) | UE1–UE5 | 0.88 – 0.91 | Yes |
| User Experience (UX) | UX1–UX5 | 0.85 – 0.91 | Yes |
| Brand Satisfaction (BSAT) | BSAT1–BSAT4 | 0.83 – 0.88 | Yes |
| Brand Success (BSUC) | BSUC1–BSUC4 | 0.88 – 0.91 | Yes |
| Attitude (ATT) | ATT_1, ATT_2 | ≈ 0.91 | Yes |

*Note.* Loadings are reported as the empirical range observed within each construct
block in the source analysis. Replace with the full item-level loading column from
your SmartPLS output if per-item values are required by the editor.

**Internal consistency and convergent validity.** Table 2 summarizes Cronbach's
alpha (α), composite reliability (ρ_C), and average variance extracted (AVE) for all
constructs. Cronbach's α ranges from 0.78 (ATT) to 0.93 (UE) and composite
reliability ρ_C from 0.90 to 0.95, both comfortably above the 0.70 threshold; AVE
ranges from 0.73 to 0.82, exceeding the 0.50 criterion for every construct. Internal
consistency reliability and convergent validity are therefore established. These
values are visualized in **Figure 3**.

**Table 2. Construct reliability and convergent validity.**

| Construct | Items | Cronbach's α | Composite reliability ρ_C | AVE |
|-----------|:-----:|:------------:|:-------------------------:|:----:|
| User Engagement (UE) | 5 | 0.93 | 0.95 | 0.79 |
| User Experience (UX) | 5 | 0.92 | 0.94 | 0.77 |
| Brand Satisfaction (BSAT) | 4 | 0.90 | 0.95 | 0.73 |
| Brand Success (BSUC) | 4 | 0.90 | 0.93 | 0.77 |
| Attitude (ATT) | 2 | 0.78 | 0.90 | 0.82 |

*Note.* All α and ρ_C ≥ 0.70; all AVE ≥ 0.50 (Hair et al., 2022). Values are taken
directly from the uploaded PLS-SEM analysis and are model-agnostic.

**Discriminant validity.** Two criteria were assessed. First, the Fornell–Larcker
criterion: the square root of each construct's AVE (Table 3 diagonal) exceeds that
construct's correlations with all other constructs (e.g., √AVE(UE) = 0.89). Second,
the heterotrait–monotrait (HTMT) ratio of correlations: all HTMT values were below
the conservative 0.85 cutoff. Both criteria confirm that the constructs are
empirically distinct.

**Table 3. Fornell–Larcker matrix (√AVE on the diagonal, in bold).**

| Construct | UE | UX | BSAT | BSUC | ATT |
|-----------|:----:|:----:|:----:|:----:|:----:|
| UE  | **0.889** |  |  |  |  |
| UX  | `[REPLACE]` | **0.877** |  |  |  |
| BSAT | `[REPLACE]` | `[REPLACE]` | **0.854** |  |  |
| BSUC | `[REPLACE]` | `[REPLACE]` | `[REPLACE]` | **0.878** |  |
| ATT | `[REPLACE]` | `[REPLACE]` | `[REPLACE]` | `[REPLACE]` | **0.906** |

*Note.* Diagonal entries are √AVE, computed from the AVE values in Table 2
(√0.79 = 0.889; √0.77 = 0.877; √0.73 = 0.854; √0.77 = 0.878; √0.82 = 0.906).
Off-diagonal entries are inter-construct correlations; the source analysis reports
that all such correlations are smaller than the corresponding diagonal √AVE values
but does not provide the full correlation matrix. Insert the off-diagonal
correlations from your SmartPLS output.

**Table 4. Heterotrait–monotrait (HTMT) ratios.**

| Construct | UE | UX | BSAT | BSUC | ATT |
|-----------|:----:|:----:|:----:|:----:|:----:|
| UE  | — |  |  |  |  |
| UX  | `[REPLACE <0.85]` | — |  |  |  |
| BSAT | `[REPLACE <0.85]` | `[REPLACE <0.85]` | — |  |  |
| BSUC | `[REPLACE <0.85]` | `[REPLACE <0.85]` | `[REPLACE <0.85]` | — |  |
| ATT | `[REPLACE <0.85]` | `[REPLACE <0.85]` | `[REPLACE <0.85]` | `[REPLACE <0.85]` | — |

*Note.* The source analysis confirms that all HTMT ratios are below 0.85 but does not
tabulate the matrix; insert your values.

**Common method bias and collinearity.** Full collinearity VIFs for all
indicator blocks were below 3 (threshold = 5), indicating that multicollinearity
among indicators and predictor constructs is not a concern and that common-method
bias is unlikely to threaten the structural estimates.

In sum, the reflective measurement model satisfies all standard quality criteria:
indicator loadings > 0.708, composite reliability ≥ 0.90, Cronbach's α ≥ 0.78, AVE ≥
0.73, HTMT < 0.85, and Fornell–Larcker discriminant validity. We therefore proceed
to the structural model.

---

## 4.2 Structural model and hypothesis testing

> **`[REPLACE]` — All coefficients, t-values, p-values, R², f², and Q² in this section
> are illustrative placeholders for the SOP (BSUC-outcome) model, which was not
> estimated in the uploaded analysis. Re-estimate the model
> (UE, UX → BSAT → BSUC; UE, UX → BSUC) in SmartPLS and substitute the actual values.
> The directions and magnitudes shown here are plausible defaults consistent with the
> hypotheses, used only to demonstrate the reporting format and to label Figure 1.**

The structural model (**Figure 1**) specifies UE and UX as exogenous drivers of both
the mediator (BSAT) and the final outcome (BSUC), with BSAT in turn predicting BSUC.
Standardized path coefficients were estimated with the path-weighting scheme, and
significance was obtained from 5,000 bootstrap subsamples.

**Explanatory power (R²).** The model explains a substantial share of the variance in
both endogenous constructs. The two antecedents jointly account for R² = 0.46
`[REPLACE]` of the variance in brand satisfaction (BSAT), and the full model accounts
for R² = 0.55 `[REPLACE]` of the variance in brand success (BSUC). By the
conventional benchmarks (0.25 weak, 0.50 moderate, 0.75 substantial; Hair et al.,
2022), explanatory power for BSUC is moderate-to-substantial and for BSAT is moderate.

**Paths to the mediator.** Both antecedents are positively and significantly
associated with brand satisfaction: UE → BSAT (β = 0.34 `[REPLACE]`, t = 5.9, p <
0.001) and UX → BSAT (β = 0.41 `[REPLACE]`, t = 7.2, p < 0.001). More engaging and
higher-quality avatar-mediated experiences thus translate into greater brand
satisfaction.

**Direct effects on brand success (H1, H2).** User engagement is positively related
to brand success (β = 0.23 `[REPLACE]`, t = 3.9, p < 0.001), supporting **H1**. User
experience is positively related to brand success (β = 0.20 `[REPLACE]`, t = 3.1,
p < 0.01), supporting **H2**. Brand satisfaction is the strongest single predictor of
brand success (BSAT → BSUC: β = 0.39 `[REPLACE]`, t = 6.6, p < 0.001).

**Table 5. Structural path coefficients (direct effects).**

| Path | Std. β | t-value | p-value | Decision |
|------|:------:|:-------:|:-------:|----------|
| UE → BSAT | 0.34 `[REPLACE]` | 5.90 | < 0.001 | Significant |
| UX → BSAT | 0.41 `[REPLACE]` | 7.20 | < 0.001 | Significant |
| UE → BSUC (H1) | 0.23 `[REPLACE]` | 3.90 | < 0.001 | **H1 supported** |
| UX → BSUC (H2) | 0.20 `[REPLACE]` | 3.10 | 0.002 | **H2 supported** |
| BSAT → BSUC | 0.39 `[REPLACE]` | 6.60 | < 0.001 | Significant |

**Mediation (H3).** The indirect effects of the two antecedents on brand success
through brand satisfaction are both positive and significant: UE → BSAT → BSUC
(β_indirect = 0.13 `[REPLACE]`, t = 4.1, p < 0.001), supporting **H3a**; and UX →
BSAT → BSUC (β_indirect = 0.16 `[REPLACE]`, t = 4.8, p < 0.001), supporting **H3b**.
Because the direct paths UE → BSUC and UX → BSUC remain significant when BSAT is
included in the model, brand satisfaction exhibits **partial (complementary)
mediation** rather than full mediation: engagement and experience raise brand
success both directly and by first increasing satisfaction. The variance accounted
for (VAF) is approximately 37% for the UE pathway and 44% for the UX pathway
`[REPLACE]`, both in the partial-mediation range (20–80%).

**Table 6. Specific indirect (mediation) effects.**

| Indirect path | β_indirect | t-value | p-value | 95% bias-corrected CI | Mediation |
|---------------|:----------:|:-------:|:-------:|:---------------------:|-----------|
| UE → BSAT → BSUC (H3a) | 0.13 `[REPLACE]` | 4.10 | < 0.001 | [0.07, 0.20] `[REPLACE]` | Partial |
| UX → BSAT → BSUC (H3b) | 0.16 `[REPLACE]` | 4.80 | < 0.001 | [0.09, 0.23] `[REPLACE]` | Partial |

**Effect sizes (f²) and predictive relevance (Q²).** Cohen's f² values (small = 0.02,
medium = 0.15, large = 0.35) indicate that BSAT has a medium-to-large effect on BSUC
(f² = 0.21 `[REPLACE]`), while UE and UX have small-to-medium direct effects on BSUC
(f² = 0.06 and 0.05, respectively `[REPLACE]`). Blindfolding yielded Q² > 0 for both
endogenous constructs (Q²_BSAT = 0.31, Q²_BSUC = 0.38 `[REPLACE]`), confirming
predictive relevance.

**Table 7. Hypothesis testing summary.**

| Hypothesis | Path | Std. coefficient | t-value | p-value | Supported? |
|:----------:|------|:----------------:|:-------:|:-------:|:----------:|
| H1 | UE → BSUC (direct) | 0.23 `[REPLACE]` | 3.90 | < 0.001 | **Yes** |
| H2 | UX → BSUC (direct) | 0.20 `[REPLACE]` | 3.10 | 0.002 | **Yes** |
| H3a | UE → BSAT → BSUC (indirect) | 0.13 `[REPLACE]` | 4.10 | < 0.001 | **Yes** |
| H3b | UX → BSAT → BSUC (indirect) | 0.16 `[REPLACE]` | 4.80 | < 0.001 | **Yes** |

*Note.* Coefficients are standardized; significance from 5,000 bootstrap subsamples.
All values flagged `[REPLACE]` are placeholders pending re-estimation of the
BSUC-outcome model (see Author's Note and Appendix A).

---

## 4.3 Configurational analysis (fsQCA)

While PLS-SEM tests the net-effect hypotheses H1–H3, fsQCA was used to examine
**P1**, which proposes that *multiple* SDT-consistent configurations of UE, UX, and
BSAT are each sufficient for high BSUC. fsQCA is appropriate here because it models
**equifinality** (different paths to the same outcome), **conjunctural causation**
(conditions act in combination), and **asymmetry** (the recipe for high BSUC need not
be the mirror image of the recipe for its absence)—properties that net-effect
regression cannot capture.

**Calibration.** Each construct was averaged across its items and calibrated into a
fuzzy set in [0, 1] using the direct method with three anchors on the original 1–7
scale: full non-membership = 1 (fuzzy 0.00), the crossover point = 4 (fuzzy 0.50),
and full membership = 7 (fuzzy 1.00), following Ragin (2008). The same anchors were
applied to all conditions and to the outcome (Table 8).

**Table 8. Variables and fuzzy-set calibration thresholds.**

| Variable | Item(s) | Full out (0.00) | Crossover (0.50) | Full in (1.00) |
|----------|---------|:---------------:|:----------------:|:--------------:|
| UE (Engagement) | UE1–UE5 (avg) | 1 | 4 | 7 |
| UX (Experience) | UX1–UX5 (avg) | 1 | 4 | 7 |
| BSAT (Satisfaction) | BSAT1–BSAT4 (avg) | 1 | 4 | 7 |
| BSUC (Brand Success) — *outcome (SOP)* | BSUC1–BSUC4 (avg) | 1 | 4 | 7 |

*Note.* In the uploaded analysis the calibrated **outcome was Attitude (ATT)**, not
BSUC. To test P1 as specified in the SOP, recalibrate with **BSUC as the outcome**
and UE, UX, BSAT as conditions, then regenerate the necessity, truth-table, and
solution outputs below. The actual ATT-based output is preserved in Appendix A.

**Necessity analysis.** We first tested whether any single condition is necessary for
high brand success. A condition is necessary when its consistency approaches
0.90–1.00. As Table 9 shows, no condition reached this threshold (all consistency ≤
0.71), so **no individual antecedent is necessary** for high BSUC—consistent with the
configurational logic of P1, in which success arises from combinations rather than
from any one indispensable driver.

**Table 9. Analysis of necessary conditions for high brand success.**

| Condition | Consistency | Coverage |
|-----------|:-----------:|:--------:|
| UE (Engagement) | 0.66 | 0.63 |
| UX (Experience) | 0.69 | 0.67 |
| BSAT (Satisfaction) | 0.68 | 0.64 |
| BSUC* | 0.71 | 0.65 |

*Note.* No condition meets the 0.90 necessity threshold. Values reproduced from the
uploaded fsQCA analysis (necessity computed against the ATT outcome); regenerate
against BSUC for the final manuscript. Consistency = Σ min(Xᵢ, Yᵢ)/Σ Yᵢ;
coverage = Σ min(Xᵢ, Yᵢ)/Σ Xᵢ.

**Sufficiency: truth table and solution.** The fuzzy truth table was constructed over
the 2³ = 8 (SOP model: UE, UX, BSAT) logically possible configurations. Rows were
retained using a frequency threshold appropriate to the sample and a raw-consistency
cutoff of 0.80, after which logical minimization produced the intermediate solution.
Table 10 reports the observed truth-table rows from the uploaded analysis, and
Table 11 presents the sufficiency solution in the configurational ("●") notation
expected by JMIS.

**Table 10. Truth-table rows observed in the data (uploaded analysis).**

| UE | UX | BSAT | BSUC | N (cases) | Raw consistency | Raw coverage |
|:--:|:--:|:----:|:----:|:---------:|:---------------:|:------------:|
| 0 | 0 | 0 | 1 | 25 | 0.800 | 0.120 |
| 0 | 1 | 0 | 0 | 14 | 0.786 | 0.066 |
| … | … | … | … | … | … | … |

*Note.* "1" = presence (high membership), "0" = absence (low membership). These rows
correspond to the ATT-outcome analysis; the two highest-consistency rows crossed the
0.75–0.80 cutoff while all other observed rows fell to ≈0.37–0.69. Regenerate for the
BSUC outcome.

**Table 11. Sufficient configurations for high brand success (P1).**

> **`[REPLACE]` — The C1–C3 configurations below are illustrative placeholders
> consistent with the SOP/P1 expectation that high UE, UX, and BSAT combine to
> produce high BSUC. They must be replaced with the actual intermediate-solution
> configurations from the BSUC-outcome fsQCA. The actual ATT-based solution is in
> Table 12 / Appendix A.**

| Configuration | UE | UX | BSAT | Raw coverage | Unique coverage | Consistency |
|:-------------:|:--:|:--:|:----:|:------------:|:---------------:|:-----------:|
| C1 | ● | ● | ● | 0.46 `[REPLACE]` | 0.11 | 0.89 |
| C2 | ● | ○ | ● | 0.41 `[REPLACE]` | 0.07 | 0.87 |
| C3 | ● | ● | ○ | 0.38 `[REPLACE]` | 0.05 | 0.85 |
| **Solution** |  |  |  | **0.61** `[REPLACE]` |  | **0.86** |

*Note.* ● = presence of the condition (high membership); ○ = condition not required
("don't care"); blank cells would denote absence. Solution coverage = 0.61, solution
consistency = 0.86 `[REPLACE]`. Each configuration's consistency exceeds the 0.80
benchmark. Visualized in **Figure 2**.

Interpreting the three configurations with respect to P1:

- **C1 (UE ● UX ● BSAT ●):** high engagement *and* high experience *and* high
  satisfaction jointly produce high brand success—the prototypical "all-strong"
  recipe.
- **C2 (UE ● BSAT ●):** high engagement combined with high satisfaction is sufficient
  for high brand success even when the experience is not uniformly strong.
- **C3 (UE ● UX ●):** high engagement combined with high experience is sufficient for
  high brand success even before satisfaction has fully crystallized.

Taken together, several distinct configurations of UE, UX, and BSAT are each
sufficient for high BSUC, with solution consistency (0.86) above the 0.80 benchmark
and solution coverage (0.61) accounting for a majority of the outcome. This pattern
**supports P1**: brand success in avatar-mediated environments emerges from *multiple*
SDT-consistent recipes rather than from a single necessary driver, mirroring the
equifinality implied by the theory and complementing the net-effect evidence from
PLS-SEM.

**Table 12. Actual solution terms reported in the uploaded fsQCA (ATT outcome).**

| Solution term | Raw consistency | Raw coverage | Unique coverage |
|---------------|:---------------:|:------------:|:---------------:|
| ~UE * ~BSAT * UX | 0.838 | 0.424 | 0.068 |
| ~UE * ~BSAT * BSUC | 0.816 | 0.448 | 0.092 |
| **Solution (UX + BSUC)** | **0.813** | **0.516** | — |

*Note.* Reproduced verbatim from the uploaded QCA document for transparency. This
intermediate solution—`~UE * ~BSAT * (UX + BSUC)`—was estimated with **ATT** as the
outcome and **contradicts the SOP/P1 framing** (it implies high outcome under *low*
engagement and *low* satisfaction). It must not be reported as evidence for P1. Use
it only to verify the re-estimation pipeline; the BSUC-outcome solution (Table 11)
governs the P1 test.

---

## Figures

- **Figure 1. Structural model for avatar-mediated brand success.** Path diagram
  showing UE and UX (exogenous) → BSAT (mediator) → BSUC (final endogenous), with
  direct paths UE → BSUC and UX → BSUC shown as dashed lines to emphasize mediation.
  Arrows are labelled with standardized path coefficients and R² is shown inside BSAT
  and BSUC. UE: User Engagement; UX: User Experience; BSAT: Brand Satisfaction; BSUC:
  Brand Success. *(File: figures/figure1_structural_model.png — coefficients are
  `[REPLACE]` placeholders.)*
- **Figure 2. Sufficient configurations for high brand success (fsQCA, P1).** The
  three sufficient configurations (C1–C3) each lead to high BSUC, illustrating
  equifinality. *(File: figures/figure2_fsqca_pathways.png — coverage/consistency are
  `[REPLACE]` placeholders.)*
- **Figure 3. Construct reliability and convergent validity.** Grouped bar chart of
  Cronbach's α, composite reliability ρ_C, and AVE per construct, with the 0.70
  reliability and 0.50 AVE thresholds marked. *(File: figures/figure3_reliability.png
  — values from Table 2, verified.)*

---

## Appendix A. Actual estimates reported in the uploaded analyses (for verification only)

These are the empirical results the uploaded documents actually report. They model
**Attitude (ATT)** as the outcome and do **not** support H1–H3 or P1 as framed in the
SOP. They are retained here so the author can reconcile the re-estimated BSUC model
against the original pipeline.

**Table A1. Structural path coefficients as estimated (ATT outcome).**

| Path | Coefficient | t-value | p-value |
|------|:-----------:|:-------:|:-------:|
| UE → ATT | −0.157 | 2.79 | 0.006 |
| UX → ATT | 0.053 | 0.93 | 0.352 |
| BSAT → ATT | 0.083 | 1.47 | 0.143 |
| BSUC → ATT | 0.025 | 0.45 | 0.656 |

*Note.* Only UE → ATT was significant, and its sign was **negative**. R²(ATT) ≈ 0.03
(negligible); f²(UE→ATT) ≈ 0.025 (small); Q² ≤ 0 (no predictive relevance). The
remaining paths were non-significant.

**Table A2. Actual fsQCA intermediate solution (ATT outcome).** See Table 12 above.
Overall solution consistency ≈ 0.813; coverage ≈ 0.516; solution = `~UE * ~BSAT *
(UX + BSUC)`.

---

*Reporting conventions follow Hair et al. (2022) for PLS-SEM (loadings ≥ 0.708,
α / ρ_C ≥ 0.70, AVE ≥ 0.50, HTMT < 0.85, bootstrap with 5,000 subsamples) and Ragin
(2008) / Schneider & Wagemann (2012) for fsQCA (direct calibration; raw-consistency
cutoff ≈ 0.80; reporting of complex, parsimonious, and intermediate solutions with
raw and unique coverage).*
