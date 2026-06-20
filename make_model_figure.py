# -*- coding: utf-8 -*-
"""Conceptual model + hypotheses figure (framework block-diagram style).

Professional, grayscale, flat-rectangle layout in the style of established
conceptual frameworks: bold underlined headers, bulleted sub-items, category
shading with a legend, solid black arrows, and a role legend row.

Model: User Engagement (UE) and User Experience (UX) -> Brand Satisfaction
(BSAT, mediator) -> Brand Success (BSUC), grounded in Flow Theory and
Self-Determination Theory. Hypotheses H1-H3 and configurational note P1.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

# ---- grayscale palette (matches reference) ----
INK   = "#000000"
LIGHT = "#d9d9d9"   # experiential antecedents
MED   = "#a6a6a6"   # mediating evaluation
WHITE = "#ffffff"   # theoretical lens / brand outcome

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Calibri", "Helvetica"],
    "svg.fonttype": "none",
})

fig, ax = plt.subplots(figsize=(14.0, 8.2))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis("off")

PAD = 0.16


def block(x, y, w, h, header, fill=WHITE, bullets=None, subtitle=None,
          header_fs=11.5, bullet_fs=9.8, sub_fs=9.2, header_wrap=None):
    """Flat rectangle with bold underlined header and optional bulleted body."""
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=INK,
                           linewidth=1.3, zorder=2))
    hx = x + PAD
    hy = y + h - PAD
    head = header_wrap if header_wrap else [header]
    for k, line in enumerate(head):
        ax.text(hx, hy - k * 0.30, line, ha="left", va="top",
                fontsize=header_fs, fontweight="bold", color=INK, zorder=4)
    rule_y = hy - 0.30 * len(head) - 0.02
    ax.plot([hx, x + w - PAD], [rule_y, rule_y], color=INK, lw=1.0, zorder=4)
    cy = rule_y - 0.12
    if subtitle:
        cy -= 0.26
        ax.text(hx, cy + 0.10, subtitle, ha="left", va="top",
                fontsize=sub_fs, style="italic", color=INK, zorder=4)
    if bullets:
        for b in bullets:
            cy -= 0.355
            ax.text(hx, cy + 0.12, u"\u2022  " + b, ha="left", va="top",
                    fontsize=bullet_fs, color=INK, zorder=4)


def arrow(p1, p2, lw=1.4, ms=16, z=3):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                                 linewidth=lw, color=INK, zorder=z,
                                 shrinkA=2, shrinkB=2))


def plabel(x, y, text, fs=10, bold=True):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=INK, zorder=6,
            bbox=dict(boxstyle="square,pad=0.18", fc=WHITE, ec="none"))


# ---------------- theoretical foundations (left lens column) ----------------
fx, fy, fw, fh = 0.30, 3.05, 2.25, 4.40
ax.add_patch(Rectangle((fx, fy), fw, fh, facecolor=WHITE, edgecolor=INK,
                       linewidth=1.3, zorder=2))
ax.text(fx + PAD, fy + fh - PAD, "Theoretical", ha="left", va="top",
        fontsize=11.5, fontweight="bold", color=INK, zorder=4)
ax.text(fx + PAD, fy + fh - PAD - 0.30, "Foundations:", ha="left", va="top",
        fontsize=11.5, fontweight="bold", color=INK, zorder=4)
ax.plot([fx + PAD, fx + fw - PAD], [fy + fh - PAD - 0.66, fy + fh - PAD - 0.66],
        color=INK, lw=1.0, zorder=4)
# lens 1
ax.text(fx + PAD, fy + fh - 1.15, "Flow Theory", ha="left", va="top",
        fontsize=10.6, fontweight="bold", color=INK, zorder=4)
ax.text(fx + PAD, fy + fh - 1.50, "challenge\u2013skill balance,\nclear goals, feedback",
        ha="left", va="top", fontsize=8.8, color=INK, zorder=4)
# lens 2
ax.text(fx + PAD, fy + fh - 2.55, "Self-Determination", ha="left", va="top",
        fontsize=10.6, fontweight="bold", color=INK, zorder=4)
ax.text(fx + PAD, fy + fh - 2.86, "Theory", ha="left", va="top",
        fontsize=10.6, fontweight="bold", color=INK, zorder=4)
ax.text(fx + PAD, fy + fh - 3.21, "autonomy, competence,\nrelatedness",
        ha="left", va="top", fontsize=8.8, color=INK, zorder=4)

# ---------------- antecedent blocks (light grey) ----------------
block(4.35, 5.30, 2.95, 2.20, "User Engagement (UE):", fill=LIGHT,
      bullets=["Cognitive involvement", "Emotional involvement",
               "Behavioural participation"])
block(4.35, 2.30, 2.95, 2.20, "User Experience (UX):", fill=LIGHT,
      bullets=["Immersion & presence", "Usability", "Enjoyment"])

# ---------------- mediator block (medium grey) ----------------
block(8.30, 3.55, 2.45, 2.30, "Brand Satisfaction", fill=MED,
      header_wrap=["Brand Satisfaction", "(BSAT):"], subtitle="Mediator",
      bullets=["Cumulative brand", "  evaluation", "Affective response"],
      header_fs=11.0)

# ---------------- outcome block (white) ----------------
block(11.45, 3.05, 2.30, 3.05, "Brand Success", fill=WHITE,
      header_wrap=["Brand Success", "(BSUC):"],
      bullets=["Continuance intention", "Purchase intention",
               "Advocacy", "Word-of-mouth (WOM)"])

# ---------------- arrows ----------------
# foundations -> antecedents (grounding)
arrow((fx + fw, 6.35), (4.35, 6.40), lw=1.3, ms=14)
arrow((fx + fw, 4.10), (4.35, 3.40), lw=1.3, ms=14)
# indirect (mediated) paths a1, a2, b
arrow((7.30, 6.00), (8.30, 5.30))           # a1: UE -> BSAT
arrow((7.30, 3.80), (8.30, 4.35))           # a2: UX -> BSAT
arrow((10.75, 4.70), (11.45, 4.70))         # b: BSAT -> BSUC
plabel(7.85, 5.92, u"a\u2081 (+)", fs=9.5)
plabel(7.85, 3.78, u"a\u2082 (+)", fs=9.5)
plabel(11.10, 4.97, u"b (+)", fs=9.5)
# direct effects (hypotheses H1, H2) - straight diagonals
arrow((7.30, 6.95), (11.45, 5.75), lw=1.5)  # H1: UE -> BSUC
arrow((7.30, 2.85), (11.45, 3.95), lw=1.5)  # H2: UX -> BSUC
plabel(9.35, 6.86, u"H1 (+):  UE \u2192 BSUC  (c\u2081\u2032)", fs=9.6)
plabel(9.35, 2.74, u"H2 (+):  UX \u2192 BSUC  (c\u2082\u2032)", fs=9.6)
plabel(9.52, 3.30, u"H3 (+):  BSAT mediates\nUE / UX \u2192 BSUC", fs=8.9)

# ---------------- shading legend (top-right) ----------------
def swatch(x, y, fill, label):
    ax.add_patch(Rectangle((x, y), 0.46, 0.30, facecolor=fill, edgecolor=INK,
                           linewidth=1.1, zorder=4))
    ax.text(x + 0.60, y + 0.15, label, ha="left", va="center",
            fontsize=9.4, color=INK, zorder=4)

swatch(10.55, 8.35, LIGHT, "Experiential antecedent (UE, UX)")
swatch(10.55, 7.90, MED,   "Mediating evaluation (BSAT)")
swatch(10.55, 7.45, WHITE, "Theoretical lens / brand outcome")

# ---------------- role legend row (bottom) ----------------
def legbox(x, fill, label):
    ax.add_patch(Rectangle((x, 0.55), 1.85, 0.62, facecolor=fill,
                           edgecolor=INK, linewidth=1.2, zorder=2))
    ax.text(x + 0.925, 0.86, label, ha="center", va="center",
            fontsize=9.6, fontweight="bold", color=INK, zorder=4)

legbox(0.80, WHITE, "Theoretical lens")
legbox(3.70, LIGHT, "Antecedents (UE, UX)")
legbox(6.60, MED,   "Mediator (BSAT)")
legbox(9.50, WHITE, "Outcome (BSUC)")

# ---------------- title + note ----------------
fig.text(0.5, 0.965, "Figure 4. Conceptual model and hypotheses.",
         ha="center", fontsize=13, fontweight="bold", color=INK)
note = ("Notes. Solid arrows denote hypothesized positive relationships. Brand satisfaction is modelled as a "
        "mediator (H3) of the engagement/experience\u2013success links via the indirect paths a\u2081b and a\u2082b; c\u2081\u2032 and "
        "c\u2082\u2032 denote direct effects. P1 (equifinality): multiple sufficient configurations of UE, UX and BSAT can "
        "yield high BSUC, evaluated through fuzzy-set qualitative comparative analysis (fsQCA).")
fig.text(0.5, 0.045, note, ha="center", va="center", fontsize=8.6, color=INK, wrap=True)

plt.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.10)
for ext, dpi in [("png", 300), ("pdf", None), ("svg", None)]:
    fig.savefig(f"Figure1_Conceptual_Model.{ext}", dpi=dpi, bbox_inches="tight",
                facecolor="white")
print("Saved Figure1_Conceptual_Model.png / .pdf / .svg")
