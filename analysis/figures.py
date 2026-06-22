"""
Generate all figures/diagrams for the BSRS Results section.
Saves PNGs (300 dpi) to analysis/outputs/figures/.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
FIG = os.path.join(OUT, "figures")
os.makedirs(FIG, exist_ok=True)
DATA = os.path.join(HERE, "..", "Original collected reponses.xlsx")

BLOCKS = {
    "UE":   ["UE1", "UE2", "UE3", "UE4", "UE5"],
    "UX":   ["UX1", "UX2", "UX3", "UX4", "UX5"],
    "BSAT": ["BSAT1", "BSAT2", "BSAT3", "BSAT4"],
    "BSUC": ["BSUC1", "BSUC2", "BSUC3", "BSUC4"],
}
plt.rcParams.update({"font.family": "serif", "font.size": 11})

df = pd.read_excel(DATA)
sc = pd.DataFrame({k: df[v].mean(axis=1) for k, v in BLOCKS.items()})
paths = pd.read_csv(os.path.join(OUT, "pls_structural_paths.csv"))
loadings = pd.read_csv(os.path.join(OUT, "pls_loadings.csv"))
relval = pd.read_csv(os.path.join(OUT, "pls_reliability_validity.csv"))
r2 = pd.read_csv(os.path.join(OUT, "pls_r2.csv")).set_index("Construct")["R2"].to_dict()
nec = pd.read_csv(os.path.join(OUT, "fsqca_necessity.csv"))
tt = pd.read_csv(os.path.join(OUT, "fsqca_truth_table.csv"))
cal = pd.read_csv(os.path.join(OUT, "fsqca_calibrated.csv"))


# ----------------------------------------------------------------- Fig 1: conceptual / SEM path diagram
def fig_path_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off")
    pos = {"UE": (1.5, 6), "UX": (1.5, 2), "BSAT": (5, 4), "BSUC": (8.3, 4)}
    names = {"UE": "User\nEngagement\n(UE)", "UX": "User\nExperience\n(UX)",
             "BSAT": "Brand\nSatisfaction\n(BSAT)", "BSUC": "Brand Success /\nContinuance\n(BSUC)"}

    def box(xy, text, color):
        b = FancyBboxPatch((xy[0]-1, xy[1]-0.7), 2, 1.4,
                           boxstyle="round,pad=0.05", linewidth=1.5,
                           edgecolor="#222", facecolor=color)
        ax.add_patch(b)
        ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=10, weight="bold")

    for k in ["UE", "UX"]:
        box(pos[k], names[k], "#dbe9f6")
    box(pos["BSAT"], names["BSAT"], "#fbe7c6")
    box(pos["BSUC"], names["BSUC"], "#d6f0d8")

    pmap = {f"{r.Path}": r for _, r in paths.iterrows()}

    def arrow(a, b, hyp):
        rrow = pmap[f"{a}->{b}"]
        beta, p = rrow.Beta, rrow.p
        sig = "*" if p < 0.05 else " (n.s.)"
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ar = FancyArrowPatch((x1+1, y1), (x2-1, y2),
                             arrowstyle="-|>", mutation_scale=18,
                             linewidth=1.6, color="#444",
                             connectionstyle="arc3,rad=0.0")
        ax.add_patch(ar)
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my+0.35, f"{hyp}: β={beta:.3f}{sig}",
                ha="center", fontsize=8.5,
                color=("#0a7d28" if p < 0.05 else "#b00020"))

    arrow("UE", "BSAT", "H3a"); arrow("UX", "BSAT", "H3b")
    arrow("UE", "BSUC", "H1"); arrow("UX", "BSUC", "H2")
    arrow("BSAT", "BSUC", "H4")
    ax.text(pos["BSAT"][0], pos["BSAT"][1]-1.05, f"R²={r2.get('BSAT',0):.3f}",
            ha="center", fontsize=8.5, style="italic")
    ax.text(pos["BSUC"][0], pos["BSUC"][1]-1.05, f"R²={r2.get('BSUC',0):.3f}",
            ha="center", fontsize=8.5, style="italic")
    ax.text(5, 7.5, "Figure 1. PLS-SEM structural model with standardized path coefficients",
            ha="center", fontsize=11, weight="bold")
    ax.text(5, 0.4, "* p < 0.05 (two-tailed, 5,000 bootstrap subsamples); n.s. = not significant",
            ha="center", fontsize=8, style="italic")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig1_sem_path_diagram.png"), dpi=300, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------- Fig 2: outer loadings
def fig_loadings():
    fig, ax = plt.subplots(figsize=(9, 6))
    colors = {"UE": "#3b76af", "UX": "#5aa0d6", "BSAT": "#e8a33d", "BSUC": "#5cb85c"}
    y = 0; yticks, ylabels = [], []
    for c in ["UE", "UX", "BSAT", "BSUC"]:
        sub = loadings[loadings.Construct == c]
        for _, r in sub.iterrows():
            ax.barh(y, r.Loading, color=colors[c], edgecolor="#222", linewidth=0.5)
            ax.text(r.Loading+0.01, y, f"{r.Loading:.3f}", va="center", fontsize=8)
            yticks.append(y); ylabels.append(r.Indicator); y += 1
        y += 0.6
    ax.axvline(0.708, color="red", ls="--", lw=1.2, label="Threshold = 0.708")
    ax.set_yticks(yticks); ax.set_yticklabels(ylabels)
    ax.set_xlabel("Standardized outer loading"); ax.set_xlim(0, 1.05)
    ax.invert_yaxis(); ax.legend(loc="lower right")
    ax.set_title("Figure 2. Indicator outer loadings by construct", weight="bold")
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[c]) for c in colors]
    ax.legend(handles + [plt.Line2D([0], [0], color="red", ls="--")],
              list(colors.keys()) + ["Threshold 0.708"], loc="lower right", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig2_outer_loadings.png"), dpi=300, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------- Fig 3: reliability/validity bars
def fig_relval():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = np.arange(len(relval)); w = 0.25
    ax.bar(x-w, relval.Cronbach_alpha, w, label="Cronbach's α", color="#3b76af")
    ax.bar(x, relval.Composite_Reliability, w, label="Composite reliability (ρc)", color="#e8a33d")
    ax.bar(x+w, relval.AVE, w, label="AVE", color="#5cb85c")
    ax.axhline(0.70, color="grey", ls="--", lw=1, label="0.70 (α, CR)")
    ax.axhline(0.50, color="black", ls=":", lw=1, label="0.50 (AVE)")
    for i, r in relval.iterrows():
        ax.text(i-w, r.Cronbach_alpha+0.01, f"{r.Cronbach_alpha:.2f}", ha="center", fontsize=8)
        ax.text(i, r.Composite_Reliability+0.01, f"{r.Composite_Reliability:.2f}", ha="center", fontsize=8)
        ax.text(i+w, r.AVE+0.01, f"{r.AVE:.2f}", ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(relval.Construct)
    ax.set_ylim(0, 1.1); ax.set_ylabel("Value")
    ax.set_title("Figure 3. Construct reliability and convergent validity", weight="bold")
    ax.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig3_reliability_validity.png"), dpi=300, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------- Fig 4: LV correlation heatmap
def fig_corr_heatmap():
    corr = sc.corr()
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr))); ax.set_xticklabels(corr.columns)
    ax.set_yticks(range(len(corr))); ax.set_yticklabels(corr.index)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.values[i,j]:.3f}", ha="center", va="center",
                    color="black", fontsize=10)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Figure 4. Construct-level correlation matrix", weight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig4_correlation_heatmap.png"), dpi=300, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------- Fig 5: bootstrap path coefficients w/ CI
def fig_paths_ci():
    fig, ax = plt.subplots(figsize=(8.5, 5))
    yp = np.arange(len(paths))
    ax.errorbar(paths.Beta, yp,
                xerr=[paths.Beta - paths.CI_2_5, paths.CI_97_5 - paths.Beta],
                fmt="o", color="#3b76af", ecolor="#888", capsize=4, ms=7)
    ax.axvline(0, color="red", ls="--", lw=1)
    ax.set_yticks(yp); ax.set_yticklabels(paths.Path)
    for i, r in paths.iterrows():
        ax.text(r.CI_97_5+0.005, i, f"β={r.Beta:.3f}, p={r.p:.2f}", va="center", fontsize=8)
    ax.set_xlabel("Standardized path coefficient (95% bootstrap CI)")
    ax.set_title("Figure 5. Structural path estimates with 95% confidence intervals", weight="bold")
    ax.set_xlim(-0.35, 0.45)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig5_path_coeffs_ci.png"), dpi=300, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------- Fig 6: item distributions
def fig_distributions():
    items = [c for cols in BLOCKS.values() for c in cols]
    fig, axes = plt.subplots(3, 6, figsize=(15, 7.5))
    for ax, it in zip(axes.ravel(), items):
        ax.hist(df[it], bins=np.arange(0.5, 8.5, 1), color="#5aa0d6", edgecolor="#222")
        ax.set_title(it, fontsize=9); ax.set_xticks(range(1, 8))
        ax.tick_params(labelsize=7)
    fig.suptitle("Figure 6. Response distributions for all measurement items (1–7 Likert)",
                 weight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig6_item_distributions.png"), dpi=300, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------- Fig 7: fsQCA necessity
def fig_necessity():
    sub = nec[nec.Outcome == "BSUC"].copy()
    fig, ax = plt.subplots(figsize=(8.5, 5))
    yp = np.arange(len(sub))
    bars = ax.barh(yp, sub.Consistency, color="#e8a33d", edgecolor="#222")
    ax.axvline(0.90, color="red", ls="--", lw=1.4, label="Necessity threshold = 0.90")
    ax.set_yticks(yp); ax.set_yticklabels(sub.Condition)
    for i, v in enumerate(sub.Consistency):
        ax.text(v+0.005, i, f"{v:.3f}", va="center", fontsize=8)
    ax.set_xlim(0, 1.0); ax.set_xlabel("Consistency (necessity for high BSUC)")
    ax.set_title("Figure 7. fsQCA analysis of necessary conditions for high BSUC", weight="bold")
    ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig7_fsqca_necessity.png"), dpi=300, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------- Fig 8: truth table consistency
def fig_truthtable():
    t = tt.sort_values("Consistency")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    yp = np.arange(len(t))
    colors = ["#5cb85c" if c >= 0.80 else "#c0504d" for c in t.Consistency]
    ax.barh(yp, t.Consistency, color=colors, edgecolor="#222")
    ax.axvline(0.80, color="red", ls="--", lw=1.4, label="Sufficiency threshold = 0.80")
    ax.set_yticks(yp); ax.set_yticklabels(t.Configuration, fontsize=8)
    for i, (v, n) in enumerate(zip(t.Consistency, t.Cases_gt_0_5)):
        ax.text(v+0.005, i, f"{v:.3f} (n={n})", va="center", fontsize=7.5)
    ax.set_xlim(0, 1.0); ax.set_xlabel("Raw consistency with high BSUC")
    ax.set_title("Figure 8. Truth-table configurations and consistency", weight="bold")
    ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig8_fsqca_truthtable.png"), dpi=300, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------- Fig 9: calibration example
def fig_calibration():
    fig, ax = plt.subplots(figsize=(8, 5))
    x = sc["BSUC"].values; y = cal["BSUC"].values
    order = np.argsort(x)
    ax.scatter(x, y, s=14, color="#3b76af", alpha=0.5)
    ax.plot(x[order], y[order], color="#b00020", lw=1.5)
    ax.axhline(0.5, color="grey", ls=":", lw=1)
    ax.set_xlabel("Raw BSUC score (1–7)"); ax.set_ylabel("Calibrated fuzzy membership (0–1)")
    ax.set_title("Figure 9. Direct-method calibration of BSUC (illustrative)", weight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig9_calibration_bsuc.png"), dpi=300, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------- Fig 10: analysis workflow flowchart
def fig_flowchart():
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")

    def fbox(x, y, w, h, text, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04",
                    edgecolor="#222", facecolor=color, linewidth=1.4))
        ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=8.5)

    def arr(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                    mutation_scale=16, lw=1.4, color="#444"))

    fbox(0.3, 3, 2.1, 1.2, "Survey data\nN = 312\n(7-point Likert)", "#dbe9f6")
    arr(2.4, 3.6, 3.0, 3.6)
    fbox(3.0, 3, 2.2, 1.2, "Data screening\n(no missing,\nattention checks)", "#dbe9f6")
    # split into two methods
    arr(5.2, 4.0, 5.9, 5.3); arr(5.2, 3.2, 5.9, 1.7)
    fbox(5.9, 4.9, 2.6, 1.4, "PLS-SEM\nMeasurement model:\nloadings, CR, AVE, HTMT", "#fbe7c6")
    arr(8.5, 5.6, 9.2, 5.6)
    fbox(9.2, 4.9, 2.5, 1.4, "Structural model:\npaths, R², f², Q²,\n5,000 bootstraps", "#fbe7c6")
    fbox(5.9, 0.9, 2.6, 1.4, "fsQCA\nCalibration\n(p95 / p50 / p5)", "#d6f0d8")
    arr(8.5, 1.6, 9.2, 1.6)
    fbox(9.2, 0.9, 2.5, 1.4, "Necessity +\ntruth table +\nsufficiency", "#d6f0d8")
    ax.text(6, 6.7, "Figure 10. Two-stage symmetric (PLS-SEM) and asymmetric (fsQCA) analytical workflow",
            ha="center", fontsize=11, weight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig10_workflow_flowchart.png"), dpi=300, bbox_inches="tight")
    plt.close()


for f in [fig_path_diagram, fig_loadings, fig_relval, fig_corr_heatmap,
          fig_paths_ci, fig_distributions, fig_necessity, fig_truthtable,
          fig_calibration, fig_flowchart]:
    f()
    print("done:", f.__name__)

print("\nFigures written to", FIG)
print(sorted(os.listdir(FIG)))
