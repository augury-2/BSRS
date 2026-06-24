# Requirements Document

## Introduction

This document specifies the requirements for a complete, reproducible, publication-grade quantitative analysis pipeline that analyzes the dataset `MTVS.xlsx`. The pipeline applies Partial Least Squares Structural Equation Modeling (PLS-SEM) followed by fuzzy-set Qualitative Comparative Analysis (fsQCA) to a four-construct reflective measurement model, and produces APA 7th-edition publication-ready tables, figures, and narrative suitable for an ABS 4*/Scopus Q1 outlet.

The pipeline is intended to be implementable in R (using `seminr` or `plspm` for PLS-SEM and `QCA`/`SetMethods` for fsQCA) or equivalent Python libraries. This specification is method- and tool-agnostic at the requirement level: each requirement states *what* the pipeline must produce and *which thresholds* must be met, not *how* a specific library implements it.

### Research Model

Four reflective latent constructs measured on 7-point Likert indicators (verified range 1–7):

- **User Engagement (UE)**: indicators UE1–UE5
- **User Experience (UX)**: indicators UX1–UX5
- **Brand Satisfaction (BSAT)**: indicators BSAT1–BSAT4
- **Brand Success (BSUC)**: indicators BSUC1–BSUC4
- **Optional control variables**: ATT_1, ATT_2 (included only where they improve explanatory power)

### Hypotheses and Proposition

- **H1**: UE has a positive direct effect on BSUC.
- **H2**: UX has a positive direct effect on BSUC.
- **H3**: BSAT mediates the effects of UE on BSUC and of UX on BSUC.
- **H4 (RQ-MGA — Demographic Moderation)**: The strength of one or more structural relationships in the model differs across key demographic segments (gender, age band, marital status, occupation, metaverse engagement frequency, NFT interaction, virtual event participation, social interaction/content creation, and monthly family income). **Note: H4 is not testable with the available (confidential-demographics) data; per-respondent demographic values are confidential and will not be supplied, so Multi-Group Analysis is not estimable. H4 is reported descriptively only.**
- Additional structural paths: UE → BSAT, UX → BSAT, BSAT → BSUC.
- **P1 (fsQCA)**: Multiple configurations of UE, UX, and BSAT lead to High Brand Success, exhibiting equifinality and causal asymmetry.

### Dataset Facts Verified Against `MTVS.xlsx` (Re-verified This Session)

These facts were confirmed by inspecting the actual file and are recorded so that downstream assumptions are traceable:

- The file contains a single sheet (`Sheet1`) with **312 data rows** and **22 columns**.
- Columns are exactly: `S.No`, `ID`, `UE1`–`UE5`, `UX1`–`UX5`, `BSAT1`–`BSAT4`, `BSUC1`–`BSUC4`, `ATT_1`, `ATT_2`.
- All 20 substantive indicators take **integer values in the range 1–7** (7-point Likert), confirming the assumed scale.
- There are **0 missing values** and **0 duplicate rows** (by `ID` and by full row) in the current file.
- **No per-respondent demographic columns are present** in `MTVS.xlsx`. The file does NOT contain gender, age, marital status, occupation, metaverse engagement frequency, NFT interaction, virtual event participation, social interaction/content creation, or monthly family income as per-respondent fields.
- A **Respondent Demographic Profile (Table 1, N = 312)** has been provided separately, but only as **aggregate category counts and percentages**, not as per-respondent values. The provided profile covers nine demographic variables: Gender, Age (Years), Marital Status, Occupation, Metaverse Engagement Frequency, NFT Interaction, Virtual Event Participation, Social Interaction/Content Creation, and Monthly Family Income. **Table 1 is reported from these published aggregate counts only.**
- **Per-respondent demographic data is confidential by design:** respondents were given a confidentiality assurance, and per-respondent demographic values will **not** be released or merged into the analysis dataset. Only the aggregate category counts in the Respondent Demographic Profile (Table 1) are available.
- **Multi-Group Analysis (PART G) is NOT ESTIMABLE for this dataset:** because per-respondent demographic values are confidential and will not be supplied, individual respondents cannot be assigned to demographic groups. Consequently, hypothesis **H4 (demographic moderation) is not testable** with the available data. Multi-Group Analysis is therefore reported as not estimable (Requirement 12), and the ID-keyed merge / MICOM / PLS-MGA procedure is retained only as an **optional, conditional path** that would apply if non-confidential per-respondent demographic data ever became available internally (Requirement 2).

## Glossary

- **Analysis_Pipeline**: The complete software system that ingests `MTVS.xlsx`, executes all analysis stages (PARTS A–P), and emits tables, figures, and narrative artifacts.
- **Data_Loader**: The pipeline component that reads `MTVS.xlsx`, validates structure, and produces the analysis dataset.
- **Screening_Module**: The pipeline component that performs data screening (PART A).
- **Composite_Builder**: The pipeline component that computes mean-based composite scores for fsQCA and descriptive use.
- **Measurement_Evaluator**: The pipeline component that evaluates the reflective measurement model (PART B).
- **Structural_Estimator**: The pipeline component that estimates the structural model and runs bootstrapping (PART C).
- **Mediation_Analyzer**: The pipeline component that decomposes direct, indirect, and total effects (PART D).
- **Quality_Assessor**: The pipeline component that computes explanatory and predictive quality metrics (PART E).
- **IPMA_Module**: The pipeline component that performs Importance-Performance Map Analysis (PART F).
- **MGA_Module**: The pipeline component that performs Multi-Group Analysis across demographic segments (PART G).
- **FSQCA_Module**: The pipeline component that performs fuzzy-set Qualitative Comparative Analysis (PART H).
- **Robustness_Module**: The pipeline component that performs robustness and sensitivity checks (PART K).
- **Reporting_Module**: The pipeline component that assembles APA 7th-edition tables, figures, discussion, and conclusion (PARTS L–P).
- **Indicator**: A single measured Likert item (e.g., UE1).
- **Construct**: A latent reflective variable (UE, UX, BSAT, BSUC).
- **Composite_Score**: The arithmetic mean of a construct's indicators: UE = mean(UE1..UE5), UX = mean(UX1..UX5), BSAT = mean(BSAT1..BSAT4), BSUC = mean(BSUC1..BSUC4).
- **Calibration**: The fsQCA transformation of an interval/composite variable into a fuzzy-set membership score in [0, 1].
- **Consistency (fsQCA)**: The degree to which a condition or configuration is a subset of the outcome (set-theoretic consistency).
- **Coverage (fsQCA)**: The proportion of the outcome explained by a condition or configuration.
- **RoN**: Relevance of Necessity, an auxiliary measure used to assess trivial necessity.
- **PRI**: Proportional Reduction in Inconsistency, used in truth-table consistency assessment.
- **VAF**: Variance Accounted For, the ratio of indirect effect to total effect used to classify mediation.
- **HTMT**: Heterotrait-Monotrait ratio of correlations, used for discriminant validity.
- **AVE**: Average Variance Extracted.
- **Run_Manifest**: A machine-readable record of software versions, package versions, random seeds, input file hash, and run timestamp emitted by the pipeline.
- **Grouping_Variable**: A categorical per-respondent demographic variable (Gender, Age band, Marital Status, Occupation, Metaverse Engagement Frequency, NFT Interaction, Virtual Event Participation, Social Interaction/Content Creation, or Monthly Family Income) used to partition the sample for Multi-Group Analysis.
- **Demographic_Profile**: The Respondent Demographic Profile (Table 1) reporting category counts and percentages for each Grouping_Variable across the N = 312 sample.
- **MICOM**: Measurement Invariance of Composite Models, a three-step procedure (configural invariance, compositional invariance, and equality of composite means and variances) used to establish measurement invariance prior to Multi-Group Analysis (Henseler et al., 2016).
- **PLS-MGA**: Partial Least Squares Multi-Group Analysis, a test of the significance of the difference in a structural path estimate between groups (Hair et al., 2022).
- **OTG**: Overall Test of Group differences, an omnibus test used to assess differences across more than two groups.

## Requirements

### Requirement 1: Data Ingestion and Structural Validation

**User Story:** As a researcher, I want the pipeline to load and validate the dataset deterministically, so that every downstream analysis runs on a verified, well-formed dataset.

#### Acceptance Criteria

1. WHEN the pipeline is executed, THE Data_Loader SHALL read the single worksheet from `MTVS.xlsx` into an in-memory analysis dataset.
2. THE Data_Loader SHALL verify that the analysis dataset contains the 20 substantive indicator columns UE1–UE5, UX1–UX5, BSAT1–BSAT4, and BSUC1–BSUC4.
3. THE Data_Loader SHALL verify that the control columns ATT_1 and ATT_2 are present and retain them for optional use.
4. IF any required indicator column is absent from the dataset, THEN THE Data_Loader SHALL halt execution and report the names of the missing columns.
5. THE Data_Loader SHALL verify that every substantive indicator contains only integer values within the closed interval 1 to 7, and SHALL report the count of values outside that interval per indicator.
6. IF any substantive indicator contains a value outside the closed interval 1 to 7, THEN THE Data_Loader SHALL record the violating indicator name, row identifier, and value in the screening report and SHALL continue processing the dataset.
7. WHERE no out-of-range values are detected, THE Data_Loader SHALL skip generation of the out-of-range screening report rather than emit an empty report.
8. THE Data_Loader SHALL report the observed row count and SHALL state whether the row count equals 312.
9. THE Data_Loader SHALL exclude the `S.No` and `ID` columns from all statistical computations while retaining `ID` as a case label.
10. THE Data_Loader SHALL detect whether the per-respondent demographic grouping columns Gender, Age band, Marital Status, Occupation, Metaverse Engagement Frequency, NFT Interaction, Virtual Event Participation, Social Interaction/Content Creation, and Monthly Family Income are present in the analysis dataset.
11. WHERE the demographic grouping columns are present, THE Data_Loader SHALL report, for each demographic variable, the observed count and percentage of every category, and SHALL compare each observed category frequency against the expected Respondent Demographic Profile (Table 1; N = 312) and flag any category whose observed count deviates from the expected count.
12. IF one or more demographic grouping columns are absent from the dataset, THEN THE Data_Loader SHALL record that per-respondent demographic data is unavailable, SHALL flag the data dependency required for Multi-Group Analysis (Requirement 2), and SHALL continue executing the analysis stages that do not require grouping variables.

### Requirement 2: Demographic Grouping Variables and Multi-Group Analysis Data Dependency

**User Story:** As a researcher, I want the confidentiality status of the per-respondent demographic variables recorded explicitly, so that Multi-Group Analysis is correctly reported as not estimable and any future conditional path is documented.

#### Acceptance Criteria

1. THE Data_Loader SHALL record that the following per-respondent demographic variables are confidential and unavailable by design, and SHALL name them as the Grouping_Variables that Multi-Group Analysis would require: Gender, Age band, Marital Status, Occupation, Metaverse Engagement Frequency, NFT Interaction, Virtual Event Participation, Social Interaction/Content Creation, and Monthly Family Income.
2. THE Data_Loader SHALL report that respondents were given a confidentiality assurance, that per-respondent demographic values will not be released or merged, and that the current input file contains only the 20 substantive indicators and the controls ATT_1 and ATT_2.
3. THE Data_Loader SHALL state that the aggregate category counts in the Respondent Demographic Profile (Table 1) are insufficient to assign individual respondents to groups, and SHALL record that the aggregate counts are the only demographic data available.
4. THE MGA_Module SHALL report Multi-Group Analysis as NOT ESTIMABLE for this dataset because per-respondent demographic data is confidential and will not be supplied, and SHALL record hypothesis H4 as not testable with the available data.

##### Conditional Path (applies only if non-confidential per-respondent demographic data ever becomes available internally)

5. WHERE non-confidential per-respondent demographic values become available internally, THE Data_Loader SHALL apply a documented merge procedure that joins those values to the analysis dataset on the `ID` case label and SHALL preserve the row count at 312 after the merge.
6. WHERE per-respondent demographic values are merged, THE Data_Loader SHALL validate that each demographic variable's category frequencies match the Respondent Demographic Profile (Table 1), and IF any demographic variable's category counts do not sum to 312, THEN THE Data_Loader SHALL halt and report the discrepancy.
7. WHERE per-respondent demographic values are merged, THE MGA_Module SHALL perform Multi-Group Analysis as specified in the conditional block of Requirement 12 (MICOM followed by permutation/PLS-MGA testing).

### Requirement 3: Reproducibility and Run Provenance

**User Story:** As a reviewer, I want the analysis to be fully reproducible, so that reported results can be independently regenerated.

#### Acceptance Criteria

1. THE Analysis_Pipeline SHALL set a fixed random seed before any stochastic procedure, and SHALL record the seed value in the Run_Manifest.
2. WHEN bootstrapping, permutation, or resampling procedures are executed, THE Analysis_Pipeline SHALL use the recorded seed so that repeated executions produce identical numerical results.
3. THE Analysis_Pipeline SHALL emit a Run_Manifest that records the programming language version, every analysis package name and version, the random seed, the input file name, a content hash of the input file, and the run timestamp.
4. WHEN the pipeline is executed twice with the same input file and the same seed, THE Analysis_Pipeline SHALL produce identical reported statistics to at least three decimal places.
5. THE Analysis_Pipeline SHALL document, in the Run_Manifest, the chosen implementation stack (R or Python) and the specific estimation library used for PLS-SEM and for fsQCA.

### Requirement 4: Composite Variable Construction and Missing-Value Handling

**User Story:** As an analyst, I want mean-based composite scores computed with a documented missing-value procedure, so that fsQCA and descriptive analyses use consistent inputs.

#### Acceptance Criteria

1. THE Composite_Builder SHALL compute UE as the arithmetic mean of UE1 through UE5, UX as the mean of UX1 through UX5, BSAT as the mean of BSAT1 through BSAT4, and BSUC as the mean of BSUC1 through BSUC4.
2. THE Composite_Builder SHALL apply a documented missing-value procedure and SHALL report, for each construct, the number of cases affected by missing values.
3. WHERE one or more indicators of a construct are missing for a case, THE Composite_Builder SHALL compute the Composite_Score using the documented missing-value rule and SHALL record the rule applied.
4. WHEN the current `MTVS.xlsx` is processed, THE Composite_Builder SHALL report zero cases affected by missing values, consistent with the verified dataset facts.
5. THE Composite_Builder SHALL report the minimum, maximum, mean, and standard deviation of each Composite_Score.

### Requirement 5: PART A — Data Screening and Assumption Checks

**User Story:** As a researcher, I want comprehensive data screening, so that the suitability of the data for PLS-SEM and fsQCA is established and reported.

#### Acceptance Criteria

1. THE Screening_Module SHALL report the achieved sample size and SHALL state whether it meets or exceeds the minimum recommended by the inverse-square-root method and the 10-times rule for the most complex regression in the model (Hair et al., 2022).
2. THE Screening_Module SHALL report a missing-value analysis giving the count and percentage of missing values per indicator and the overall percentage of missing data.
3. THE Screening_Module SHALL report the number of duplicate cases detected by `ID` and by full-row comparison.
4. THE Screening_Module SHALL detect multivariate outliers using Mahalanobis distance evaluated against a chi-square critical value at p < 0.001 with degrees of freedom equal to the number of indicators, and SHALL report each flagged case identifier and distance.
5. THE Screening_Module SHALL produce per-indicator boxplots and SHALL report univariate outliers using the 1.5 × interquartile range rule.
6. WHERE a dependent composite regression is used for influence diagnostics, THE Screening_Module SHALL report Cook's distance per case and SHALL flag a case as influential only when both its Cook's distance and the 4/n threshold are valid finite values and the distance exceeds the threshold.
7. THE Screening_Module SHALL report, per indicator, the mean, standard deviation, skewness, and kurtosis, and SHALL flag indicators whose absolute skewness exceeds 2 or absolute kurtosis exceeds 7 (Byrne, 2016).
8. THE Screening_Module SHALL produce a histogram, a density plot, and a Q-Q plot for each indicator.
9. THE Screening_Module SHALL produce a correlation heatmap and a scatterplot matrix across the substantive indicators.
10. THE Screening_Module SHALL produce a descriptive statistics table, a Pearson correlation matrix, and a covariance matrix across constructs and indicators as specified in PART M.
11. THE Screening_Module SHALL compute the Variance Inflation Factor for the predictors of each endogenous construct and SHALL flag any VIF value at or above 5 as indicating potential multicollinearity (Hair et al., 2022).

### Requirement 6: PART A — Respondent Demographic Profile (Table 1)

**User Story:** As a researcher, I want a respondent demographic profile table, so that the composition of the N = 312 sample is documented per APA descriptive conventions.

#### Acceptance Criteria

1. THE Reporting_Module SHALL produce the Respondent Demographic Profile table (Table 1) from the published aggregate category counts and percentages for all nine demographic variables, based on N = 312, because per-respondent demographic values are confidential and unavailable (Requirement 2).
2. THE Reporting_Module SHALL report Gender as Male (143; 46.00%) and Female (169; 54.00%).
3. THE Reporting_Module SHALL report Age (Years) as 18–22 (64; 20.51%), 23–28 (75; 24.04%), 29–34 (60; 19.23%), 35–41 (57; 18.27%), and 42–45 (56; 17.95%).
4. THE Reporting_Module SHALL report Marital Status as Single (107; 34.29%), Married with children (84; 26.93%), and Married without children (121; 38.78%).
5. THE Reporting_Module SHALL report Occupation as Students (88; 28.21%), Job (102; 32.69%), and Business (122; 39.10%).
6. THE Reporting_Module SHALL report Metaverse Engagement Frequency as Daily (52; 16.67%), Several times a week (98; 31.41%), Weekly (73; 23.38%), Monthly (54; 17.31%), and Rarely (35; 11.21%).
7. THE Reporting_Module SHALL report NFT Interaction as Yes (141; 45.19%) and No (171; 54.81%).
8. THE Reporting_Module SHALL report Virtual Event Participation as Yes (129; 41.35%) and No (183; 58.65%).
9. THE Reporting_Module SHALL report Social Interaction/Content Creation as Yes (164; 52.56%) and No (148; 47.44%).
10. THE Reporting_Module SHALL report Monthly Family Income as INR 30,000 or less (57; 18.40%), INR 30,001–50,000 (80; 25.64%), INR 50,001–80,000 (100; 32.05%), and INR 80,001 and above (75; 23.91%).
11. THE Reporting_Module SHALL verify that each demographic variable's category counts sum to 312 and SHALL flag any demographic variable whose category percentages do not sum to 100% within rounding tolerance.
12. THE Reporting_Module SHALL format the Respondent Demographic Profile table per APA 7th-edition conventions, including a table number, an italicized title, column headers, and explanatory notes.
13. THE Reporting_Module SHALL annotate Table 1 to state that the counts derive from the published aggregate Respondent Demographic Profile, that per-respondent demographic data is confidential and unavailable, and that Multi-Group Analysis is therefore not estimable for this dataset (Requirements 2 and 12). WHERE non-confidential per-respondent demographic values become available internally, THE Reporting_Module MAY regenerate Table 1 directly from those per-respondent values.

### Requirement 7: PART B — Reflective Measurement Model Evaluation

**User Story:** As a researcher, I want a full reflective measurement model assessment, so that construct reliability and validity meet publication thresholds before structural interpretation.

#### Acceptance Criteria

1. THE Measurement_Evaluator SHALL report standardized outer loadings for every indicator and SHALL flag loadings below 0.708 (Hair et al., 2022).
2. THE Measurement_Evaluator SHALL report outer weights, communality, and redundancy for every indicator.
3. THE Measurement_Evaluator SHALL report a cross-loadings table across all constructs.
4. THE Measurement_Evaluator SHALL report indicator reliability as the squared outer loading for every indicator and SHALL flag values below 0.50.
5. THE Measurement_Evaluator SHALL report Cronbach's alpha, rho_A, and composite reliability for each construct, and SHALL flag values below 0.70 or above 0.95 (Hair et al., 2022), treating a perfect value of 1.0 as exceeding the 0.95 upper threshold.
6. THE Measurement_Evaluator SHALL report Average Variance Extracted for each construct and SHALL flag any AVE below 0.50 as failing convergent validity.
7. THE Measurement_Evaluator SHALL assess discriminant validity using the Fornell-Larcker criterion and SHALL flag any case where the square root of a construct's AVE is not greater than its correlations with other constructs.
8. THE Measurement_Evaluator SHALL report the Heterotrait-Monotrait ratio for every construct pair and SHALL flag any HTMT value at or above 0.85 (conservative) and at or above 0.90 (liberal) (Henseler et al., 2015).
9. THE Measurement_Evaluator SHALL report inner-model (full collinearity) VIF for each construct and SHALL flag values at or above 3.3 as indicating potential common method bias (Kock, 2015).
10. THE Measurement_Evaluator SHALL assess common method bias and SHALL report the result of a documented test (such as Harman's single-factor test and full collinearity assessment).
11. IF no common method bias test has been performed, THEN THE Measurement_Evaluator SHALL report that the assessment is required but incomplete and SHALL record this as a validation failure.
12. THE Measurement_Evaluator SHALL report model fit indices SRMR, NFI, RMS_theta, d_ULS, and d_G, and SHALL flag SRMR values above 0.08 (Henseler et al., 2014).
13. WHERE a chi-square statistic is available from the estimation method, THE Measurement_Evaluator SHALL report it; WHERE it is not available for PLS-SEM, THE Measurement_Evaluator SHALL state that it is not applicable and explain why.

### Requirement 8: PART C — Structural Model Estimation and Bootstrapping

**User Story:** As a researcher, I want bootstrapped structural path estimates, so that hypothesis decisions rest on robust inference.

#### Acceptance Criteria

1. THE Structural_Estimator SHALL estimate the standardized path coefficients for UE → BSAT, UX → BSAT, UE → BSUC, UX → BSUC, and BSAT → BSUC.
2. THE Structural_Estimator SHALL execute bootstrapping with 5000 resamples and SHALL apply the bias-corrected and accelerated method for confidence interval construction (Hair et al., 2022).
3. FOR EACH structural path, THE Structural_Estimator SHALL report the standardized beta, standard error, t-statistic, p-value, and 95% confidence interval.
4. FOR EACH structural path, THE Structural_Estimator SHALL record a decision of "supported" or "rejected" using a two-tailed significance threshold of p < 0.05, and SHALL also report significance at p < 0.01 and p < 0.001.
5. THE Structural_Estimator SHALL produce a structural path diagram annotated with standardized coefficients and significance markers.
6. WHERE the control variables ATT_1 and ATT_2 measurably improve the explained variance of BSUC, THE Structural_Estimator SHALL include them as predictors of BSUC and SHALL report their path estimates; otherwise THE Structural_Estimator SHALL report the comparison that justified their exclusion.

### Requirement 9: PART D — Mediation Analysis

**User Story:** As a researcher, I want a rigorous mediation analysis, so that the mediating role of BSAT is correctly classified.

#### Acceptance Criteria

1. THE Mediation_Analyzer SHALL compute the specific indirect effect of UE on BSUC through BSAT and the specific indirect effect of UX on BSUC through BSAT.
2. FOR EACH indirect effect, THE Mediation_Analyzer SHALL report the point estimate, standard error, t-statistic, p-value, and bias-corrected 95% confidence interval from the 5000-resample bootstrap.
3. THE Mediation_Analyzer SHALL report the direct effect, the indirect effect, and the total effect for each of the UE → BSUC and UX → BSUC relationships.
4. THE Mediation_Analyzer SHALL compute the Variance Accounted For for each mediated relationship as the ratio of the indirect effect to the total effect.
5. THE Mediation_Analyzer SHALL classify each mediated relationship as no mediation, partial mediation, or full mediation using the decision logic of Zhao et al. (2010) and Nitzl et al. (2016), and SHALL report VAF-based interpretation thresholds (VAF below 0.20 indicates no mediation, 0.20–0.80 partial, above 0.80 full) per Hair et al. (2022).
6. IF a bootstrap confidence interval for an indirect effect excludes zero, THEN THE Mediation_Analyzer SHALL record the indirect effect as statistically significant.

### Requirement 10: PART E — Model Quality and Predictive Relevance

**User Story:** As a researcher, I want explanatory and predictive quality metrics, so that the model's usefulness is demonstrated beyond significance testing.

#### Acceptance Criteria

1. THE Quality_Assessor SHALL report R² and adjusted R² for each endogenous construct (BSAT and BSUC) and SHALL interpret magnitudes against the 0.25/0.50/0.75 weak/moderate/substantial benchmarks (Hair et al., 2022).
2. THE Quality_Assessor SHALL report f² effect sizes for every predictor-endogenous relationship and SHALL interpret them against the 0.02/0.15/0.35 small/medium/large benchmarks (Cohen, 1988).
3. THE Quality_Assessor SHALL compute Q² via blindfolding for each endogenous construct and SHALL record predictive relevance when Q² exceeds zero.
4. THE Quality_Assessor SHALL run PLSpredict and SHALL report RMSE, MAE, and MAPE for the indicators of the key endogenous construct.
5. THE Quality_Assessor SHALL compare the PLS-SEM PLSpredict errors against a naive linear benchmark model and SHALL record, per indicator, whether the PLS-SEM error is lower than the benchmark.
6. THE Quality_Assessor SHALL classify the predictive power of the model as none, low, medium, or high based on the proportion of indicators for which PLS-SEM outperforms the benchmark, applying the thresholds 0% = none, above 0% to 25% = low, above 25% to 75% = medium, and above 75% = high (Shmueli et al., 2019).

### Requirement 11: PART F — Importance-Performance Map Analysis

**User Story:** As a manager, I want an IPMA, so that I can prioritize the constructs that most improve Brand Success.

#### Acceptance Criteria

1. THE IPMA_Module SHALL compute the total effect (importance) and the rescaled mean score (performance) of UE, UX, and BSAT with respect to the target construct BSUC.
2. THE IPMA_Module SHALL produce an importance-performance map with four quadrants and SHALL place each predictor construct in the appropriate quadrant.
3. THE IPMA_Module SHALL report a table of importance and performance values for each predictor construct.
4. THE IPMA_Module SHALL derive managerial implications that identify which constructs offer the highest improvement potential (high importance, low performance).

### Requirement 12: PART G — Multi-Group Analysis Across Demographic Segments

**User Story:** As a researcher, I want multi-group analysis across demographic segments, so that I can test whether measurement properties and structural relationships differ across respondent groups (H4).

#### Acceptance Criteria

1. FOR the current dataset, THE MGA_Module SHALL report Multi-Group Analysis as NOT ESTIMABLE because per-respondent demographic data is confidential and unavailable (Requirement 2), and SHALL state that hypothesis H4 is not testable with the available data and is reported descriptively only.
2. THE MGA_Module SHALL name the Grouping_Variables that Multi-Group Analysis would require (Gender, Age band, Marital Status, Occupation, Metaverse Engagement Frequency, NFT Interaction, Virtual Event Participation, Social Interaction/Content Creation, and Monthly Family Income) and SHALL record that per-respondent values for these variables will not be supplied.

##### Conditional Block (applies only WHERE non-confidential per-respondent demographic data is available internally)

3. WHERE non-confidential per-respondent demographic data is available internally, THE MGA_Module SHALL perform Multi-Group Analysis across the demographic Grouping_Variables.
4. WHERE non-confidential per-respondent demographic data is available internally, THE MGA_Module SHALL treat the dichotomous variables Gender, NFT Interaction, Virtual Event Participation, and Social Interaction/Content Creation as direct two-group comparisons.
5. WHERE non-confidential per-respondent demographic data is available internally, THE MGA_Module SHALL compare the multi-category variables Age band, Marital Status, Occupation, Metaverse Engagement Frequency, and Monthly Family Income either through pairwise comparisons of all category pairs or through the Overall Test of Group differences (OTG)/omnibus approach, and SHALL document which comparison strategy is applied to each multi-category variable.
6. WHERE non-confidential per-respondent demographic data is available internally, FOR EACH Grouping_Variable, THE MGA_Module SHALL assess measurement invariance using the MICOM procedure, comprising the configural invariance step, the compositional invariance step, and the equality-of-composite-means-and-variances step (Henseler et al., 2016).
7. WHERE non-confidential per-respondent demographic data is available internally AND at least partial measurement invariance is established, THE MGA_Module SHALL perform a permutation test and the PLS-MGA test for each structural path and SHALL report, per group, the standardized path estimate, the absolute group difference, and the p-value of the difference (Hair et al., 2022).
8. WHERE non-confidential per-respondent demographic data is available internally, FOR EACH path-by-group comparison, THE MGA_Module SHALL record a decision of significant or non-significant group difference using a two-tailed threshold of p ≤ 0.05.
9. WHERE non-confidential per-respondent demographic data is available internally, THE MGA_Module SHALL evaluate the sample-size adequacy of each subgroup against the inverse-square-root method and the 10-times rule applied per subgroup, and SHALL flag any subgroup that is underpowered for structural estimation (Hair et al., 2022).
10. WHERE non-confidential per-respondent demographic data is available internally AND a subgroup is flagged as underpowered, THE MGA_Module SHALL report the affected group comparison with an explicit caution and SHALL still report the estimated group difference and its p-value.
11. WHERE non-confidential per-respondent demographic data is available internally, THE MGA_Module SHALL produce an APA-formatted multi-group results table reporting, per Grouping_Variable and per structural path, the per-group path estimates, the group difference, the difference p-value, and the invariance decision.

### Requirement 13: PART H — fsQCA Calibration

**User Story:** As a researcher, I want defensible fuzzy-set calibration, so that conditions and the outcome are correctly transformed into fuzzy membership.

#### Acceptance Criteria

1. THE FSQCA_Module SHALL calibrate UE, UX, BSAT, and BSUC into fuzzy sets UE_f, UX_f, BSAT_f, and BSUC_f with membership values in the closed interval 0 to 1.
2. THE FSQCA_Module SHALL perform direct calibration using anchors of 6.5 for full membership, 4.0 for the crossover point, and 2.0 for full non-membership (Ragin, 2008).
3. THE FSQCA_Module SHALL perform percentile-based calibration using the 95th percentile for full membership, the 50th percentile for the crossover point, and the 5th percentile for full non-membership.
4. THE FSQCA_Module SHALL compare the direct-anchor and percentile-based calibrations and SHALL justify which calibration is more appropriate for this dataset, referencing the indicator scale range and the empirical distribution.
5. WHEN a calibrated membership value equals exactly 0.5, THE FSQCA_Module SHALL adjust the value away from 0.5 by a documented small constant to avoid dropping cases from the analysis (Fiss, 2011).
6. THE FSQCA_Module SHALL report the calibration anchors, the resulting membership distribution, and the number of cases with membership above 0.5 for each fuzzy set.

### Requirement 14: PART H — Necessity Analysis

**User Story:** As a researcher, I want a necessity analysis, so that necessary conditions for High Brand Success are identified before sufficiency testing.

#### Acceptance Criteria

1. THE FSQCA_Module SHALL test each single condition (UE_f, UX_f, BSAT_f) and its negation for necessity with respect to the outcome High BSUC_f and the negated outcome.
2. FOR EACH tested condition, THE FSQCA_Module SHALL report consistency, coverage, and Relevance of Necessity.
3. THE FSQCA_Module SHALL classify a condition as necessary only when its necessity consistency is at or above 0.90 (Schneider & Wagemann, 2012).
4. THE FSQCA_Module SHALL produce a necessity analysis table and SHALL flag any necessary condition whose Relevance of Necessity indicates triviality.

### Requirement 15: PART H — Truth Table Construction and Logical Minimization

**User Story:** As a researcher, I want a truth table and Boolean minimization, so that sufficient configurations for High Brand Success are derived transparently.

#### Acceptance Criteria

1. THE FSQCA_Module SHALL construct a truth table of all 2^k logical combinations of the conditions UE_f, UX_f, and BSAT_f.
2. FOR EACH truth-table row, THE FSQCA_Module SHALL report the number of cases, the raw consistency, and the PRI consistency.
3. THE FSQCA_Module SHALL apply a frequency cutoff of at least 1 case per row given the sample size and SHALL document the chosen frequency cutoff.
4. THE FSQCA_Module SHALL apply a raw consistency cutoff of at least 0.80 and a PRI cutoff of at least 0.70 for designating rows as sufficient, and SHALL document the chosen cutoffs (Ragin, 2008; Greckhamer et al., 2018).
5. THE FSQCA_Module SHALL derive the complex solution, the parsimonious solution, and the intermediate solution via Boolean minimization.
6. THE FSQCA_Module SHALL document the directional expectations (counterfactual assumptions) used to derive the intermediate solution.

### Requirement 16: PART H — Configuration Analysis and Solution Reporting

**User Story:** As a researcher, I want a fully annotated configuration analysis, so that pathways to High Brand Success are interpretable as recipes.

#### Acceptance Criteria

1. THE FSQCA_Module SHALL report, for the intermediate solution, each configuration with its core conditions, peripheral conditions, and absent conditions using the core/peripheral distinction of Fiss (2011).
2. FOR EACH configuration, THE FSQCA_Module SHALL report raw coverage, unique coverage, and consistency.
3. THE FSQCA_Module SHALL report the overall solution coverage and overall solution consistency.
4. THE FSQCA_Module SHALL present configurations using the standard fsQCA notation (filled circle for core present, small circle for peripheral present, crossed-out circle for absent, blank for "don't care").
5. THE FSQCA_Module SHALL interpret the configurations in terms of equifinality, causal asymmetry, and the existence of multiple pathways, and SHALL state each configuration as a recipe in plain language.

### Requirement 17: PART H — fsQCA Visualizations

**User Story:** As a researcher, I want the standard fsQCA visual diagnostics, so that set relationships and configurations are communicated visually.

#### Acceptance Criteria

1. THE FSQCA_Module SHALL produce an XY plot of condition membership against outcome membership for each sufficient configuration, with the consistency diagonal marked.
2. THE FSQCA_Module SHALL produce a truth-table visualization, a configuration plot, a membership plot, a necessity plot, a Venn diagram of set relations, and a configuration matrix figure.
3. EACH fsQCA figure SHALL include a descriptive title, axis labels, and a legend sufficient for standalone interpretation.

### Requirement 18: PART I — Hypothesis Testing Decision Table

**User Story:** As a researcher, I want a consolidated hypothesis decision table, so that hypothesis outcomes are presented in one publication-ready artifact.

#### Acceptance Criteria

1. THE Reporting_Module SHALL produce a hypothesis decision table listing H1 and H2 with the corresponding path, standardized beta, t-statistic, p-value, 95% confidence interval, and a decision of supported or rejected.
2. THE Reporting_Module SHALL present H3 with the indirect effect estimate, confidence interval, VAF, mediation type, and a decision of supported or rejected.
3. THE Reporting_Module SHALL flag any inconsistency between a decision in the hypothesis table and the corresponding statistics reported in PARTS C and D for user review, and SHALL still produce the hypothesis table.

### Requirement 19: PART J — Proposition Testing (fsQCA) Configuration Table

**User Story:** As a researcher, I want a proposition-testing table, so that proposition P1 is evaluated against the fsQCA configurations.

#### Acceptance Criteria

1. THE Reporting_Module SHALL produce a configuration table that maps proposition P1 to the derived sufficient configurations for High Brand Success.
2. THE Reporting_Module SHALL record P1 as supported only when at least two distinct sufficient configurations meet the consistency and coverage cutoffs, thereby demonstrating equifinality.
3. THE Reporting_Module SHALL state whether causal asymmetry is observed by comparing configurations for High BSUC_f against configurations for the negated outcome.

### Requirement 20: PART K — Robustness and Sensitivity Analysis

**User Story:** As a researcher, I want robustness checks, so that the fsQCA conclusions are shown to be stable under reasonable analytic choices.

#### Acceptance Criteria

1. THE Robustness_Module SHALL re-run the fsQCA using an alternative calibration (the calibration not selected in Requirement 13) and SHALL report whether the solution configurations change.
2. THE Robustness_Module SHALL perform a sensitivity analysis by varying the raw consistency cutoff and the frequency cutoff across a documented range and SHALL report the effect on the derived configurations.
3. THE Robustness_Module SHALL perform a bootstrapped fsQCA and SHALL report the stability of consistency and coverage across resamples.
4. THE Robustness_Module SHALL perform a leave-one-out analysis and SHALL report whether removing any single case alters the solution configurations.
5. THE Robustness_Module SHALL compare the solutions produced under the alternative analytic choices and SHALL summarize which findings are robust and which are sensitive (Schneider & Wagemann, 2012).

### Requirement 21: PART L — Publication-Quality Figures

**User Story:** As an author, I want all figures rendered at publication quality, so that they are accepted by an ABS 4*/Scopus Q1 journal without rework.

#### Acceptance Criteria

1. THE Reporting_Module SHALL render every raster-format figure at a resolution of at least 300 dots per inch, and SHALL render figures in a vector format where resolution independence is preferred.
2. THE Reporting_Module SHALL produce the complete figure set comprising: per-indicator histograms, density plots, and Q-Q plots; the correlation heatmap; the scatterplot matrix; the structural path diagram with standardized coefficients; the IPMA quadrant map; and the fsQCA figures specified in Requirement 17.
3. EACH figure SHALL carry a figure number, a descriptive caption, and labeled axes consistent with APA 7th-edition figure formatting.
4. THE Reporting_Module SHALL use a colour palette and font sizing that remain legible in grayscale print.

### Requirement 22: PART M — APA 7th-Edition Tables

**User Story:** As an author, I want research-paper-ready APA tables, so that statistical results are presentable without reformatting.

#### Acceptance Criteria

1. THE Reporting_Module SHALL format every results table per APA 7th-edition conventions, including a table number, an italicized title, column headers, and explanatory notes.
2. EACH results table SHALL report the relevant statistics, the applicable threshold, and an interpretation or decision column where a decision is implied.
3. THE Reporting_Module SHALL produce, at minimum, tables for: descriptive statistics; correlation matrix; covariance matrix; outer loadings and cross-loadings; reliability and convergent validity (alpha, rho_A, CR, AVE); discriminant validity (Fornell-Larcker and HTMT); collinearity (VIF); structural path results; mediation results; R²/adjusted R²/Q²/f²; PLSpredict; IPMA; calibration anchors; necessity analysis; truth table; configuration solutions; robustness comparison; and the hypothesis and proposition decision tables.
4. THE Reporting_Module SHALL report numeric values to a consistent number of decimal places per APA convention (two or three decimals as appropriate) across all tables.

### Requirement 23: PART N — Theory-Grounded Discussion

**User Story:** As an author, I want a discussion grounded in established theory, so that the empirical findings are interpreted within the relevant theoretical frameworks.

#### Acceptance Criteria

1. THE Reporting_Module SHALL produce a discussion that interprets the supported and rejected hypotheses with explicit reference to Self-Determination Theory, Flow Theory, Experience Economy Theory, Customer Engagement Theory, Relationship Marketing Theory, and Brand Equity Theory.
2. THE Reporting_Module SHALL interpret the fsQCA configurations through the same theoretical lenses and SHALL connect each configuration recipe to a theoretical mechanism.
3. THE Reporting_Module SHALL integrate the PLS-SEM and fsQCA findings into a combined interpretation that reconciles symmetric (net-effect) and asymmetric (configurational) evidence.

### Requirement 24: PART O — Conclusion

**User Story:** As an author, I want a structured conclusion, so that the contribution and implications are clearly stated.

#### Acceptance Criteria

1. THE Reporting_Module SHALL produce a conclusion that summarizes the key findings, states which hypotheses were supported, and summarizes the fsQCA findings.
2. THE Reporting_Module SHALL state the managerial insights, the theoretical contribution, directions for future research, and the study limitations.
3. THE Reporting_Module SHALL ensure that the conclusion statements are consistent with the decision tables produced in PARTS I and J.

### Requirement 25: PART P — Supplementary Material and Appendix

**User Story:** As a reviewer, I want a supplementary appendix, so that all matrices and intermediate calculations are auditable.

#### Acceptance Criteria

1. THE Reporting_Module SHALL produce a supplementary appendix containing the full correlation matrix, covariance matrix, cross-loadings matrix, HTMT matrix, calibrated dataset, truth table, and the Run_Manifest.
2. THE Reporting_Module SHALL include the Run_Manifest in the supplementary appendix.
3. THE Reporting_Module SHALL ensure that every intermediate calculation referenced in the main tables is reproducible from the artifacts in the appendix.

### Requirement 26: Cross-Cutting — Methodological Citations and Internal Consistency

**User Story:** As a reviewer, I want consistent statistics and proper citations throughout, so that the manuscript withstands rigorous peer review.

#### Acceptance Criteria

1. THE Reporting_Module SHALL attach a methodological citation to each reported threshold, drawing from Hair et al., Henseler et al., Ragin, Fiss, Schneider & Wagemann, Nitzl et al., and Zhao et al.
2. THE Reporting_Module SHALL ensure that any statistic appearing in more than one artifact reports the same value to the same precision in every artifact.
3. IF a statistic reported in a decision table disagrees with the same statistic in its source table, THEN THE Reporting_Module SHALL halt and report the inconsistency rather than emit conflicting artifacts.
4. THE Analysis_Pipeline SHALL record, for every threshold-based decision, both the observed value and the threshold applied so that each decision is independently verifiable.
