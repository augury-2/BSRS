# Results

This section reports the empirical evaluation of the Self-Determination-Theory (SDT) based model of avatar-mediated brand outcomes. We first describe the sample and basic descriptive statistics, then assess the reflective measurement model, test the structural hypotheses (H1a–H4) using partial least squares structural equation modeling (PLS-SEM) with bootstrapping, and finally examine the configurational proposition (P1) using fuzzy-set qualitative comparative analysis (fsQCA). Tables and the figure are referenced in their order of appearance.

> **Transparency note (read first).** As required by a confirmatory-yet-honest analytic protocol, the hypotheses below were stated *a priori* from SDT and were revised only where the data forced a change. The measurement model is exemplary, but the data do **not** support any of the hypothesized structural or configurational relationships: the four latent constructs are essentially **statistically orthogonal** in this sample. We report this outcome fully and transparently, justify every threshold, and discuss the implications for the model and for the dataset itself. We did not alter, trim, or re-weight cases to manufacture effects.

---

## 1. Sample characteristics and descriptive statistics

The analysis is based on **N = 312** complete responses collected with reflective, 7-point Likert-type items (1 = *strongly disagree* to 7 = *strongly agree*). The dataset contained **no missing values** across the 18 focal indicators and the two attitudinal control items (ATT_1, ATT_2), so no imputation was required. Univariate screening showed all items spanning the full 1–7 range with means clustered near the scale midpoint (item *M* range = 3.85–4.15) and substantial dispersion (item *SD* range = 1.83–2.01). Item-level skewness (|skew| ≤ 0.14) and kurtosis (range −1.22 to −1.02) were within commonly accepted limits for symmetric, slightly platykurtic distributions; the mild negative kurtosis is typical of broadly used 7-point scales. A multivariate outlier screen using Mahalanobis distance over the 18 indicators flagged **no** cases at the conservative p < .001 criterion (max *D²* = 39.54 < χ²(18) = 42.31). Because PLS-SEM makes no multivariate-normality assumption and bootstrapping is used for inference, the modest non-normality is inconsequential.

Construct composites were formed as item means: UE = mean(UE1–UE5), UX = mean(UX1–UX5), BSAT = mean(BSAT1–BSAT4), BSUC = mean(BSUC1–BSUC4). Composite descriptive statistics and their zero-order correlations (including the attitudinal controls) are reported in **Table 1**.

**Table 1. Means, standard deviations, and correlations among composites (N = 312).**

| Variable | M | SD | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|---|
| 1. UE | 3.99 | 1.71 | 1.00 | | | | | |
| 2. UX | 3.96 | 1.65 | .01 | 1.00 | | | | |
| 3. BSAT | 4.05 | 1.69 | −.04 | .08 | 1.00 | | | |
| 4. BSUC | 4.13 | 1.63 | .04 | −.05 | .01 | 1.00 | | |
| 5. ATT_1 | 3.85 | 1.84 | −.12 | .02 | −.04 | −.06 | 1.00 | |
| 6. ATT_2 | 3.92 | 1.87 | −.16 | .07 | −.09 | −.01 | .64 | 1.00 |

*Note.* No correlation among the four focal constructs reaches |r| = .09; none is statistically significant at α = .05 (the critical value for n = 312 is |r| ≈ .111). The only sizeable association is between the two attitudinal control items (r = .64), which correlate with one another but not meaningfully with the focal constructs.

The descriptive picture already foreshadows the central finding: although each construct is well-measured (Section 2), the constructs are **uncorrelated with one another**.

---

## 2. Measurement model (PLS-SEM)

The model was estimated with PLS-SEM (Mode A, reflective measurement; path-weighting inner scheme), which is appropriate for a predictive, composite-based evaluation of an SDT nomological network. All four constructs (UE, UX, BSAT, BSUC) were specified as reflective, consistent with the conceptualization of UE and UX as interaction-level manifestations of SDT need satisfaction, BSAT as the evaluative outcome, and BSUC as the brand-level outcome.

### 2.1 Indicator reliability and internal consistency

All standardized outer loadings substantially exceed the .70 benchmark (range = **.831–.946**), so every indicator was retained; no item fell into the .40–.70 "consider-removal" band or below. Internal consistency is excellent and uniform across constructs: Cronbach's α = .902–.934 and composite reliability (CR/ρc) = .929–.942, all comfortably above the .70 threshold and below the .95 ceiling that would signal redundancy. **Table 2** reports indicator properties together with α, CR, and average variance extracted (AVE).

**Table 2. Measurement model: loadings, reliability, and AVE.**

| Construct | Item | Loading | Cronbach's α | CR (ρc) | AVE |
|---|---|---|---|---|---|
| **User Engagement (UE)** | UE1 | .832 | **.934** | **.942** | **.764** |
| | UE2 | .862 | | | |
| | UE3 | .946 | | | |
| | UE4 | .881 | | | |
| | UE5 | .845 | | | |
| **User Experience (UX)** | UX1 | .860 | **.925** | **.943** | **.766** |
| | UX2 | .900 | | | |
| | UX3 | .889 | | | |
| | UX4 | .854 | | | |
| | UX5 | .874 | | | |
| **Brand Satisfaction (BSAT)** | BSAT1 | .901 | **.913** | **.936** | **.786** |
| | BSAT2 | .877 | | | |
| | BSAT3 | .857 | | | |
| | BSAT4 | .910 | | | |
| **Brand Success (BSUC)** | BSUC1 | .904 | **.902** | **.929** | **.767** |
| | BSUC2 | .895 | | | |
| | BSUC3 | .871 | | | |
| | BSUC4 | .831 | | | |

*Note.* All loadings significant at p < .001 (bootstrap, 5,000 subsamples).

### 2.2 Convergent reliability (AVE)

AVE ranges from **.764 to .786**, exceeding the .50 criterion for every construct. Consistent with current measurement guidance, we interpret AVE as a **reliability** index — the proportion of indicator variance captured by the construct relative to measurement error (here ≈ 76–79%) — rather than as a stand-alone test of validity.

### 2.3 Discriminant validity

Discriminant validity was assessed with the heterotrait–monotrait ratio of correlations (HTMT), reported in **Table 3**. All HTMT values are extraordinarily low (range = **.032–.094**), far below both the conservative .85 and liberal .90 thresholds. The Fornell–Larcker criterion is likewise satisfied: each construct's √AVE (≈ .87–.89) vastly exceeds its correlations with the other constructs (|r| ≤ .10). Discriminant validity is therefore not merely adequate but extreme — a direct consequence of the constructs being empirically independent.

**Table 3. Heterotrait–monotrait ratios (HTMT).**

| | UE | UX | BSAT | BSUC |
|---|---|---|---|---|
| UE | — | | | |
| UX | .041 | — | | |
| BSAT | .050 | .094 | — | |
| BSUC | .042 | .073 | .032 | — |

*Note.* All HTMT < .85 (and < .90). The near-zero values indicate the constructs share virtually no common variance.

### 2.4 Common method bias

Common method bias (CMB) was evaluated with Kock's full-collinearity approach: each construct was regressed on all others and the variance inflation factor (VIF) inspected. All full-collinearity VIFs are **≈ 1.00** (UE = 1.006, UX = 1.014, BSAT = 1.014, BSUC = 1.008), far below the 3.3 threshold (**Table 4**). There is thus no evidence of common method bias or of pathological collinearity. (Trivially, the near-unity VIFs also reflect the absence of inter-construct correlation.)

**Table 4. Full-collinearity VIFs (CMB check).**

| Construct | VIF |
|---|---|
| UE | 1.006 |
| UX | 1.014 |
| BSAT | 1.014 |
| BSUC | 1.008 |

**Measurement-model summary.** The reflective measurement model is, by every standard criterion, exemplary: high and significant loadings, α and CR well above .70, AVE near .77, HTMT below .10, and no CMB. The instrument is reliable and the constructs are sharply distinct. This clean measurement foundation makes the structural results that follow interpretable and credible rather than an artifact of poor measurement.

---

## 3. Structural model and hypothesis tests (PLS-SEM)

The structural model specified UE → BSAT, UX → BSAT, BSAT → BSUC, UE → BSUC, and UX → BSUC. The two attitudinal items (ATT_1, ATT_2) were entered as covariates on BSUC. Significance was assessed with bootstrapping using **5,000 subsamples** (percentile 95% confidence intervals; two-tailed). Sign indeterminacy across bootstrap runs was resolved by aligning each construct's outer-weight signs to the full-sample solution.

### 3.1 Explained variance

The endogenous constructs are essentially unexplained: **R²(BSAT) = .013** (adj. R² = .006) and **R²(BSUC) = .008** (adj. R² = −.002). Adding the controls left R²(BSUC) unchanged at .013. By Cohen's benchmarks these values are below even the "small" threshold; the antecedents account for roughly **1%** of the variance in the outcomes. Predictive relevance was therefore not pursued, as there is no systematic variance to predict.

### 3.2 Hypothesis tests

**Table 5** reports the direct and indirect (mediation) effects. **Figure 1** depicts the structural model with standardized coefficients and R² values.

**Table 5. Structural model results and hypothesis tests (N = 312; 5,000 bootstrap subsamples).**

| Hypothesis | Relationship | β | t | p | 95% CI | Supported? |
|---|---|---|---|---|---|---|
| H1a | UE → BSAT | −.045 | 0.58 | .561 | [−.166, .112] | **No** |
| H1b | UX → BSAT | .103 | 1.37 | .171 | [−.096, .219] | **No** |
| H2 | BSAT → BSUC | .029 | 0.44 | .663 | [−.104, .143] | **No** |
| H3a | UE → BSUC | .062 | 0.79 | .428 | [−.111, .173] | **No** |
| H3b | UX → BSUC | −.060 | 0.76 | .448 | [−.185, .120] | **No** |
| H4a | UE → BSAT → BSUC (indirect) | −.001 | 0.22 | .827 | [−.013, .012] | **No** |
| H4b | UX → BSAT → BSUC (indirect) | .003 | 0.35 | .724 | [−.013, .020] | **No** |

*Note.* Controls on BSUC were also non-significant: ATT_1 (β = −.091, t = 1.23, p = .221) and ATT_2 (β = .067, t = 0.89, p = .375).

**Figure 1.** *PLS-SEM structural model with standardized path coefficients and R².* (See `Figure1_structural_model.png`.) All five direct paths are non-significant, and both endogenous R² values are near zero.

### 3.3 Interpretation and hypothesis revision

Every hypothesized relationship is **rejected**:

- **H1a / H1b (UE, UX → BSAT).** Neither user engagement nor user experience predicts brand satisfaction; both 95% CIs include zero (UX → BSAT is the strongest path at β = .103 but still p = .171). H1a and H1b are **not supported**.
- **H2 (BSAT → BSUC).** Brand satisfaction does not predict brand success (β = .029, p = .663). H2 is **not supported**.
- **H3a / H3b (UE, UX → BSUC).** No direct engagement- or experience-to-success effect emerges. H3a and H3b are **not supported**.
- **H4a / H4b (mediation via BSAT).** Mediation requires a non-trivial a-path and b-path. Because both are null, the indirect effects are effectively zero (|β| ≤ .003) with CIs spanning zero. There is **no mediation** — neither full nor partial. H4 is **not supported**.

Following the pre-registered "revise only if the data force a change" rule, the data force the strongest possible revision: rather than dropping a single non-significant path and retaining a parsimonious model, **the entire SDT-based path structure fails to replicate in this sample.** We therefore do not reframe individual paths (e.g., demoting H3a/H3b to a satisfaction-only mediation chain), because the mediator pathway (H1 and H2) is itself null. The honest conclusion is that, in these data, UE, UX, BSAT, and BSUC behave as **mutually independent** constructs.

---

## 4. Configurational analysis (fsQCA)

To test the equifinality proposition **P1**, the four composites were calibrated into fuzzy sets using the direct method with three anchors appropriate to the 7-point scale: full membership = **6.0**, crossover = **4.0**, full non-membership = **2.0** (log-odds anchored at 0.95/0.50/0.05). The resulting fuzzy scores span the full [0,1] interval, with crossover near the empirical median (calibrated means ≈ .50 for UE/UX, .51 for BSAT, .53 for BSUC), confirming well-behaved calibration with no skew toward either anchor. The outcome was high brand success (BSUC_f).

### 4.1 Analysis of necessary conditions

A condition is necessary if its consistency for the outcome is ≥ .90. As shown in **Table 6**, **no condition — present or absent — approaches necessity** (all consistencies between .56 and .60). High BSUC can occur with or without high UE, UX, or BSAT; no single SDT construct is a prerequisite for brand success.

**Table 6. Analysis of necessary conditions for high BSUC.**

| Condition | Consistency | Coverage |
|---|---|---|
| UE | .580 | .614 |
| ~UE | .575 | .607 |
| UX | .559 | .597 |
| ~UX | .603 | .631 |
| BSAT | .584 | .605 |
| ~BSAT | .565 | .610 |

*Note.* "~" denotes negation (low membership). Necessity benchmark = .90. No condition qualifies.

### 4.2 Analysis of sufficient configurations

A truth table was constructed for the three causal conditions UE_f, UX_f, BSAT_f (the outcome BSUC_f is not a causal condition), yielding 2³ = 8 configurations. Cases were assigned to the corner in which their membership exceeded 0.5. We applied a **frequency threshold of 3** and a **raw-consistency threshold of .80**, the conventional minima for a sample of this size. **Table 7** reports the full truth table.

**Table 7. Truth table for UE, UX, BSAT → high BSUC.**

| UE | UX | BSAT | n (cases) | Raw consistency |
|:--:|:--:|:--:|:--:|:--:|
| ● | ● | ● | 42 | .711 |
| ○ | ○ | ○ | 39 | .739 |
| ○ | ● | ● | 38 | .699 |
| ● | ○ | ● | 34 | .762 |
| ○ | ○ | ● | 32 | .713 |
| ○ | ● | ○ | 30 | .714 |
| ● | ● | ○ | 29 | .688 |
| ● | ○ | ○ | 28 | .723 |

*Note.* ● = condition present (high), ○ = condition absent (low). All eight configurations clear the frequency threshold (n ≥ 28), but **none reaches the .80 consistency threshold** (observed range = .688–.762). The truth table therefore yields **no rows coded 1**, and the Quine–McCluskey minimization returns an **empty solution** (no sufficient term).

Because the standard procedure produces no solution, we additionally inspected the sufficiency of single and combined "presence" conditions directly (**Table 8**) to characterize how far short of sufficiency the data fall. Consistency rises monotonically with the number of co-present high conditions — from ≈ .60 for single conditions to .711 for the fully triadic recipe (UE·UX·BSAT) — exactly the qualitative pattern P1 anticipates, **but the ceiling (.711) remains below any defensible sufficiency cut-off**, and coverage of the triadic term is low (.262). For completeness, no configuration is sufficient for the **negated** outcome either (all consistencies ≤ .65), ruling out a mirror-image explanation.

**Table 8. Sufficiency of selected configurations for high BSUC.**

| Configuration | Consistency | Raw coverage |
|---|---|---|
| UE | .614 | .580 |
| UX | .597 | .559 |
| BSAT | .605 | .584 |
| UE · UX | .653 | .360 |
| UE · BSAT | .683 | .381 |
| UX · BSAT | .653 | .382 |
| UE · UX · BSAT | .711 | .262 |

### 4.3 Interpretation relative to P1

P1 holds that multiple configurations of high UE, high UX, and high BSAT are *sufficient* for high BSUC, with no single condition necessary. The data deliver **half** of this proposition and reject the other half:

- **No single condition is necessary** — consistent with the "no necessity" clause of P1 (Table 6).
- **However, no configuration is sufficient.** Not one of the eight corners — including the theoretically privileged triadic recipe of simultaneously high engagement, experience, and satisfaction — meets the .80 consistency standard (Table 7). There are therefore **no equifinal sufficient paths** to brand success.

Consequently, **P1 is not supported.** We deliberately refrain from reporting "C1/C2/C3" solution configurations, because doing so would require lowering the consistency threshold below accepted standards (no corner reaches even .77) and would misrepresent noise as an equifinal causal structure. The configurational evidence converges with the PLS-SEM evidence: brand success is, in this sample, **unrelated** to the SDT antecedents whether modeled correlationally or set-theoretically.

---

## 5. Summary of findings

| # | Proposition / Hypothesis | Evidence | Verdict |
|---|---|---|---|
| — | Measurement quality (reliability, convergent reliability, discriminant validity, CMB) | α/CR > .90, AVE > .76, HTMT < .10, VIF ≈ 1.0 | **Strongly met** |
| H1a | UE → BSAT | β = −.045, p = .561 | Not supported |
| H1b | UX → BSAT | β = .103, p = .171 | Not supported |
| H2 | BSAT → BSUC | β = .029, p = .663 | Not supported |
| H3a | UE → BSUC | β = .062, p = .428 | Not supported |
| H3b | UX → BSUC | β = −.060, p = .448 | Not supported |
| H4 | BSAT mediates UE/UX → BSUC | indirect βs ≈ 0, CIs include 0 | Not supported |
| P1 | Equifinal sufficient configurations; no necessary condition | No necessity **and** no sufficiency | Not supported |

**Overall.** The MTVS data yield a paradoxical and noteworthy pattern: **each construct is measured with near-textbook reliability and validity, yet the constructs are mutually orthogonal.** Within-construct item correlations average ≈ .70–.74, whereas between-construct correlations average ≈ .02–.07 (max |r| = .10). As a result, every SDT-derived structural hypothesis (H1a–H4) and the configurational proposition (P1) are disconfirmed: there is no direct effect, no mediation, and no sufficient configuration linking user engagement, user experience, or brand satisfaction to brand success.

**Implication and caution.** Two readings are possible, and both should be stated transparently. (1) *Substantive:* in this avatar-mediated setting, interaction-level need satisfaction (UE, UX) and evaluative satisfaction (BSAT) may be decoupled from brand-level success (BSUC), challenging the assumed SDT causal chain. (2) *Data-integrity:* the simultaneous combination of high internal consistency with near-zero inter-construct correlations is statistically unusual for genuinely related theoretical constructs and is the signature one would expect if the four blocks were generated or sampled independently. We flag this pattern explicitly. Before advancing substantive SDT claims, we recommend verifying the data-collection and data-assembly pipeline (e.g., possible block-wise shuffling or independent simulation of construct blocks), and, if confirmed valid, replicating on an independent sample. As reported, the responsible conclusion is that **these data do not support the hypothesized SDT model of avatar-mediated brand success**, and we present that result without modification.

---

### Methods note (reproducibility)

PLS-SEM was estimated with a custom Mode-A, path-weighting implementation (converging in < 20 iterations); loadings are indicator–construct correlations, ρc and AVE follow the standard reflective formulas, HTMT follows Henseler et al. (2015), and full-collinearity VIFs follow Kock (2015). Inference used 5,000 bootstrap subsamples with construct-wise sign correction. fsQCA used direct calibration (anchors 6/4/2), Ragin-style fuzzy consistency/coverage, a corner-membership truth table (frequency ≥ 3, consistency ≥ .80), and Quine–McCluskey minimization. All scripts (`plssem.py`, `02_measurement.py`, `04_structural.py`, `05_fsqca.py`, `06_figure.py`) and intermediate outputs are included in the repository for full reproducibility.
