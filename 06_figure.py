import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")

def box(x, y, label, sub=""):
    b = FancyBboxPatch((x-1.05, y-0.55), 2.1, 1.1,
                       boxstyle="round,pad=0.02,rounding_size=0.1",
                       fc="#eef3fb", ec="#2c3e50", lw=1.6)
    ax.add_patch(b)
    ax.text(x, y+0.12, label, ha="center", va="center", fontsize=12, fontweight="bold")
    if sub:
        ax.text(x, y-0.28, sub, ha="center", va="center", fontsize=8.5, color="#555")

# positions
UE=(1.4,5.3); UX=(1.4,1.7); BSAT=(5.0,3.5); BSUC=(8.6,3.5)
box(*UE,"UE"); box(*UX,"UX")
box(*BSAT,"BSAT", "R\u00b2 = .013"); box(*BSUC,"BSUC","R\u00b2 = .008")

def arrow(p1,p2,beta,p,offset=0.0,color="#333"):
    a=FancyArrowPatch(p1,p2,arrowstyle="-|>",mutation_scale=16,
                      lw=1.4,color=color,shrinkA=58,shrinkB=58,
                      connectionstyle=f"arc3,rad={offset}")
    ax.add_patch(a)
    mx=(p1[0]+p2[0])/2; my=(p1[1]+p2[1])/2 + offset*2.2
    sig = "n.s." 
    ax.text(mx,my+0.18,f"\u03b2={beta}",ha="center",fontsize=9.5,color=color,fontweight="bold")
    ax.text(mx,my-0.05,f"({sig})",ha="center",fontsize=8,color="#999")

arrow(UE,BSAT,"-.045","H1a",offset=0.05)
arrow(UX,BSAT,".103","H1b",offset=-0.05)
arrow(BSAT,BSUC,".029","H2")
arrow(UE,BSUC,".062","H3a",offset=0.16,color="#888")
arrow(UX,BSUC,"-.060","H3b",offset=-0.16,color="#888")

ax.text(5.0,6.6,"Figure 1. PLS-SEM structural model (standardized path coefficients; n = 312, 5,000 bootstrap subsamples)",
        ha="center",fontsize=10.5,fontweight="bold")
ax.text(5.0,0.35,"All structural paths non-significant (95% bootstrap CIs include zero). n.s. = not significant.",
        ha="center",fontsize=9,style="italic",color="#666")
plt.tight_layout()
plt.savefig("Figure1_structural_model.png",dpi=160,bbox_inches="tight")
print("saved Figure1_structural_model.png")
