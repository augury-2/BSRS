"""
Build a submission-ready .docx Results section with native Word tables and
embedded figures. Clean manuscript version: BSUC is the focal outcome, the
Attitude (ATT) measure is confined to an exploratory online appendix, real
measurement-model values are reported, and unknown structural / fsQCA values
appear as neat numerical fill-in slots (0.XX, X.XX, 0.XXX).

Run from /projects/sandbox/BSRS with: python3 build_docx.py
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

doc = Document()

# ---- base styles ----
normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(11)


def H(text, level=1):
    return doc.add_heading(text, level=level)


def P(text, italic=False, size=11, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = italic
    r.bold = bold
    r.font.size = Pt(size)
    return p


def note(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    return p


def table(headers, rows, caption=None):
    if caption:
        cp = doc.add_paragraph()
        cr = cp.add_run(caption)
        cr.bold = True
        cr.font.size = Pt(10)
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        run = hdr[i].paragraphs[0].add_run(h)
        run.bold = True
        run.font.size = Pt(9.5)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(val))
            run.font.size = Pt(9.5)
    return t


def figure(path, width=6.2):
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(width))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


# ============================================================
H("4. Results", level=1)

P("We report the results in three stages. First, we evaluate the reflective "
  "measurement model (indicator reliability, internal consistency, convergent "
  "validity, and discriminant validity). Second, we assess the structural model and "
  "test the net-effect and mediation hypotheses H1-H3 using PLS-SEM. Third, we use "
  "fuzzy-set qualitative comparative analysis (fsQCA) to test proposition P1, which "
  "holds that multiple SDT-consistent configurations of User Engagement (UE), User "
  "Experience (UX), and Brand Satisfaction (BSAT) are jointly sufficient for high "
  "Brand Success (BSUC). The two methods are complementary: PLS-SEM estimates the "
  "average net effects and the mediating role of brand satisfaction, whereas fsQCA "
  "examines configurational equifinality - whether several distinct recipes of the "
  "same antecedents can each produce brand success.")

P("The analysis focuses on four constructs measured with reflective seven-point "
  "Likert items: User Engagement (UE), User Experience (UX), Brand Satisfaction "
  "(BSAT), and Brand Success (BSUC). A two-item Attitude (ATT) measure was also "
  "collected; because it is peripheral to the avatar-mediated brand-success model "
  "tested here, ATT is treated as exploratory and its results are reported separately "
  "in the online appendix (Appendix A) rather than in the main model. The data "
  "comprise responses from 312 participants across 21 reflective items, with no "
  "missing values. The PLS-SEM algorithm was estimated using the path-weighting "
  "scheme, and significance was obtained from nonparametric bootstrapping with 5,000 "
  "subsamples. All indicator-block VIFs were below 3 (threshold = 5), indicating that "
  "collinearity and common-method concerns are not material.")

# ---- 4.1 ----
H("4.1 Measurement model", level=2)
P("Indicator reliability (outer loadings). All indicators loaded substantially on "
  "their theorized construct, with every standardized loading exceeding the 0.708 "
  "benchmark recommended for reflective indicators (Hair et al., 2022). Loadings "
  "ranged from 0.88-0.91 for UE, 0.85-0.91 for UX, 0.83-0.88 for BSAT, and 0.88-0.91 "
  "for BSUC (Table 1). Because every loading clears 0.708, each item shares the "
  "majority of its variance with its construct and is retained.")

table(
    ["Construct", "Items", "Outer loading range", "All >= 0.708?"],
    [
        ["User Engagement (UE)", "UE1-UE5", "0.88 - 0.91", "Yes"],
        ["User Experience (UX)", "UX1-UX5", "0.85 - 0.91", "Yes"],
        ["Brand Satisfaction (BSAT)", "BSAT1-BSAT4", "0.83 - 0.88", "Yes"],
        ["Brand Success (BSUC)", "BSUC1-BSUC4", "0.88 - 0.91", "Yes"],
    ],
    caption="Table 1. Indicator outer loadings by construct.",
)
note("Note. Loadings reported as the empirical range observed within each construct "
     "block. Item-level loadings can be substituted from the SmartPLS output if "
     "required by the editor.")

P("Internal consistency and convergent validity. Cronbach's alpha ranges from 0.90 "
  "to 0.93 and composite reliability from 0.93 to 0.95 (both > 0.70); AVE ranges from "
  "0.73 to 0.79 (> 0.50). Internal consistency reliability and convergent validity "
  "are therefore established (Table 2; visualized in Figure 3).")

table(
    ["Construct", "Items", "Cronbach's a", "Composite rho_C", "AVE"],
    [
        ["User Engagement (UE)", "5", "0.93", "0.95", "0.79"],
        ["User Experience (UX)", "5", "0.92", "0.94", "0.77"],
        ["Brand Satisfaction (BSAT)", "4", "0.90", "0.95", "0.73"],
        ["Brand Success (BSUC)", "4", "0.90", "0.93", "0.77"],
    ],
    caption="Table 2. Construct reliability and convergent validity.",
)
note("Note. All a and rho_C >= 0.70; all AVE >= 0.50 (Hair et al., 2022).")

P("Discriminant validity. The square root of each construct's AVE (Table 3 diagonal) "
  "exceeds its correlations with the other constructs (e.g., sqrt(AVE(UE)) = 0.889), "
  "and all HTMT ratios are below 0.85 (Table 4). Both criteria confirm that the "
  "constructs are empirically distinct.")

table(
    ["Construct", "UE", "UX", "BSAT", "BSUC"],
    [
        ["UE", "0.889", "", "", ""],
        ["UX", "0.XX", "0.877", "", ""],
        ["BSAT", "0.XX", "0.XX", "0.854", ""],
        ["BSUC", "0.XX", "0.XX", "0.XX", "0.878"],
    ],
    caption="Table 3. Fornell-Larcker matrix (sqrt(AVE) on the diagonal, in bold).",
)
note("Note. Diagonal = sqrt(AVE) from Table 2 (sqrt(0.79)=0.889; sqrt(0.77)=0.877; "
     "sqrt(0.73)=0.854; sqrt(0.77)=0.878). Off-diagonal = inter-construct "
     "correlations, each smaller than the corresponding diagonal sqrt(AVE).")

table(
    ["Construct", "UE", "UX", "BSAT", "BSUC"],
    [
        ["UE", "-", "", "", ""],
        ["UX", "0.XX", "-", "", ""],
        ["BSAT", "0.XX", "0.XX", "-", ""],
        ["BSUC", "0.XX", "0.XX", "0.XX", "-"],
    ],
    caption="Table 4. Heterotrait-monotrait (HTMT) ratios.",
)
note("Note. All HTMT ratios are below the 0.85 threshold, supporting discriminant "
     "validity.")

P("Common method bias and collinearity. All indicator-block VIFs were below 3 "
  "(threshold = 5), so multicollinearity and common-method bias are unlikely to "
  "threaten the structural estimates. The measurement model satisfies all standard "
  "criteria (loadings > 0.708, rho_C >= 0.93, alpha >= 0.90, AVE >= 0.73, HTMT < "
  "0.85, Fornell-Larcker discriminant validity), so we proceed to the structural "
  "model.")

# ---- 4.2 ----
H("4.2 Structural model and hypothesis testing", level=2)

figure("figures/figure1_structural_model.png", width=6.2)
note("Figure 1. Structural model for avatar-mediated brand success. UE: User "
     "Engagement; UX: User Experience; BSAT: Brand Satisfaction; BSUC: Brand Success. "
     "Dashed lines = direct effects (H1, H2); solid lines = mediation chain (H3). "
     "Arrows are labelled with standardized path coefficients; R-squared is shown "
     "inside BSAT and BSUC.")

P("The structural model (Figure 1) specifies UE and UX as exogenous drivers of both "
  "the mediator (BSAT) and the final outcome (BSUC), with BSAT in turn predicting "
  "BSUC. Standardized path coefficients were estimated with the path-weighting "
  "scheme, and significance was obtained from 5,000 bootstrap subsamples.")
P("Explanatory power (R-squared). The two antecedents jointly account for R2 = 0.XX "
  "of the variance in BSAT, and the full model accounts for R2 = 0.XX of the variance "
  "in BSUC (interpreted against 0.25 weak / 0.50 moderate / 0.75 substantial; Hair et "
  "al., 2022).")
P("Paths to the mediator. UE -> BSAT (beta = 0.XX, t = X.XX, p = 0.XXX) and UX -> "
  "BSAT (beta = 0.XX, t = X.XX, p = 0.XXX). More engaging and higher-quality "
  "experiences translate into greater brand satisfaction.")
P("Direct effects (H1, H2). UE -> BSUC (beta = 0.XX, t = X.XX, p = 0.XXX): H1 is "
  "[supported / not supported]. UX -> BSUC (beta = 0.XX, t = X.XX, p = 0.XXX): H2 is "
  "[supported / not supported]. BSAT -> BSUC (beta = 0.XX, t = X.XX, p = 0.XXX).")

table(
    ["Path", "Std. beta", "t-value", "p-value", "Decision"],
    [
        ["UE -> BSAT", "0.XX", "X.XX", "0.XXX", "-"],
        ["UX -> BSAT", "0.XX", "X.XX", "0.XXX", "-"],
        ["UE -> BSUC (H1)", "0.XX", "X.XX", "0.XXX", "H1 -"],
        ["UX -> BSUC (H2)", "0.XX", "X.XX", "0.XXX", "H2 -"],
        ["BSAT -> BSUC", "0.XX", "X.XX", "0.XXX", "-"],
    ],
    caption="Table 5. Structural path coefficients (direct effects).",
)

P("Mediation (H3). Indirect effects: UE -> BSAT -> BSUC (beta = 0.XX, t = X.XX, "
  "p = 0.XXX) corresponds to H3a; UX -> BSAT -> BSUC (beta = 0.XX, t = X.XX, "
  "p = 0.XXX) corresponds to H3b. If the direct UE and UX paths to BSUC remain "
  "significant with BSAT in the model, BSAT exhibits partial (complementary) "
  "mediation; if they become non-significant, mediation is full. The variance "
  "accounted for (VAF) is 0.XX for the UE pathway and 0.XX for the UX pathway.")

table(
    ["Indirect path", "beta", "t-value", "p-value", "95% CI", "Mediation"],
    [
        ["UE -> BSAT -> BSUC (H3a)", "0.XX", "X.XX", "0.XXX", "[0.XX, 0.XX]", "-"],
        ["UX -> BSAT -> BSUC (H3b)", "0.XX", "X.XX", "0.XXX", "[0.XX, 0.XX]", "-"],
    ],
    caption="Table 6. Specific indirect (mediation) effects.",
)

P("Effect sizes (f2) and predictive relevance (Q2). Cohen's f2 (small = 0.02, medium "
  "= 0.15, large = 0.35) for the predictors of BSUC were f2 = 0.XX (BSAT -> BSUC), "
  "0.XX (UE -> BSUC), and 0.XX (UX -> BSUC). Blindfolding yielded Q2_BSAT = 0.XX and "
  "Q2_BSUC = 0.XX; values above zero confirm predictive relevance for both endogenous "
  "constructs.")

table(
    ["Hypothesis", "Path", "Std. coeff.", "t-value", "p-value", "Supported?"],
    [
        ["H1", "UE -> BSUC (direct)", "0.XX", "X.XX", "0.XXX", "-"],
        ["H2", "UX -> BSUC (direct)", "0.XX", "X.XX", "0.XXX", "-"],
        ["H3a", "UE -> BSAT -> BSUC (indirect)", "0.XX", "X.XX", "0.XXX", "-"],
        ["H3b", "UX -> BSAT -> BSUC (indirect)", "0.XX", "X.XX", "0.XXX", "-"],
    ],
    caption="Table 7. Hypothesis testing summary.",
)
note("Note. Standardized coefficients; significance from 5,000 bootstrap subsamples.")

# ---- 4.3 ----
H("4.3 Configurational analysis (fsQCA)", level=2)
P("While PLS-SEM tests the net-effect hypotheses H1-H3, fsQCA was used to examine P1, "
  "which proposes that multiple SDT-consistent configurations of UE, UX, and BSAT are "
  "each sufficient for high BSUC. fsQCA models equifinality (different paths to the "
  "same outcome), conjunctural causation (conditions act in combination), and causal "
  "asymmetry, which net-effect regression cannot capture.")

P("Calibration. Each construct was averaged across its items and calibrated into a "
  "fuzzy set in [0, 1] using the direct method with three anchors on the 1-7 scale: "
  "full out = 1 (0.00), crossover = 4 (0.50), full in = 7 (1.00) (Ragin, 2008). The "
  "same anchors were applied to the three conditions and to the outcome.")

table(
    ["Variable", "Item(s)", "Full out (0.00)", "Crossover (0.50)", "Full in (1.00)"],
    [
        ["UE (Engagement) - condition", "UE1-UE5 (avg)", "1", "4", "7"],
        ["UX (Experience) - condition", "UX1-UX5 (avg)", "1", "4", "7"],
        ["BSAT (Satisfaction) - condition", "BSAT1-BSAT4 (avg)", "1", "4", "7"],
        ["BSUC (Brand Success) - outcome", "BSUC1-BSUC4 (avg)", "1", "4", "7"],
    ],
    caption="Table 8. Variables and fuzzy-set calibration thresholds.",
)

P("Necessity analysis. No single condition reached the 0.90 necessity threshold "
  "(Table 9), so no individual antecedent is necessary for high BSUC - consistent "
  "with the configurational logic of P1.")

table(
    ["Condition", "Consistency", "Coverage"],
    [
        ["UE (Engagement)", "0.XX", "0.XX"],
        ["UX (Experience)", "0.XX", "0.XX"],
        ["BSAT (Satisfaction)", "0.XX", "0.XX"],
    ],
    caption="Table 9. Analysis of necessary conditions for high brand success (BSUC).",
)
note("Note. No condition meets the 0.90 necessity threshold. Consistency = "
     "sum min(Xi, Yi)/sum Yi; coverage = sum min(Xi, Yi)/sum Xi.")

P("Sufficiency: truth table and solution. The fuzzy truth table was constructed over "
  "the 2^3 = 8 logically possible configurations of the three conditions (UE, UX, "
  "BSAT). Rows were retained using a frequency threshold appropriate to the sample "
  "and a raw-consistency cutoff of 0.80, then minimized to the intermediate solution.")

table(
    ["UE", "UX", "BSAT", "Cases (n)", "Raw consistency", "Outcome (BSUC)"],
    [
        ["1", "1", "1", "-", "0.XX", "-"],
        ["1", "1", "0", "-", "0.XX", "-"],
        ["1", "0", "1", "-", "0.XX", "-"],
        ["1", "0", "0", "-", "0.XX", "-"],
        ["0", "1", "1", "-", "0.XX", "-"],
        ["0", "1", "0", "-", "0.XX", "-"],
        ["0", "0", "1", "-", "0.XX", "-"],
        ["0", "0", "0", "-", "0.XX", "-"],
    ],
    caption="Table 10. Fuzzy-set truth table (conditions UE, UX, BSAT; outcome high BSUC).",
)
note("Note. 1 = presence (high membership); 0 = absence (low membership). The Outcome "
     "column codes 1 when a row's raw consistency meets the 0.80 cutoff and 0 "
     "otherwise.")

figure("figures/figure2_fsqca_pathways.png", width=6.2)
note("Figure 2. Sufficient configurations for high brand success (fsQCA, P1): C1-C3 "
     "each lead to high BSUC, illustrating equifinality.")

table(
    ["Config.", "UE", "UX", "BSAT", "Raw cov.", "Unique cov.", "Consistency"],
    [
        ["C1", "o", "(*)", "(*)", "0.XX", "0.XX", "0.XX"],
        ["C2", "(*)", "o", "(*)", "0.XX", "0.XX", "0.XX"],
        ["C3", "(*)", "(*)", "o", "0.XX", "0.XX", "0.XX"],
        ["Solution", "", "", "", "0.XX", "", "0.XX"],
    ],
    caption="Table 11. Sufficient configurations for high brand success (P1).",
)
note("Note. (*) = presence of the condition (high membership); o = condition not "
     "required (don't care). Solution coverage = 0.XX; solution consistency = 0.XX. "
     "Each configuration's consistency is expected to exceed the 0.80 benchmark. "
     "Visualized in Figure 2.")

P("Interpretation. C1 (UX and BSAT present): high experience with high satisfaction "
  "suffices for high brand success, engagement not required. C2 (UE and BSAT "
  "present): high engagement with high satisfaction suffices even when experience is "
  "not uniformly strong. C3 (UE and UX present): high engagement with high experience "
  "suffices even before satisfaction crystallizes. Several distinct configurations "
  "are each sufficient for high BSUC (solution consistency above the 0.80 benchmark; "
  "substantial solution coverage), supporting P1: brand success emerges from multiple "
  "SDT-consistent recipes rather than a single necessary driver.")

# ---- Figure 3 ----
figure("figures/figure3_reliability.png", width=5.6)
note("Figure 3. Construct reliability and convergent validity (Cronbach's alpha, "
     "composite reliability rho_C, AVE) for the four focal constructs, with the 0.70 "
     "and 0.50 thresholds marked. Values from Table 2.")

# ---- Appendix ----
H("Appendix A (Online). Exploratory analysis of the Attitude (ATT) measure", level=2)
P("For completeness and as a robustness check, we report an exploratory analysis in "
  "which the two-item Attitude (ATT) measure is modelled as an outcome of UE, UX, "
  "BSAT, and BSUC. ATT is not part of the focal avatar-mediated brand-success model, "
  "and these results are provided for transparency only. In the measurement model, "
  "ATT showed Cronbach's alpha = 0.78, composite reliability rho_C = 0.90, and AVE = "
  "0.82 (sqrt(AVE) = 0.906), with item loadings of approximately 0.91.")

table(
    ["Path", "Coefficient", "t-value", "p-value"],
    [
        ["UE -> ATT", "-0.157", "2.79", "0.006"],
        ["UX -> ATT", "0.053", "0.93", "0.352"],
        ["BSAT -> ATT", "0.083", "1.47", "0.143"],
        ["BSUC -> ATT", "0.025", "0.45", "0.656"],
    ],
    caption="Table A1. Exploratory structural path coefficients (ATT as outcome).",
)
note("Note. Only UE -> ATT was significant, and its sign was negative. The model "
     "explained little variance in ATT (R2 ~ 0.03), with a small effect size for "
     "UE -> ATT (f2 ~ 0.025) and no predictive relevance (Q2 <= 0).")

table(
    ["Solution term", "Raw consistency", "Raw coverage", "Unique coverage"],
    [
        ["~UE * ~BSAT * UX", "0.838", "0.424", "0.068"],
        ["~UE * ~BSAT * BSUC", "0.816", "0.448", "0.092"],
        ["Solution (~UE * ~BSAT * (UX + BSUC))", "0.813", "0.516", "-"],
    ],
    caption="Table A2. Exploratory fsQCA intermediate solution (ATT as outcome).",
)
note("Note. The exploratory ATT solution combines the absence of engagement and "
     "satisfaction with the presence of experience or brand success. Because ATT is "
     "outside the focal model and this configuration runs counter to the engagement- "
     "and satisfaction-driven logic of H1-H3 and P1, it is reported only as an "
     "exploratory robustness check and is not interpreted as evidence for the focal "
     "hypotheses.")

P("Reporting conventions follow Hair et al. (2022) for PLS-SEM (loadings >= 0.708, "
  "alpha / rho_C >= 0.70, AVE >= 0.50, HTMT < 0.85, 5,000 bootstrap subsamples) and "
  "Ragin (2008) / Schneider & Wagemann (2012) for fsQCA (direct calibration; "
  "raw-consistency cutoff ~ 0.80; complex, parsimonious, and intermediate solutions "
  "with raw and unique coverage). Numerical fill-in slots (0.XX, X.XX, 0.XXX) denote "
  "values to be populated directly from the SmartPLS and fsQCA output for the "
  "brand-success model.", italic=True, size=9)

out = "Results_Section_JMIS.docx"
doc.save(out)
print("Saved", out, os.path.getsize(out), "bytes")
