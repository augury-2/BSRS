# -*- coding: utf-8 -*-
"""Minimalist conceptual model + hypotheses figure for the metaverse branding paper."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.font_manager import FontProperties

# ---- palette (minimalist: near-black + one teal accent + soft grey) ----
INK   = "#1f2937"   # box border / text
FILL  = "#ffffff"
GREY  = "#9aa3ad"   # secondary lines / lens band
PALE  = "#f4f6f7"   # lens band fill
ACC   = "#0f766e"   # teal accent for hypotheses / signs

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "svg.fonttype": "none",
})

fig, ax = plt.subplots(figsize=(11.5, 6.2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")

def box(cx, cy, w, h, title, sub, title_fs=13, sub_fs=10):
    b = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                       boxstyle="round,pad=0.02,rounding_size=0.14",
                       linewidth=1.4, edgecolor=INK, facecolor=FILL, zorder=3)
    ax.add_patch(b)
    ax.text(cx, cy + 0.16, title, ha="center", va="center",
            fontsize=title_fs, fontweight="bold", color=INK, zorder=4)
    ax.text(cx, cy - 0.24, sub, ha="center", va="center",
            fontsize=sub_fs, color="#52606d", style="italic", zorder=4)
    return dict(cx=cx, cy=cy, w=w, h=h)

def arrow(p1, p2, rad=0.0, color=INK, lw=1.6, ls="-", z=2):
    a = FancyArrowPatch(p1, p2,
                        connectionstyle=f"arc3,rad={rad}",
                        arrowstyle="-|>", mutation_scale=16,
                        linewidth=lw, color=color, linestyle=ls, zorder=z,
                        shrinkA=2, shrinkB=2)
    ax.add_patch(a)

def label(x, y, text, fs=11, color=ACC, weight="bold", bg=True):
    bbox = dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.95) if bg else None
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=color, fontweight=weight, zorder=6, bbox=bbox)

# ---- theoretical lenses band (far left) ----
band = FancyBboxPatch((0.25, 1.05), 1.5, 4.9,
                      boxstyle="round,pad=0.02,rounding_size=0.12",
                      linewidth=1.0, edgecolor=GREY, facecolor=PALE, zorder=1)
ax.add_patch(band)
ax.text(1.0, 5.55, "THEORETICAL", ha="center", va="center", fontsize=8.5,
        color="#52606d", fontweight="bold")
ax.text(1.0, 5.25, "LENSES", ha="center", va="center", fontsize=8.5,
        color="#52606d", fontweight="bold")
ax.text(1.0, 3.5, "Flow Theory\n\nSelf-Determination\nTheory\n(autonomy,\ncompetence,\nrelatedness)",
        ha="center", va="center", fontsize=9.2, color="#52606d")

# ---- construct boxes ----
UE   = box(3.55, 5.05, 2.7, 1.15, "User Engagement", "(UE)")
UX   = box(3.55, 1.95, 2.7, 1.15, "User Experience", "(UX)")
BSAT = box(7.05, 3.5, 2.7, 1.15, "Brand Satisfaction", "(BSAT) \u2014 mediator")
BSUC = box(10.35, 3.5, 2.7, 1.15, "Brand Success", "(BSUC)")

# ---- lens -> antecedents (faint, dashed) ----
arrow((1.78, 4.7), (2.18, 4.95), color=GREY, lw=1.0, ls=(0,(4,3)), z=1)
arrow((1.78, 2.3), (2.18, 2.05), color=GREY, lw=1.0, ls=(0,(4,3)), z=1)

# ---- mediated (indirect) paths: UE->BSAT, UX->BSAT, BSAT->BSUC ----
arrow((4.9, 4.75), (5.75, 3.95), color=INK, lw=1.6)          # a1: UE -> BSAT
arrow((4.9, 2.25), (5.75, 3.05), color=INK, lw=1.6)          # a2: UX -> BSAT
arrow((8.4, 3.5), (8.99, 3.5), color=INK, lw=1.8)            # b: BSAT -> BSUC

label(5.15, 4.62, "a\u2081 (+)", fs=9.5, color="#52606d", weight="normal")
label(5.15, 2.40, "a\u2082 (+)", fs=9.5, color="#52606d", weight="normal")
label(8.70, 3.85, "b (+)", fs=9.5, color="#52606d", weight="normal")

# ---- direct paths (hypotheses H1, H2) ----
arrow((4.55, 5.45), (9.55, 4.25), rad=-0.32, color=ACC, lw=1.8)   # H1: UE -> BSUC (over top)
arrow((4.55, 1.55), (9.55, 2.75), rad=0.32, color=ACC, lw=1.8)    # H2: UX -> BSUC (under)

label(7.0, 6.35, "H1 (+):  UE \u2192 BSUC", fs=11)
label(7.0, 0.62, "H2 (+):  UX \u2192 BSUC", fs=11)
label(7.7, 4.18, "H3 (+):  BSAT mediates\nUE / UX \u2192 BSUC", fs=10.2)

# ---- title + notes ----
fig.text(0.5, 0.965, "Figure 1.  Conceptual Model and Hypotheses",
         ha="center", fontsize=14.5, fontweight="bold", color=INK)
note = ("Notes. H1\u2013H3 denote hypothesized positive relationships. Brand satisfaction is modelled as a "
        "mediator (H3) of the engagement/experience\u2013success links (indirect paths a\u2081, a\u2082, b). "
        "P1 proposes equifinality: multiple sufficient configurations of UE, UX and BSAT for high BSUC, "
        "evaluated through fuzzy-set qualitative comparative analysis (fsQCA).")
fig.text(0.5, 0.045, note, ha="center", va="center", fontsize=8.6, color="#52606d", wrap=True)

plt.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.10)
for ext, dpi in [("png", 300), ("pdf", None), ("svg", None)]:
    fig.savefig(f"Figure1_Conceptual_Model.{ext}", dpi=dpi, bbox_inches="tight",
                facecolor="white")
print("Saved Figure1_Conceptual_Model.png / .pdf / .svg")
