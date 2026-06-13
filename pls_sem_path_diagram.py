"""
PLS-SEM structural results path diagram.
Clean, publication-style figure: path coefficients, R^2 values, and
significant vs non-significant paths.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

plt.rcParams["font.family"] = "DejaVu Serif"

fig, ax = plt.subplots(figsize=(13, 7.5), dpi=200)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis("off")

BOX_W, BOX_H = 2.5, 1.25
SIG_COLOR = "#1a1a1a"
NS_COLOR = "#b0b0b0"

def box(cx, cy, code, r2=None, endogenous=False):
    """Rounded construct box. Endogenous boxes get a light fill + R^2 line."""
    x = cx - BOX_W / 2
    y = cy - BOX_H / 2
    fc = "#f2f2f2" if endogenous else "white"
    patch = FancyBboxPatch(
        (x, y), BOX_W, BOX_H,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        linewidth=1.4, edgecolor=SIG_COLOR, facecolor=fc,
    )
    ax.add_patch(patch)
    if r2 is None:
        ax.text(cx, cy, code, ha="center", va="center",
                fontsize=13, fontweight="bold", color="#1a1a1a")
    else:
        ax.text(cx, cy + 0.24, code, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color="#1a1a1a")
        ax.text(cx, cy - 0.26, r2, ha="center", va="center",
                fontsize=9.2, color="#333333")
    return dict(cx=cx, cy=cy, w=BOX_W, h=BOX_H)

# ---- Column x-centres ----------------------------------------------------
C1, C2, C3, C4 = 2.1, 6.4, 10.6, 14.0

RP  = box(C1, 8.5, "RP")
SP  = box(C1, 6.6, "SP")
KSR = box(C1, 3.4, "KSR")
CBI = box(C1, 1.5, "CBI")

TMC = box(C2, 7.6, "TMC", r2="$R^2$ = 0.41", endogenous=True)
DI  = box(C2, 2.5, "DI",  r2="$R^2$ = 0.16 (n.s.)", endogenous=True)

GSCI = box(C3, 5.0, "GSCI", r2="$R^2$ = 0.57", endogenous=True)
GLP  = box(C4, 5.0, "GLP",  r2="$R^2$ = 0.59", endogenous=True)

# ---- Arrow + label helpers ----------------------------------------------
def edge(b, side):
    cx, cy, w, h = b["cx"], b["cy"], b["w"], b["h"]
    return {
        "r": (cx + w / 2, cy), "l": (cx - w / 2, cy),
        "t": (cx, cy + h / 2), "b": (cx, cy - h / 2),
    }[side]

def arrow(p0, p1, rad=0.0, color=SIG_COLOR, dashed=False, lw=1.6):
    a = FancyArrowPatch(
        p0, p1, connectionstyle=f"arc3,rad={rad}",
        arrowstyle="-|>", mutation_scale=16,
        linewidth=lw, color=color, shrinkA=2, shrinkB=2,
        linestyle="--" if dashed else "-",
    )
    ax.add_patch(a)

def beta(x, y, text, color="#000000"):
    ax.text(x, y, text, ha="center", va="center", fontsize=10.5,
            fontweight="bold", color=color,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))

# ---- Significant paths ---------------------------------------------------
arrow(edge(RP, "r"), (edge(TMC, "l")[0], edge(TMC, "l")[1] + 0.1), rad=-0.05)
beta(4.25, 8.4, "0.44")

arrow(edge(SP, "r"), (edge(TMC, "l")[0], edge(TMC, "l")[1] - 0.15), rad=0.06)
beta(4.25, 6.75, "0.29")

arrow(edge(KSR, "r"), (edge(DI, "l")[0], edge(DI, "l")[1] + 0.1), rad=-0.05)
beta(4.25, 3.25, "0.61")

arrow(edge(TMC, "b"), edge(GSCI, "t"), rad=-0.18)
beta(8.5, 6.7, "0.38")

arrow(edge(DI, "t"), edge(GSCI, "b"), rad=0.18)
beta(8.6, 3.25, "0.41")

arrow(edge(GSCI, "r"), edge(GLP, "l"))
beta(12.3, 5.32, "0.49")

# TMC -> GLP direct effect (the previously floating 0.27), arcing over the top
arrow(edge(TMC, "t"), (GLP["cx"], GLP["cy"] + GLP["h"] / 2), rad=-0.32)
beta(10.6, 8.85, "0.27")

# ---- Non-significant path: CBI -> DI (dashed grey) -----------------------
arrow(edge(CBI, "r"), (edge(DI, "l")[0], edge(DI, "l")[1] - 0.2),
      rad=0.10, color=NS_COLOR, dashed=True, lw=1.4)
beta(4.35, 1.65, "n.s.", color=NS_COLOR)

# ---- Legend --------------------------------------------------------------
legend_handles = [
    Line2D([0], [0], color=SIG_COLOR, lw=1.8, linestyle="-",
           label="Significant path (p < 0.05)"),
    Line2D([0], [0], color=NS_COLOR, lw=1.6, linestyle="--",
           label="Non-significant path"),
]
ax.legend(handles=legend_handles, loc="lower center",
          bbox_to_anchor=(0.5, -0.02), ncol=2, frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig("/projects/sandbox/BSRS/pls_sem_path_diagram.png",
            dpi=200, bbox_inches="tight", facecolor="white")
print("saved")
