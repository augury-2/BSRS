# Metaverse Brand Study — Results Manuscript (Template)

> **How to turn this into a Word document with real results.** This is a structured manuscript template. Placeholders shown as `⟨…⟩` must be filled with the values produced by knitting `analysis.Rmd` (see `implementation-appendix.md`). Two ways to get a `.docx`:
> 1. **Recommended:** knit `analysis.Rmd` with `output: word_document` — it produces a results-filled Word file directly.
> 2. **From this template:** after filling the placeholders, convert with pandoc: `pandoc results-manuscript-template.md -o Results.docx`.
>
> No statistics are pre-filled here on purpose: the numbers must come from the actual analysis of `MTVS.xlsx`, not from estimates.

## Abstract (template)
This study examines how User Engagement (UE) and User Experience (UX) influence Brand Success (BSUC), directly and through Brand Satisfaction (BSAT), in a metaverse branding context (N = 312). Using PLS-SEM and fsQCA, we find ⟨summary of supported hypotheses⟩ and ⟨summary of fsQCA configurations⟩. 

## 4. Results

### 4.1 Data screening (Part A)
Sample size was N = 312, exceeding the 10-times-rule minimum (30) and the inverse-square-root minimum for the most complex regression (3 predictors into BSUC). Missing values: ⟨count/%⟩. Duplicates: ⟨count⟩. Multivariate outliers (Mahalanobis D² > χ²₀.₉₉₉,₂₀ ≈ 45.315): ⟨count⟩. Skewness ranged ⟨min⟩–⟨max⟩ and kurtosis ⟨min⟩–⟨max⟩ (within |skew| ≤ 2, |kurtosis| ≤ 7; Byrne, 2016). Predictor VIFs were ⟨range⟩ (all < 5; Hair et al., 2022).

**Table 1. Respondent demographic profile (N = 312).** *(from published aggregate counts; per-respondent demographics are confidential, so MGA is not estimable.)*

| Variable | Category | n | % |
|---|---|---|---|
| Gender | Male / Female | 143 / 169 | 46.00 / 54.00 |
| Age | 18–22 / 23–28 / 29–34 / 35–41 / 42–45 | 64 / 75 / 60 / 57 / 56 | 20.51 / 24.04 / 19.23 / 18.27 / 17.95 |
| Marital status | Single / Married w/ children / Married w/o children | 107 / 84 / 121 | 34.29 / 26.93 / 38.78 |
| Occupation | Students / Job / Business | 88 / 102 / 122 | 28.21 / 32.69 / 39.10 |
| Engagement freq. | Daily / Several-wk / Weekly / Monthly / Rarely | 52 / 98 / 73 / 54 / 35 | 16.67 / 31.41 / 23.38 / 17.31 / 11.21 |
| NFT interaction | Yes / No | 141 / 171 | 45.19 / 54.81 |
| Virtual event | Yes / No | 129 / 183 | 41.35 / 58.65 |
| Social/content | Yes / No | 164 / 148 | 52.56 / 47.44 |
| Monthly income (INR) | ≤30k / 30–50k / 50–80k / 80k+ | 57 / 80 / 100 / 75 | 18.40 / 25.64 / 32.05 / 23.91 |

**Table 2. Descriptive statistics (indicators).**

| Indicator | M | SD | Skew | Kurtosis |
|---|---|---|---|---|
| UE1…BSUC4 | ⟨M⟩ | ⟨SD⟩ | ⟨skew⟩ | ⟨kurtosis⟩ |

### 4.2 Measurement model (Part B)
**Table 3. Reliability and convergent validity.**

| Construct | Cronbach's α | ρ_A | CR | AVE |
|---|---|---|---|---|
| UE | ⟨α⟩ | ⟨ρ_A⟩ | ⟨CR⟩ | ⟨AVE⟩ |
| UX | ⟨α⟩ | ⟨ρ_A⟩ | ⟨CR⟩ | ⟨AVE⟩ |
| BSAT | ⟨α⟩ | ⟨ρ_A⟩ | ⟨CR⟩ | ⟨AVE⟩ |
| BSUC | ⟨α⟩ | ⟨ρ_A⟩ | ⟨CR⟩ | ⟨AVE⟩ |

*Thresholds: α/CR 0.70–0.95; AVE ≥ 0.50 (Hair et al., 2022). Decision: ⟨met/not met⟩.*

**Table 4. Discriminant validity — HTMT (and Fornell-Larcker in appendix).**

| | UE | UX | BSAT | BSUC |
|---|---|---|---|---|
| UE | — | ⟨HTMT⟩ | ⟨HTMT⟩ | ⟨HTMT⟩ |
| UX | | — | ⟨HTMT⟩ | ⟨HTMT⟩ |
| BSAT | | | — | ⟨HTMT⟩ |
| BSUC | | | | — |

*Threshold: HTMT < 0.85/0.90 (Henseler et al., 2015). CMB full-collinearity VIF: ⟨values⟩ (< 3.3; Kock, 2015). Harman single factor: ⟨%⟩ (< 50%).*

### 4.3 Structural model and hypotheses (Parts C, I)
**Table 5. Structural paths (5,000-resample BCa bootstrap).**

| Path | β | SE | t | p | 95% CI | Decision |
|---|---|---|---|---|---|---|
| UE → BSAT | ⟨β⟩ | ⟨SE⟩ | ⟨t⟩ | ⟨p⟩ | [⟨lo⟩, ⟨hi⟩] | ⟨sig?⟩ |
| UX → BSAT | ⟨β⟩ | ⟨SE⟩ | ⟨t⟩ | ⟨p⟩ | [⟨lo⟩, ⟨hi⟩] | ⟨sig?⟩ |
| UE → BSUC (H1) | ⟨β⟩ | ⟨SE⟩ | ⟨t⟩ | ⟨p⟩ | [⟨lo⟩, ⟨hi⟩] | ⟨supported/rejected⟩ |
| UX → BSUC (H2) | ⟨β⟩ | ⟨SE⟩ | ⟨t⟩ | ⟨p⟩ | [⟨lo⟩, ⟨hi⟩] | ⟨supported/rejected⟩ |
| BSAT → BSUC | ⟨β⟩ | ⟨SE⟩ | ⟨t⟩ | ⟨p⟩ | [⟨lo⟩, ⟨hi⟩] | ⟨sig?⟩ |

### 4.4 Mediation (Part D)
**Table 6. Indirect effects via BSAT.**

| Mediation | Indirect | 95% CI | Direct | Total | VAF | Type |
|---|---|---|---|---|---|---|
| UE → BSAT → BSUC | ⟨a·b⟩ | [⟨lo⟩, ⟨hi⟩] | ⟨c'⟩ | ⟨c⟩ | ⟨VAF⟩ | ⟨none/partial/full⟩ |
| UX → BSAT → BSUC | ⟨a·b⟩ | [⟨lo⟩, ⟨hi⟩] | ⟨c'⟩ | ⟨c⟩ | ⟨VAF⟩ | ⟨none/partial/full⟩ |

*VAF < 0.20 none; 0.20–0.80 partial; > 0.80 full (Hair et al., 2022; Nitzl et al., 2016; Zhao et al., 2010).*

### 4.5 Model quality (Part E)
- R² (adj): BSAT = ⟨R²⟩ (⟨adj⟩); BSUC = ⟨R²⟩ (⟨adj⟩) — ⟨weak/moderate/substantial⟩.
- f²: ⟨values⟩ (0.02/0.15/0.35; Cohen, 1988). Q²: BSAT = ⟨Q²⟩, BSUC = ⟨Q²⟩ (> 0 ⇒ predictive relevance).
- PLSpredict (BSUC indicators): RMSE/MAE/MAPE = ⟨values⟩; vs LM benchmark ⇒ predictive power = ⟨none/low/medium/high⟩ (Shmueli et al., 2019).

### 4.6 IPMA (Part F)
**Table 7. Importance–performance (target = BSUC).** Importance (total effect) / Performance (0–100): UE ⟨imp⟩/⟨perf⟩; UX ⟨imp⟩/⟨perf⟩; BSAT ⟨imp⟩/⟨perf⟩. Highest improvement potential: ⟨construct⟩.

### 4.7 Multi-Group Analysis (Part G)
Not estimable for this dataset. Per-respondent demographic data is confidential and was not released, so respondents cannot be assigned to groups; hypothesis H4 (demographic moderation) is **not testable** with the available data and is reported descriptively (Table 1) only.

### 4.8 fsQCA (Parts H, J)
- **Calibration:** direct anchors (6.5 / 4.0 / 2.0; Ragin, 2008) selected as primary; percentile anchors retained for robustness.
- **Necessity (Table 8):** consistency / coverage / RoN for UE_f, UX_f, BSAT_f and negations; necessary if consistency ≥ 0.90 (Schneider & Wagemann, 2012): ⟨results⟩.
- **Sufficiency (Table 9 — configurations for high BSUC_f):** raw consistency ≥ 0.80, PRI ≥ 0.70, freq ≥ 1.

| Configuration | Core / peripheral conditions | Raw cov. | Unique cov. | Consistency |
|---|---|---|---|---|
| C1 | ⟨recipe⟩ | ⟨⟩ | ⟨⟩ | ⟨⟩ |
| C2 | ⟨recipe⟩ | ⟨⟩ | ⟨⟩ | ⟨⟩ |

Overall solution coverage = ⟨⟩; overall consistency = ⟨⟩. **P1 (equifinality):** ⟨supported if ≥ 2 configurations⟩. Causal asymmetry vs ~BSUC_f: ⟨observed?⟩.

### 4.9 Robustness (Part K)
Alternative (percentile) calibration: ⟨configurations stable?⟩. Consistency-cutoff sensitivity {0.75–0.90} and frequency {1,2}: ⟨effect⟩. Bootstrapped fsQCA / leave-one-out: ⟨stable?⟩. Summary: ⟨robust vs sensitive findings⟩.

## 5. Discussion (Part N)
Interpret H1/H2/H3 and the fsQCA recipes through Self-Determination Theory, Flow Theory, Experience Economy Theory, Customer Engagement Theory, Relationship Marketing Theory, and Brand Equity Theory. Reconcile symmetric (PLS-SEM net effects) and asymmetric (fsQCA configurational) evidence: ⟨narrative⟩. Compare with prior studies: ⟨similarities/contradictions⟩. Theoretical, managerial, and policy implications: ⟨…⟩.

## 6. Conclusion (Part O)
Key findings: ⟨…⟩. Hypothesis support: H1 ⟨…⟩, H2 ⟨…⟩, H3 ⟨…⟩; H4 not testable (confidential demographics). fsQCA: ⟨…⟩. Contribution: ⟨…⟩. Limitations: confidential demographics preclude MGA; single-context sample; ⟨others⟩. Future research: ⟨…⟩.

## References
Byrne (2016); Cohen (1988); Fiss (2011); Greckhamer et al. (2018); Hair et al. (2022); Henseler et al. (2015, 2016); Kock (2015); Nitzl et al. (2016); Ragin (2008); Schneider & Wagemann (2012); Shmueli et al. (2019); Zhao et al. (2010). (Full APA 7th references in design.md.)
