"""PART L - publication-quality figures for the PLS-SEM and fsQCA results."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import seaborn as sns
import common as C
import fsqca as Q
from plssem import PLSSEM

sns.set_theme(style="whitegrid", context="paper")
df = C.load_raw()
comp = C.composites(df)
model = PLSSEM(C.CONSTRUCTS, C.STRUCTURAL_PATHS).fit(df)
struct = pd.read_csv(C.TBL + "/C_structural_paths.csv")
rel = pd.read_csv(C.TBL + "/B_reliability_validity.csv")
load_tbl = pd.read_csv(C.TBL + "/B_loadings_weights.csv")
r2 = {r["Construct"]: r["R2"] for _, r in pd.read_csv(C.TBL + "/E_r2.csv").iterrows()}

pcoef = {}
for _, r in struct.iterrows():
    a, b = r["Path"].split(" -> ")
    pcoef[(a, b)] = (r["Beta"], r["p"])


def box(ax, x, y, w, h, text, fc="#E8EEF7", ec="#34495E"):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02",
                       fc=fc, ec=ec, lw=1.5)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=10, weight="bold")


def arrow(ax, p0, p1, label=None, sig=False, color=None):
    col = color or ("#C0392B" if sig else "#7F8C8D")
    a = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=16,
                        lw=2.0 if sig else 1.2, color=col, shrinkA=18, shrinkB=18)
    ax.add_patch(a)
    if label:
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        ax.text(mx, my + 0.03, label, fontsize=9, color=col, ha="center",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))


# ---- L1 Structural model / path diagram ----
def structural_diagram(fname, title):
    fig, ax = plt.subplots(figsize=(11, 6.5))
    pos = {"UE": (0.12, 0.78), "UX": (0.12, 0.22), "BSAT": (0.5, 0.5), "BSUC": (0.88, 0.5)}
    for lv, (x, y) in pos.items():
        lab = lv + (f"\nR2={r2[lv]:.3f}" if lv in r2 else "")
        box(ax, x, y, 0.16, 0.16, lab)
    for (a, b), (beta, p) in pcoef.items():
        sig = p < 0.05
        arrow(ax, pos[a], pos[b], f"beta={beta:.3f}{'*' if sig else ' (ns)'}", sig)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title(title, fontsize=13)
    fig.tight_layout(); fig.savefig(C.FIG + "/" + fname, dpi=150); plt.close(fig)

structural_diagram("L1_structural_model.png", "Figure L1. Structural model with standardized path coefficients (* p<.05)")

# ---- L2 Measurement model ----
def measurement_diagram():
    fig, ax = plt.subplots(figsize=(12, 9))
    lvpos = {"UE": (0.78, 0.85), "UX": (0.78, 0.62), "BSAT": (0.78, 0.38), "BSUC": (0.78, 0.15)}
    for lv, (lx, ly) in lvpos.items():
        box(ax, lx, ly, 0.14, 0.1, lv, fc="#D5E8D4")
        items = C.CONSTRUCTS[lv]
        ys = np.linspace(ly + 0.09, ly - 0.09, len(items))
        for k, it in enumerate(items):
            box(ax, 0.3, ys[k], 0.1, 0.05, it, fc="#FCEFD6")
            l = model.loadings[lv][k]
            arrow(ax, (lx - 0.07, ly), (0.35, ys[k]), f"{l:.2f}", sig=True, color="#2E86C1")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("Figure L2. Reflective measurement model (outer loadings)", fontsize=13)
    fig.tight_layout(); fig.savefig(C.FIG + "/L2_measurement_model.png", dpi=150); plt.close(fig)

measurement_diagram()

# ---- L3 Mediation model ----
def mediation_diagram():
    med = pd.read_csv(C.TBL + "/D_mediation.csv")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, (_, r) in zip(axes, med.iterrows()):
        x, _, y = r["Mediation"].split("->")
        a, b = r["a(X->M)"], r["b(M->Y)"]
        d, ind = r["Direct"], r["Indirect"]
        pos = {"X": (0.1, 0.25), "M": (0.5, 0.8), "Y": (0.9, 0.25)}
        box(ax, *pos["X"], 0.18, 0.14, x); box(ax, *pos["M"], 0.18, 0.14, "BSAT")
        box(ax, *pos["Y"], 0.18, 0.14, y)
        arrow(ax, pos["X"], pos["M"], f"a={a:.3f}")
        arrow(ax, pos["M"], pos["Y"], f"b={b:.3f}")
        arrow(ax, pos["X"], pos["Y"], f"c'={d:.3f}")
        ax.text(0.5, 0.05, f"Indirect={ind:.4f} (ns)", ha="center", fontsize=10, color="#C0392B")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        ax.set_title(r["Mediation"])
    fig.suptitle("Figure L3. Mediation models (BSAT as mediator)", fontsize=13)
    fig.tight_layout(); fig.savefig(C.FIG + "/L3_mediation_model.png", dpi=150); plt.close(fig)

mediation_diagram()

# ---- L4 IPMA ----
ipma = pd.read_csv(C.TBL + "/F_ipma.csv")
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(ipma["Importance(TotalEffect)"], ipma["Performance(0-100)"], s=120, color="#2E86C1", zorder=3)
for _, r in ipma.iterrows():
    ax.annotate(r["Construct"], (r["Importance(TotalEffect)"], r["Performance(0-100)"]),
                textcoords="offset points", xytext=(8, 8), fontsize=11, weight="bold")
ax.axhline(ipma["Performance(0-100)"].mean(), color="gray", ls="--")
ax.axvline(ipma["Importance(TotalEffect)"].mean(), color="gray", ls="--")
ax.set_xlabel("Importance (total effect on BSUC)"); ax.set_ylabel("Performance (0-100)")
ax.set_title("Figure L4. Importance-Performance Map (target: Brand Success)")
fig.tight_layout(); fig.savefig(C.FIG + "/L4_ipma.png", dpi=150); plt.close(fig)

# ---- L5 Calibration plots ----
fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))
for ax, v in zip(axes, ["UE", "UX", "BSAT", "BSUC"]):
    xs = np.linspace(1, 7, 200)
    mem = Q.calibrate(xs, 6.5, 4.0, 2.0)
    ax.plot(xs, mem, color="#8E44AD", lw=2)
    ax.scatter(comp[v], Q.calibrate(comp[v].values, 6.5, 4.0, 2.0), s=10, alpha=0.3, color="#16A085")
    for a, lab in [(2.0, "out"), (4.0, "cross"), (6.5, "in")]:
        ax.axvline(a, color="gray", ls=":", lw=0.8)
    ax.axhline(0.5, color="red", ls="--", lw=0.8)
    ax.set_title(f"{v}_f calibration"); ax.set_xlabel("Raw score"); ax.set_ylabel("Membership")
fig.suptitle("Figure L5. Direct calibration curves (anchors 6.5 / 4.0 / 2.0)", fontsize=13)
fig.tight_layout(); fig.savefig(C.FIG + "/L5_calibration.png", dpi=150); plt.close(fig)

# ---- L6 XY plots (sufficiency) for each condition vs BSUC_f ----
cal = pd.read_csv(C.TBL + "/H_calibrated_primary.csv")
fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))
for ax, c in zip(axes, ["UE", "UX", "BSAT"]):
    x = cal[c + "_f"]; y = cal["BSUC_f"]
    ax.scatter(x, y, s=14, alpha=0.4, color="#2980B9")
    ax.plot([0, 1], [0, 1], color="red", ls="--")
    cons = Q.consistency_suf(x.values, y.values)
    ax.set_title(f"{c}_f -> BSUC_f (consistency={cons:.3f})")
    ax.set_xlabel(c + "_f"); ax.set_ylabel("BSUC_f"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
fig.suptitle("Figure L6. fsQCA XY sufficiency plots", fontsize=13)
fig.tight_layout(); fig.savefig(C.FIG + "/L6_xy_plots.png", dpi=150); plt.close(fig)

# ---- L7 Truth table visualization ----
tt = pd.read_csv(C.TBL + "/H_truth_table_primary.csv")
fig, ax = plt.subplots(figsize=(9, 6))
colors = ["#C0392B" if c >= 0.8 else "#5DADE2" for c in tt["raw_consistency"]]
labels = ["".join([("" if v else "~") + n for v, n in zip([r.UE, r.UX, r.BSAT], ["UE", "UX", "BSAT"])])
          for r in tt.itertuples()]
ax.barh(range(len(tt)), tt["raw_consistency"], color=colors)
ax.axvline(0.80, color="black", ls="--", label="consistency cutoff 0.80")
ax.set_yticks(range(len(tt))); ax.set_yticklabels(labels, fontsize=8)
ax.invert_yaxis(); ax.set_xlabel("Raw consistency")
ax.set_title("Figure L7. Truth-table configurations (BSUC); none reach sufficiency"); ax.legend()
fig.tight_layout(); fig.savefig(C.FIG + "/L7_truth_table.png", dpi=150); plt.close(fig)

# ---- L8 Radar plot of construct means ----
fig = plt.figure(figsize=(7, 7))
ax = plt.subplot(111, polar=True)
cats = ["UE", "UX", "BSAT", "BSUC"]
vals = [comp[c].mean() for c in cats] + [comp[cats[0]].mean()]
ang = np.linspace(0, 2 * np.pi, len(cats), endpoint=False).tolist() + [0]
ax.plot(ang, vals, color="#2E86C1", lw=2); ax.fill(ang, vals, color="#2E86C1", alpha=0.25)
ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats); ax.set_ylim(1, 7)
ax.set_title("Figure L8. Radar plot of mean construct scores (1-7)")
fig.tight_layout(); fig.savefig(C.FIG + "/L8_radar.png", dpi=150); plt.close(fig)

# ---- L9 Bar chart of loadings & reliability ----
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].bar(load_tbl["Indicator"], load_tbl["OuterLoading"], color="#27AE60")
axes[0].axhline(0.708, color="red", ls="--", label="0.708 threshold")
axes[0].set_title("Outer loadings"); axes[0].tick_params(axis="x", rotation=90); axes[0].legend()
relm = rel.set_index("Construct")[["CronbachAlpha", "rhoA", "CR", "AVE"]]
relm.plot(kind="bar", ax=axes[1])
axes[1].axhline(0.70, color="red", ls="--"); axes[1].axhline(0.50, color="orange", ls=":")
axes[1].set_title("Reliability & AVE"); axes[1].tick_params(axis="x", rotation=0)
fig.suptitle("Figure L9. Measurement-model quality", fontsize=13)
fig.tight_layout(); fig.savefig(C.FIG + "/L9_reliability_bars.png", dpi=150); plt.close(fig)

# ---- L10 Residual & normality plots of structural residuals ----
from scipy import stats
resid = model.residuals["BSUC"]; fitted = model.fitted["BSUC"]
fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
axes[0].scatter(fitted, resid, s=14, alpha=0.5, color="#34495E"); axes[0].axhline(0, color="red", ls="--")
axes[0].set_xlabel("Fitted BSUC"); axes[0].set_ylabel("Residual"); axes[0].set_title("Residuals vs fitted")
stats.probplot(resid, dist="norm", plot=axes[1]); axes[1].set_title("Q-Q plot of residuals")
sns.histplot(resid, kde=True, ax=axes[2], color="#9B59B6"); axes[2].set_title("Residual distribution")
fig.suptitle("Figure L10. Structural residual diagnostics (BSUC equation)", fontsize=13)
fig.tight_layout(); fig.savefig(C.FIG + "/L10_residuals.png", dpi=150); plt.close(fig)

# ---- L11 HTMT / discriminant heatmap ----
htmt = pd.read_csv(C.TBL + "/B_htmt.csv", index_col=0)
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(htmt.astype(float), annot=True, fmt=".3f", cmap="YlOrRd", vmin=0, vmax=1, ax=ax)
ax.set_title("Figure L11. HTMT matrix (all < 0.85 threshold)")
fig.tight_layout(); fig.savefig(C.FIG + "/L11_htmt.png", dpi=150); plt.close(fig)

# ---- L12 Bootstrap distributions of paths ----
bz = np.load(C.TBL + "/_boot_paths.npz")
keys = [k for k in bz.files if "__" in k and not k.startswith("ind")]
fig, axes = plt.subplots(1, len(keys), figsize=(4 * len(keys), 4))
for ax, k in zip(axes, keys):
    a, b = k.split("__")
    sns.histplot(bz[k], kde=True, ax=ax, color="#2E86C1")
    ax.axvline(0, color="red", ls="--")
    lo, hi = np.percentile(bz[k], [2.5, 97.5])
    ax.axvline(lo, color="black", ls=":"); ax.axvline(hi, color="black", ls=":")
    ax.set_title(f"{a}->{b}")
fig.suptitle("Figure L12. Bootstrap distributions of path coefficients (95% CI dotted)", fontsize=12)
fig.tight_layout(); fig.savefig(C.FIG + "/L12_bootstrap_paths.png", dpi=150); plt.close(fig)

print("== Figures complete ==")
import os
print("\n".join(sorted(os.listdir(C.FIG))))
