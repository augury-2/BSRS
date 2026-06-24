"""
05_figures.py
Generate all publication-quality figures (300 dpi PNG) for the Results section.
Reads the CSV/JSON artifacts produced by scripts 01-04.
"""
import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch
import matplotlib.cm as cm

import fsqca_engine as fz

OUT = "analysis/outputs"
FIG = "analysis/figures"
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({
    "figure.dpi": 300, "savefig.dpi": 300, "font.size": 11,
    "font.family": "DejaVu Sans", "axes.grid": True, "grid.alpha": 0.25,
    "axes.spines.top": False, "axes.spines.right": False,
})
BLUE, GREEN, RED, GREY = "#2C6FBB", "#2E8B57", "#C0392B", "#7F8C8D"

df = pd.read_excel("Responses.xlsx", sheet_name="responses collected")
df.columns = [c.strip() for c in df.columns]
BLOCKS = {
    "UE": ["UE1","UE2","UE3","UE4","UE5"], "UX": ["UX1","UX2","UX3","UX4","UX5"],
    "BSAT": ["BSAT1","BSAT2","BSAT3","BSAT4"], "BSUC": ["BSUC1","BSUC2","BSUC3","BSUC4"],
}

paths = pd.read_csv(f"{OUT}/T10_path_coefficients.csv")
r2 = pd.read_csv(f"{OUT}/T8_r2.csv", index_col=0)
struct = json.load(open(f"{OUT}/structural_summary.json"))
q2 = struct["Q2"]
htmt = pd.read_csv(f"{OUT}/T5_htmt.csv", index_col=0)
fl = pd.read_csv(f"{OUT}/T4_fornell_larcker.csv", index_col=0)
f2 = pd.read_csv(f"{OUT}/T9_f2.csv")
load = pd.read_csv(f"{OUT}/T2_outer_loadings.csv")
cal = pd.read_csv(f"{OUT}/calibrated_data.csv")
tt = pd.read_csv(f"{OUT}/T16_truth_table.csv")
nec = pd.read_csv(f"{OUT}/T15_necessity_high.csv")

def pstars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s."

# =====================================================================
# FIG 1: Structural model path diagram
# =====================================================================
def fig_structural():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.axis("off")
    pos = {"UE": (0.5, 4.2), "UX": (0.5, 1.3), "BSAT": (5, 2.75), "BSUC": (9.2, 2.75)}
    names = {"UE": "User\nEngagement\n(UE)", "UX": "User\nExperience\n(UX)",
             "BSAT": "Brand-System\nSatisfaction\n(BSAT)",
             "BSUC": "Brand-System\nContinuance\n(BSUC)"}
    r2map = {"BSAT": r2.loc["BSAT", "R2"], "BSUC": r2.loc["BSUC", "R2"]}
    box_w, box_h = 1.7, 1.15
    for k, (x, y) in pos.items():
        col = "#EAF1FB" if k in ("UE", "UX") else "#E8F6EF"
        fb = FancyBboxPatch((x - box_w/2, y - box_h/2), box_w, box_h,
                            boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc=col, ec=BLUE if k in ("UE","UX") else GREEN, lw=2)
        ax.add_patch(fb)
        label = names[k]
        if k in r2map:
            label += f"\nR² = {r2map[k]:.3f}"
        ax.text(x, y, label, ha="center", va="center", fontsize=10, weight="bold")

    def arrow(a, b, beta, p, off=0.0, color=None):
        x1, y1 = pos[a]; x2, y2 = pos[b]
        # trim to box edges
        dx, dy = x2 - x1, y2 - y1
        d = np.hypot(dx, dy)
        ux, uy = dx/d, dy/d
        sx, sy = x1 + ux*box_w/2*0.95, y1 + uy*box_h/2 + off
        ex, ey = x2 - ux*box_w/2*0.95, y2 - uy*box_h/2 + off
        sig = p < 0.05
        c = color or (BLUE if sig else GREY)
        ar = FancyArrowPatch((sx, sy), (ex, ey), arrowstyle="-|>",
                             mutation_scale=18, lw=2.4 if sig else 1.4,
                             color=c, ls="-" if sig else "--")
        ax.add_patch(ar)
        mx, my = (sx+ex)/2, (sy+ey)/2
        ax.text(mx, my+0.22, f"β={beta:.3f}{pstars(p)}", ha="center",
                fontsize=9.5, color=c, weight="bold",
                bbox=dict(fc="white", ec="none", alpha=0.8, pad=0.5))

    pr = {(r["Path"]): (r["Beta"], r["p"]) for _, r in paths.iterrows()}
    arrow("UE", "BSAT", *pr["UE -> BSAT"])
    arrow("UX", "BSAT", *pr["UX -> BSAT"])
    arrow("BSAT", "BSUC", *pr["BSAT -> BSUC"])
    arrow("UE", "BSUC", *pr["UE -> BSUC"], off=0.55)
    arrow("UX", "BSUC", *pr["UX -> BSUC"], off=-0.55)

    ax.set_xlim(-0.6, 10.4); ax.set_ylim(0, 5.4)
    ax.set_title("Figure 1. PLS-SEM structural model with standardized path "
                 "coefficients\n(solid = significant at p<.05; dashed = n.s.; "
                 "*p<.05, **p<.01, ***p<.001)", fontsize=11.5, weight="bold")
    leg = [Patch(fc="#EAF1FB", ec=BLUE, label="Exogenous antecedent"),
           Patch(fc="#E8F6EF", ec=GREEN, label="Endogenous construct")]
    ax.legend(handles=leg, loc="lower center", ncol=2, frameon=False,
              bbox_to_anchor=(0.5, -0.02))
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig1_structural_model.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 2: Path coefficients with bootstrap 95% CIs
# =====================================================================
def fig_paths_ci():
    d = paths.copy().sort_values("Beta")
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    y = np.arange(len(d))
    colors = [BLUE if p < 0.05 else GREY for p in d["p"]]
    err_low = d["Beta"] - d["CI_2.5%"]
    err_high = d["CI_97.5%"] - d["Beta"]
    ax.errorbar(d["Beta"], y, xerr=[err_low, err_high], fmt="o", ms=8,
                ecolor=GREY, elinewidth=2, capsize=5,
                mfc="white", mec="k", zorder=3)
    for yi, (_, row), c in zip(y, d.iterrows(), colors):
        ax.scatter(row["Beta"], yi, s=80, color=c, zorder=4)
        ax.text(row["CI_97.5%"]+0.01, yi,
                f"β={row['Beta']:.3f} {pstars(row['p'])}", va="center", fontsize=9)
    ax.axvline(0, color=RED, ls="--", lw=1)
    ax.set_yticks(y); ax.set_yticklabels(d["Path"])
    ax.set_xlabel("Standardized path coefficient (β) with 95% bootstrap CI")
    ax.set_title("Figure 2. Structural path estimates and bootstrap confidence "
                 "intervals\n(5,000 resamples)", weight="bold")
    ax.set_xlim(-0.15, 0.75)
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig2_path_CIs.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 3: R2 and Q2 bar chart
# =====================================================================
def fig_r2q2():
    cons = ["BSAT", "BSUC"]
    r2v = [r2.loc[c, "R2"] for c in cons]
    q2v = [q2[c] for c in cons]
    x = np.arange(len(cons)); w = 0.36
    fig, ax = plt.subplots(figsize=(7, 4.8))
    b1 = ax.bar(x - w/2, r2v, w, label="R² (in-sample)", color=BLUE)
    b2 = ax.bar(x + w/2, q2v, w, label="Q² (predictive relevance)", color=GREEN)
    for b in list(b1)+list(b2):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.005,
                f"{b.get_height():.3f}", ha="center", fontsize=9, weight="bold")
    ax.axhline(0.25, color=GREY, ls=":", lw=1)
    ax.text(1.45, 0.255, "R²≈.25 (weak/moderate)", fontsize=8, color=GREY)
    ax.set_xticks(x); ax.set_xticklabels(cons)
    ax.set_ylabel("Variance explained / predictive relevance")
    ax.set_ylim(0, 0.45); ax.legend(frameon=False)
    ax.set_title("Figure 3. Explanatory (R²) and predictive (Q²) power of "
                 "endogenous constructs", weight="bold")
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig3_R2_Q2.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 4: f2 effect sizes
# =====================================================================
def fig_f2():
    d = f2.copy()
    d["label"] = d["from"] + " -> " + d["to"]
    d = d.sort_values("f2")
    fig, ax = plt.subplots(figsize=(8, 4.6))
    colors = []
    for v in d["f2"]:
        colors.append(RED if v < 0.02 else ("#E59866" if v < 0.15
                      else (GREEN if v < 0.35 else BLUE)))
    bars = ax.barh(d["label"], d["f2"], color=colors)
    for b, v in zip(bars, d["f2"]):
        ax.text(v+0.003, b.get_y()+b.get_height()/2, f"{v:.3f}",
                va="center", fontsize=9)
    for thr, lab in [(0.02, "small"), (0.15, "medium"), (0.35, "large")]:
        ax.axvline(thr, color=GREY, ls=":", lw=1)
        ax.text(thr, len(d)-0.4, lab, rotation=90, fontsize=8, color=GREY, va="top")
    ax.set_xlabel("Cohen's f² effect size")
    ax.set_title("Figure 4. f² effect sizes for structural paths", weight="bold")
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig4_f2.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 5: HTMT heatmap
# =====================================================================
def _heat(ax, M, title, fmt="{:.3f}", vmax=1.0, cmap="Blues", mask_diag=False):
    data = M.values.astype(float)
    im = ax.imshow(data, cmap=cmap, vmin=0, vmax=vmax)
    ax.set_xticks(range(len(M.columns))); ax.set_xticklabels(M.columns)
    ax.set_yticks(range(len(M.index))); ax.set_yticklabels(M.index)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if mask_diag and i == j:
                continue
            val = data[i, j]
            ax.text(j, i, fmt.format(val), ha="center", va="center",
                    fontsize=9, color="white" if val > vmax*0.6 else "black")
    ax.set_title(title, weight="bold")
    return im

def fig_htmt():
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = _heat(ax, htmt, "Figure 5. Heterotrait-monotrait ratios (HTMT)",
               vmax=0.85, cmap="Blues")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="HTMT (threshold 0.85)")
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig5_HTMT.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 6: Fornell-Larcker / construct correlation heatmap
# =====================================================================
def fig_fl():
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = _heat(ax, fl, "Figure 6. Fornell-Larcker matrix\n(diagonal = sqrt(AVE), "
               "off-diagonal = construct correlations)", vmax=1.0, cmap="Greens")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig6_FornellLarcker.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 7: Outer loadings by construct
# =====================================================================
def fig_loadings():
    fig, ax = plt.subplots(figsize=(9, 5))
    cmap = {"UE": BLUE, "UX": GREEN, "BSAT": "#8E44AD", "BSUC": "#E67E22"}
    colors = [cmap[c] for c in load["Construct"]]
    bars = ax.bar(load["Item"], load["Loading"], color=colors)
    for b, v in zip(bars, load["Loading"]):
        ax.text(b.get_x()+b.get_width()/2, v+0.005, f"{v:.2f}", ha="center",
                fontsize=8, rotation=0)
    ax.axhline(0.708, color=RED, ls="--", lw=1.2, label="Threshold 0.708")
    ax.set_ylim(0, 1.0); ax.set_ylabel("Standardized outer loading")
    ax.set_title("Figure 7. Indicator outer loadings by construct", weight="bold")
    ax.tick_params(axis="x", rotation=90)
    handles = [Patch(color=v, label=k) for k, v in cmap.items()]
    handles.append(plt.Line2D([0],[0], color=RED, ls="--", label="0.708 threshold"))
    ax.legend(handles=handles, ncol=5, frameon=False, fontsize=8, loc="lower center",
              bbox_to_anchor=(0.5, -0.42))
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig7_outer_loadings.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 8: IPMA
# =====================================================================
def fig_ipma():
    ipma = pd.read_csv(f"{OUT}/T12_ipma.csv")
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.scatter(ipma["Importance_total_effect"], ipma["Performance_0_100"],
               s=160, color=BLUE, zorder=3)
    for _, r in ipma.iterrows():
        ax.annotate(r["Construct"],
                    (r["Importance_total_effect"], r["Performance_0_100"]),
                    textcoords="offset points", xytext=(10, 6), fontsize=11,
                    weight="bold")
    ax.axhline(ipma["Performance_0_100"].mean(), color=GREY, ls="--", lw=1)
    ax.axvline(ipma["Importance_total_effect"].mean(), color=GREY, ls="--", lw=1)
    ax.set_xlabel("Importance (total effect on BSUC)")
    ax.set_ylabel("Performance (0-100 index)")
    ax.set_title("Figure 8. Importance-Performance Map Analysis (target: BSUC)",
                 weight="bold")
    ax.set_ylim(0, 100)
    ax.text(0.02, 0.04, "Note: performance is uniform (~50) because every "
            "construct mean ≈ scale midpoint.", transform=ax.transAxes,
            fontsize=8, color=GREY, style="italic")
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig8_IPMA.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 9: fsQCA calibration (raw histogram + calibrated overlay)
# =====================================================================
def fig_calibration():
    comp = pd.DataFrame({c: df[items].mean(axis=1) for c, items in BLOCKS.items()})
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))
    for ax, c in zip(axes.ravel(), ["UE", "UX", "BSAT", "BSUC"]):
        ax.hist(comp[c], bins=14, color="#BFD7EA", ec="white", alpha=0.9)
        ax.set_xlabel(f"{c} (raw composite, 1-7)")
        ax.set_ylabel("Frequency", color="#5D6D7E")
        ax2 = ax.twinx()
        order = np.argsort(comp[c].values)
        ax2.plot(comp[c].values[order], cal[c].values[order], color=RED, lw=2)
        ax2.set_ylabel("Calibrated membership", color=RED)
        ax2.set_ylim(0, 1); ax2.axhline(0.5, color=GREY, ls=":", lw=1)
        ax2.grid(False)
        ax.set_title(f"{c}", weight="bold")
    fig.suptitle("Figure 9. fsQCA calibration: raw composite distributions and "
                 "fuzzy-set membership functions", weight="bold", y=1.0)
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig9_calibration.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 10: fsQCA XY plot for sufficient configuration
# =====================================================================
def fig_xy_sufficiency():
    CONDS = ["UE", "UX", "BSAT"]
    memb = fz.config_membership((1, 1, 1), cal, CONDS)
    Y = cal["BSUC"].values
    cons = fz.consistency_suff(memb, Y)
    cov = fz.coverage_suff(memb, Y)
    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    ax.scatter(memb, Y, s=28, alpha=0.5, color=BLUE, ec="white")
    ax.plot([0, 1], [0, 1], color=RED, lw=1.5, ls="--", label="Diagonal (X=Y)")
    ax.set_xlabel("Membership in configuration  UE • UX • BSAT")
    ax.set_ylabel("Membership in outcome (high BSUC)")
    ax.set_title("Figure 10. fsQCA sufficiency XY plot\nfor the core "
                 "configuration UE•UX•BSAT", weight="bold")
    ax.text(0.04, 0.92, f"Consistency = {cons:.3f}\nRaw coverage = {cov:.3f}",
            transform=ax.transAxes, fontsize=10,
            bbox=dict(fc="white", ec=GREY, alpha=0.9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.legend(loc="lower right", frameon=False)
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig10_fsqca_XY_sufficiency.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 11: necessity XY plots (3 conditions)
# =====================================================================
def fig_necessity():
    CONDS = ["UE", "UX", "BSAT"]
    Y = cal["BSUC"].values
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    for ax, c in zip(axes, CONDS):
        X = cal[c].values
        cons = fz.consistency_nec(X, Y)
        ax.scatter(X, Y, s=22, alpha=0.45, color=GREEN, ec="white")
        ax.plot([0, 1], [0, 1], color=RED, ls="--", lw=1.3)
        ax.set_xlabel(f"Membership in {c}")
        if ax is axes[0]:
            ax.set_ylabel("Membership in high BSUC")
        ax.set_title(f"{c}  (necessity cons. = {cons:.3f})", weight="bold",
                     fontsize=10)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fig.suptitle("Figure 11. fsQCA necessity XY plots (no condition reaches the "
                 "0.90 necessity threshold)", weight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig11_fsqca_necessity.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 12: truth-table consistency bar chart
# =====================================================================
def fig_truthtable():
    d = tt.copy()
    d["config"] = d.apply(lambda r: "".join(
        [(c if r[c] == 1 else "~"+c) + ("•" if i < 2 else "")
         for i, c in enumerate(["UE", "UX", "BSAT"])]), axis=1)
    d = d.sort_values("raw_consistency", ascending=True)
    colors = [GREEN if o == 1 else GREY for o in d["OUT"]]
    fig, ax = plt.subplots(figsize=(9.5, 6))
    bars = ax.barh(d["config"], d["raw_consistency"], color=colors)
    for b, (_, r) in zip(bars, d.iterrows()):
        ax.text(r["raw_consistency"]+0.005, b.get_y()+b.get_height()/2,
                f"cons={r['raw_consistency']:.3f}, PRI={r['PRI']:.3f}, n={int(r['n_cases'])}",
                va="center", fontsize=8)
    ax.axvline(0.80, color=RED, ls="--", lw=1.2, label="Consistency cutoff = 0.80")
    ax.set_xlabel("Raw sufficiency consistency")
    ax.set_xlim(0, 1.15)
    ax.set_title("Figure 12. Truth-table configurations ranked by sufficiency "
                 "consistency\n(green = coded sufficient for high BSUC)", weight="bold")
    ax.legend(loc="lower right", frameon=False)
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig12_truth_table.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 13: Fiss-style configuration chart (core/peripheral)
# =====================================================================
def fig_config_chart():
    cp = pd.read_csv(f"{OUT}/T20_core_peripheral.csv")
    sol = pd.read_csv(f"{OUT}/T19_intermediate_solution.csv")
    neg = pd.read_csv(f"{OUT}/T21_negated_outcome_solution.csv")
    CONDS = ["UE", "UX", "BSAT"]
    # Build a matrix: rows=conditions, cols=solutions (high BSUC, ~BSUC)
    cols = ["High BSUC\n(UE•UX•BSAT)", "Low BSUC\n(~UE•~UX•~BSAT)"]
    fig, ax = plt.subplots(figsize=(6.5, 5.2))
    ax.set_xlim(-0.5, len(cols)-0.5); ax.set_ylim(-0.5, len(CONDS)-0.5)
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols)
    ax.set_yticks(range(len(CONDS))); ax.set_yticklabels(CONDS)
    ax.invert_yaxis()
    ax.grid(False)
    # high solution: all present, all core
    presence = {0: {"UE": 1, "UX": 1, "BSAT": 1}, 1: {"UE": 0, "UX": 0, "BSAT": 0}}
    roles = {(r["Condition"].replace("~", ""), 0): r["Role"]
             for _, r in cp.iterrows()}
    for ci, cond in enumerate(CONDS):
        for sj in range(len(cols)):
            val = presence[sj][cond]
            role = "core"  # both solutions are fully core here
            big = role == "core"
            size = 0.34 if big else 0.2
            if val == 1:
                circ = plt.Circle((sj, ci), size, color=BLUE, zorder=3)
                ax.add_patch(circ)
                ax.text(sj, ci, "●", color="white", ha="center", va="center")
            else:
                circ = plt.Circle((sj, ci), size, fc="white", ec=RED, lw=2,
                                  zorder=3, hatch="xxx")
                ax.add_patch(circ)
    # annotate coverage/consistency
    hi = sol.iloc[0]
    lo = neg.iloc[0]
    ax.text(0, len(CONDS)-0.35, f"cons={hi['consistency']:.3f}\ncov={hi['raw_coverage']:.3f}",
            ha="center", fontsize=8.5)
    ax.text(1, len(CONDS)-0.35, f"cons={lo['consistency']:.3f}\ncov={lo['raw_coverage']:.3f}",
            ha="center", fontsize=8.5)
    leg = [Patch(fc=BLUE, label="Core condition present"),
           Patch(fc="white", ec=RED, hatch="xxx", label="Core condition absent")]
    ax.legend(handles=leg, loc="upper center", bbox_to_anchor=(0.5, -0.08),
              ncol=2, frameon=False, fontsize=9)
    ax.set_title("Figure 13. Configurations for high vs. low BSUC\n(causal "
                 "asymmetry; large circles = core conditions)", weight="bold")
    plt.tight_layout()
    plt.savefig(f"{FIG}/Fig13_configurations.png", bbox_inches="tight")
    plt.close()

# =====================================================================
# FIG 14: correlation heatmap of all items (appendix)
# =====================================================================
def fig_item_corr():
    items = [i for b in BLOCKS.values() for i in b]
    C = df[items].corr()
    fig, ax = plt.subplots(figsize=(9, 8))
    im = ax.imshow(C, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(items))); ax.set_xticklabels(items, rotation=90, fontsize=7)
    ax.set_yticks(range(len(items))); ax.set_yticklabels(items, fontsize=7)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Pearson r")
    ax.set_title("Figure A1. Item-level correlation matrix", weight="bold")
    plt.tight_layout()
    plt.savefig(f"{FIG}/FigA1_item_correlations.png", bbox_inches="tight")
    plt.close()

import matplotlib.pyplot as _plt  # for Line2D in loadings
plt.Line2D = _plt.Line2D

for fn in [fig_structural, fig_paths_ci, fig_r2q2, fig_f2, fig_htmt, fig_fl,
           fig_loadings, fig_ipma, fig_calibration, fig_xy_sufficiency,
           fig_necessity, fig_truthtable, fig_config_chart, fig_item_corr]:
    fn()
    print("saved:", fn.__name__)

print("\nAll figures written to", FIG)
