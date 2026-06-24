"""
Figure generation for the JMIS Results section.

NOTE ON VALUES: The path coefficients, R-squared, and coverage/consistency
numbers used to LABEL these figures are illustrative placeholders consistent
with the SOP model (BSAT as mediator, BSUC as final outcome). They MUST be
replaced with the author's actual SmartPLS / fsQCA output for the BSUC model
before submission. The measurement-model numbers (Table 2) come from the
provided PLS-SEM document and are reusable.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Ellipse, FancyBboxPatch
import numpy as np

# ----------------------------------------------------------------------------
# Illustrative SOP-model estimates (REPLACE WITH ACTUAL OUTPUT)
# ----------------------------------------------------------------------------
b_UE_BSAT  = 0.34
b_UX_BSAT  = 0.41
b_UE_BSUC  = 0.23   # H1 direct
b_UX_BSUC  = 0.20   # H2 direct
b_BSAT_BSUC = 0.39
r2_BSAT = 0.46
r2_BSUC = 0.55

# ============================================================================
# FIGURE 1 - Structural model path diagram (JMIS standard)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis("off")

def oval(ax, x, y, w, h, label, sub=None, r2=None):
    e = Ellipse((x, y), w, h, fill=True, facecolor="#eef3fb",
                edgecolor="#1f3b66", lw=2.0, zorder=2)
    ax.add_patch(e)
    txt = label
    ax.text(x, y + (0.18 if (sub or r2) else 0), label, ha="center", va="center",
            fontsize=14, fontweight="bold", color="#1f3b66", zorder=3)
    if sub:
        ax.text(x, y - 0.16, sub, ha="center", va="center", fontsize=8.5,
                color="#1f3b66", zorder=3)
    if r2 is not None:
        ax.text(x, y - 0.40, f"$R^2$ = {r2:.2f}", ha="center", va="center",
                fontsize=10, style="italic", color="#7a1f1f", zorder=3)

# Positions
UE   = (1.4, 5.3)
UX   = (1.4, 1.7)
BSAT = (5.0, 5.1)
BSUC = (8.4, 3.5)

oval(ax, *UE,   1.9, 1.25, "UE", "User Engagement")
oval(ax, *UX,   1.9, 1.25, "UX", "User Experience")
oval(ax, *BSAT, 2.0, 1.3,  "BSAT", "Brand Satisfaction", r2=r2_BSAT)
oval(ax, *BSUC, 2.0, 1.3,  "BSUC", "Brand Success", r2=r2_BSUC)

def arrow(ax, p1, p2, label, dashed=False, color="#1f3b66", off=(0,0), rad=0.0):
    style = "--" if dashed else "-"
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=18,
                        lw=1.8, color=color, linestyle=style,
                        connectionstyle=f"arc3,rad={rad}", zorder=1,
                        shrinkA=22, shrinkB=22)
    ax.add_patch(a)
    mx = (p1[0] + p2[0]) / 2 + off[0]
    my = (p1[1] + p2[1]) / 2 + off[1]
    ax.text(mx, my, label, ha="center", va="center", fontsize=10.5,
            fontweight="bold", color=color,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
            zorder=4)

# Paths to mediator (solid)
arrow(ax, UE, BSAT, f"{b_UE_BSAT:.2f}***", off=(-0.1, 0.25))
arrow(ax, UX, BSAT, f"{b_UX_BSAT:.2f}***", off=(0.0, -0.25), rad=0.05)
# Mediator to outcome (solid)
arrow(ax, BSAT, BSUC, f"{b_BSAT_BSUC:.2f}***", off=(0.2, 0.25))
# Direct paths (dashed to emphasise mediation)
arrow(ax, UE, BSUC, f"{b_UE_BSUC:.2f}*** (H1)", dashed=True, color="#7a1f1f",
      off=(0.4, 0.55), rad=-0.18)
arrow(ax, UX, BSUC, f"{b_UX_BSUC:.2f}** (H2)", dashed=True, color="#7a1f1f",
      off=(0.4, -0.55), rad=0.18)

ax.text(5.0, 0.45,
        "Solid lines: paths to/from mediator (H3 chain).  "
        "Dashed lines: direct effects (H1, H2).\n"
        "*** p < 0.001, ** p < 0.01.   Coefficients are standardized.",
        ha="center", va="center", fontsize=8.5, color="#444")

plt.tight_layout()
plt.savefig("figures/figure1_structural_model.png", dpi=300, bbox_inches="tight")
plt.close()

# ============================================================================
# FIGURE 2 - fsQCA sufficient configurations for high BSUC (P1)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.text(5, 5.6, "Sufficient configurations for high Brand Success (BSUC)",
        ha="center", fontsize=13, fontweight="bold", color="#1f3b66")

configs = [
    ("C1", ["UE +", "UX +", "BSAT +"], "Raw cov. 0.46  |  Cons. 0.89", 4.3),
    ("C2", ["UE +", "BSAT +"],         "Raw cov. 0.41  |  Cons. 0.87", 2.6),
    ("C3", ["UE +", "UX +"],           "Raw cov. 0.38  |  Cons. 0.85", 0.9),
]
for cid, conds, metr, y in configs:
    box = FancyBboxPatch((0.6, y-0.42), 5.4, 0.95,
                         boxstyle="round,pad=0.05,rounding_size=0.12",
                         fc="#eef3fb", ec="#1f3b66", lw=1.6, zorder=2)
    ax.add_patch(box)
    ax.text(1.0, y, cid, ha="left", va="center", fontsize=12,
            fontweight="bold", color="#1f3b66")
    ax.text(1.9, y, "  +  ".join(conds), ha="left", va="center", fontsize=10.5,
            color="#1f3b66")
    ax.text(3.3, y-0.62, metr, ha="left", va="center", fontsize=8, color="#666")
    a = FancyArrowPatch((6.05, y), (7.7, 3.0), arrowstyle="-|>",
                        mutation_scale=16, lw=1.6, color="#7a1f1f",
                        connectionstyle="arc3,rad=0.0", zorder=1,
                        shrinkA=4, shrinkB=22)
    ax.add_patch(a)

outc = Ellipse((8.5, 3.0), 2.3, 1.5, fc="#fbeeee", ec="#7a1f1f", lw=2.0, zorder=3)
ax.add_patch(outc)
ax.text(8.5, 3.2, "High", ha="center", fontsize=12, fontweight="bold", color="#7a1f1f")
ax.text(8.5, 2.85, "BSUC", ha="center", fontsize=13, fontweight="bold", color="#7a1f1f")
ax.text(8.5, 2.5, "(brand success)", ha="center", fontsize=8, color="#7a1f1f")

ax.text(5, 0.35,
        "Solution coverage = 0.61   |   Solution consistency = 0.86   "
        "(equifinality: multiple sufficient 'recipes', supporting P1)",
        ha="center", fontsize=8.5, color="#444")
plt.tight_layout()
plt.savefig("figures/figure2_fsqca_pathways.png", dpi=300, bbox_inches="tight")
plt.close()

# ============================================================================
# FIGURE 3 - Reliability & validity bar chart (from provided PLS-SEM Table)
# ============================================================================
constructs = ["UE", "UX", "BSAT", "BSUC", "ATT"]
alpha = [0.93, 0.92, 0.90, 0.90, 0.78]
rho   = [0.95, 0.94, 0.95, 0.93, 0.90]
ave   = [0.79, 0.77, 0.73, 0.77, 0.82]

x = np.arange(len(constructs))
w = 0.26
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - w, alpha, w, label="Cronbach's $\\alpha$", color="#1f3b66")
ax.bar(x,      rho,  w, label="Composite reliability $\\rho_C$", color="#4f7cb3")
ax.bar(x + w,  ave,  w, label="AVE", color="#9fc0e0")
ax.axhline(0.70, ls="--", color="#7a1f1f", lw=1.2)
ax.text(len(constructs)-0.5, 0.71, "0.70 reliability threshold", color="#7a1f1f", fontsize=8, va="bottom", ha="right")
ax.axhline(0.50, ls=":", color="#2e7d32", lw=1.2)
ax.text(len(constructs)-0.5, 0.51, "0.50 AVE threshold", color="#2e7d32", fontsize=8, va="bottom", ha="right")
ax.set_xticks(x); ax.set_xticklabels(constructs)
ax.set_ylim(0, 1.05); ax.set_ylabel("Value")
ax.set_title("Construct reliability and convergent validity", fontsize=12, fontweight="bold")
ax.legend(loc="lower right", fontsize=9)
plt.tight_layout()
plt.savefig("figures/figure3_reliability.png", dpi=300, bbox_inches="tight")
plt.close()

print("Figures written:")
import os
for f in sorted(os.listdir("figures")):
    if f.endswith(".png"):
        print("  figures/" + f)
