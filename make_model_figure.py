# -*- coding: utf-8 -*-
"""Conceptual model + hypotheses figure for the metaverse branding paper.

Professional, monochrome (publication-grade) path diagram following standard
mediation conventions (a-paths, b-path, c'-direct paths). No accent colors.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---- monochrome, journal-style palette ----
INK  = "#000000"   # boxes, primary text, hypothesized paths
DARK = "#333333"   # path labels
GREY = "#808080"   # theoretical-foundations box, dashed grounding arrows
NOTE = "#4d4d4d"   # caption notes
WHITE = "#ffffff"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
    "svg.fonttype": "none",
    "mathtext.fontset": "dejavuserif",
})

fig, ax = plt.subplots(figsize=(10.0, 5.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")


def box(cx, cy, w, h, title, sub, edge=INK, lw=1.2, title_fs=12.5, sub_fs=10):
    b = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                       boxstyle="round,pad=0.015,rounding_size=0.06",
                       linewidth=lw, edgecolor=edge, facecolor=WHITE, zorder=3)
    ax.add_patch(b)
    if sub:
        ax.text(cx, cy + 0.17, title, ha="center", va="center",
                fontsize=title_fs, color=INK, zorder=4)
        ax.text(cx, cy - 0.22, sub, ha="center", va="center",
                fontsize=sub_fs, color=DARK, style="italic", zorder=4)
    else:
        ax.text(cx, cy, title, ha="center", va="center",
                fontsize=title_fs, color=INK, zorder=4)
    return dict(cx=cx, cy=cy, w=w, h=h)


def arrow(p1, p2, rad=0.0, color=INK, lw=1.3, ls="-", z=2, ms=14):
    a = FancyArrowPatch(p1, p2,
                        connectionstyle=f"arc3,rad={rad}",
                        arrowstyle="-|>", mutation_scale=ms,
                        linewidth=lw, color=color, linestyle=ls, zorder=z,
                        shrinkA=3, shrinkB=3)
    ax.add_patch(a)


def label(x, y, text, fs=10.5, color=DARK, style="italic", weight="normal"):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=color, style=style, fontweight=weight, zorder=6,
            bbox=dict(boxstyle="round,pad=0.12", fc=WHITE, ec="none", alpha=1.0))


# ---- theoretical foundations (grounding) ----
band = FancyBboxPatch((0.30, 2.05), 1.55, 2.55,
                      boxstyle="round,pad=0.02,rounding_size=0.05",
                      linewidth=1.0, edgecolor=GREY, facecolor=WHITE, zorder=1)
ax.add_patch(band)
ax.text(1.075, 4.28, "Theoretical", ha="center", va="center",
        fontsize=9.5, color=DARK)
ax.text(1.075, 4.04, "foundations", ha="center", va="center",
        fontsize=9.5, color=DARK)
ax.text(1.075, 3.30, "Flow Theory\n\nSelf-Determination\nTheory",
        ha="center", va="center", fontsize=8.8, color=GREY)

# ---- construct boxes ----
UE   = box(3.75, 5.05, 2.6, 1.0, "User Engagement", "(UE)")
UX   = box(3.75, 1.95, 2.6, 1.0, "User Experience", "(UX)")
BSAT = box(7.15, 3.5, 2.6, 1.0, "Brand Satisfaction", "(BSAT) \u2014 mediator")
BSUC = box(10.35, 3.5, 2.4, 1.0, "Brand Success", "(BSUC)")

# ---- grounding (dashed, grey) ----
arrow((1.88, 4.35), (2.42, 4.85), color=GREY, lw=0.9, ls=(0, (4, 3)), z=1, ms=10)
arrow((1.88, 2.30), (2.42, 2.15), color=GREY, lw=0.9, ls=(0, (4, 3)), z=1, ms=10)

# ---- indirect (mediated) paths: a1, a2, b ----
arrow((5.05, 4.70), (5.95, 3.95), color=INK, lw=1.3)   # a1: UE -> BSAT
arrow((5.05, 2.30), (5.95, 3.05), color=INK, lw=1.3)   # a2: UX -> BSAT
arrow((8.45, 3.5), (9.15, 3.5), color=INK, lw=1.4)     # b:  BSAT -> BSUC

label(5.30, 4.58, r"$a_1\,(+)$", fs=10)
label(5.30, 2.42, r"$a_2\,(+)$", fs=10)
label(8.80, 3.78, r"$b\,(+)$",  fs=10)

# ---- direct paths (hypotheses H1, H2) ----
arrow((4.70, 5.45), (9.55, 4.20), rad=-0.30, color=INK, lw=1.35)  # H1: UE -> BSUC
arrow((4.70, 1.55), (9.55, 2.80), rad=0.30,  color=INK, lw=1.35)  # H2: UX -> BSUC

label(7.10, 6.28, r"H1 (+):  UE $\rightarrow$ BSUC  ($c_1^{\,\prime}$)", fs=10.5, color=INK)
label(7.10, 0.70, r"H2 (+):  UX $\rightarrow$ BSUC  ($c_2^{\,\prime}$)", fs=10.5, color=INK)
label(7.95, 4.18, "H3 (+):  BSAT mediates\nUE / UX \u2192 BSUC", fs=9.8, color=INK)

# ---- title + notes ----
fig.text(0.5, 0.965, "Figure 4. Conceptual model and hypotheses.",
         ha="center", fontsize=12.5, color=INK)
note = ("Notes. Solid arrows denote hypothesized positive relationships. Brand satisfaction is "
        "modelled as a mediator (H3) of the engagement/experience\u2013success links via the indirect "
        "paths a\u2081b and a\u2082b; c\u2081\u2032 and c\u2082\u2032 denote direct effects. P1 (equifinality): multiple sufficient "
        "configurations of UE, UX and BSAT can yield high BSUC, evaluated through fuzzy-set "
        "qualitative comparative analysis (fsQCA).")
fig.text(0.5, 0.045, note, ha="center", va="center", fontsize=8.3, color=NOTE, wrap=True)

plt.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.115)
for ext, dpi in [("png", 300), ("pdf", None), ("svg", None)]:
    fig.savefig(f"Figure1_Conceptual_Model.{ext}", dpi=dpi, bbox_inches="tight",
                facecolor="white")
print("Saved Figure1_Conceptual_Model.png / .pdf / .svg")
