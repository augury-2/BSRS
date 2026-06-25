"""PART A - Data screening. Saves tables to analysis/tables and figures to analysis/figures."""
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import common as C

sns.set_theme(style="whitegrid", context="paper")
df = C.load_raw()
X = df[C.INDICATORS].astype(float)
N = len(df)

# ---- 1-3 sample, missing, duplicates ----
summary = {
    "Sample size (N)": N,
    "Number of indicators": len(C.INDICATORS),
    "Total cells": N * len(C.INDICATORS),
    "Missing values": int(X.isna().sum().sum()),
    "Missing (%)": round(100 * X.isna().sum().sum() / (N * len(C.INDICATORS)), 4),
    "Full-row duplicates": int(df.duplicated().sum()),
    "Indicator-pattern duplicates": int(X.duplicated().sum()),
    "Scale min": int(X.min().min()),
    "Scale max": int(X.max().max()),
}
pd.Series(summary).to_csv(C.TBL + "/A_sample_overview.csv")

# ---- 4 outliers: Mahalanobis ----
Xv = X.values
mu = Xv.mean(axis=0)
cov = np.cov(Xv, rowvar=False)
inv = np.linalg.pinv(cov)
diff = Xv - mu
md = np.einsum("ij,jk,ik->i", diff, inv, diff)
p = Xv.shape[1]
md_p = 1 - stats.chi2.cdf(md, df=p)
crit = stats.chi2.ppf(0.999, df=p)
mahal = pd.DataFrame({"ID": df["ID"], "MahalanobisD2": md, "p_value": md_p,
                      "Outlier_p<.001": md > crit})
mahal_out = mahal[mahal["Outlier_p<.001"]].sort_values("MahalanobisD2", ascending=False)
mahal.to_csv(C.TBL + "/A_mahalanobis.csv", index=False)

# Cook's distance: regress BSUC composite on UE,UX,BSAT composites
comp = C.composites(df)
import statsmodels.api as sm
Xc = sm.add_constant(comp[["UE", "UX", "BSAT"]])
ols = sm.OLS(comp["BSUC"], Xc).fit()
infl = ols.get_influence()
cooks = infl.cooks_distance[0]
cook_thr = 4 / N
cookdf = pd.DataFrame({"ID": df["ID"], "CooksD": cooks, "Influential_4/N": cooks > cook_thr})
cookdf.to_csv(C.TBL + "/A_cooks_distance.csv", index=False)

# ---- 5 normality / descriptives ----
desc_rows = []
for col in C.INDICATORS + C.CONTROLS:
    s = df[col].astype(float)
    sh_w, sh_p = stats.shapiro(s)
    desc_rows.append([col, s.mean(), s.std(ddof=1), s.median(), s.min(), s.max(),
                      stats.skew(s), stats.kurtosis(s, fisher=True), sh_w, sh_p])
desc = pd.DataFrame(desc_rows, columns=["Indicator", "Mean", "SD", "Median", "Min", "Max",
                                        "Skewness", "Kurtosis", "ShapiroW", "Shapiro_p"])
desc.round(4).to_csv(C.TBL + "/A_descriptives.csv", index=False)

# ---- 11 construct descriptives ----
cdesc = comp.describe().T[["mean", "std", "min", "max"]]
cdesc["skew"] = comp.skew()
cdesc["kurtosis"] = comp.kurtosis()
cdesc.round(4).to_csv(C.TBL + "/A_construct_descriptives.csv")

# ---- 12 correlation, 13 covariance ----
corr = X.corr()
corr.round(4).to_csv(C.TBL + "/A_correlation_matrix.csv")
X.cov().round(4).to_csv(C.TBL + "/A_covariance_matrix.csv")
comp.corr().round(4).to_csv(C.TBL + "/A_construct_correlation.csv")

# ---- 14-15 VIF / multicollinearity (indicator level + construct level) ----
from statsmodels.stats.outliers_influence import variance_inflation_factor
Xz = sm.add_constant(X)
vif_ind = pd.DataFrame({"Indicator": X.columns,
                        "VIF": [variance_inflation_factor(Xz.values, i + 1) for i in range(X.shape[1])]})
vif_ind.round(4).to_csv(C.TBL + "/A_vif_indicators.csv", index=False)

compz = sm.add_constant(comp)
vif_c = pd.DataFrame({"Construct": comp.columns,
                      "VIF": [variance_inflation_factor(compz.values, i + 1) for i in range(comp.shape[1])]})
vif_c.round(4).to_csv(C.TBL + "/A_vif_constructs.csv", index=False)

# ============ FIGURES ============
# Histograms
fig, axes = plt.subplots(4, 5, figsize=(18, 12))
for ax, col in zip(axes.flat, C.INDICATORS):
    ax.hist(df[col], bins=7, color="#4C72B0", edgecolor="white")
    ax.set_title(col, fontsize=10)
for ax in axes.flat[len(C.INDICATORS):]:
    ax.axis("off")
fig.suptitle("Figure A1. Histograms of all indicators", fontsize=14)
fig.tight_layout(); fig.savefig(C.FIG + "/A1_histograms.png", dpi=150); plt.close(fig)

# Density plots
fig, axes = plt.subplots(4, 5, figsize=(18, 12))
for ax, col in zip(axes.flat, C.INDICATORS):
    sns.kdeplot(df[col], ax=ax, fill=True, color="#55A868")
    ax.set_title(col, fontsize=10)
for ax in axes.flat[len(C.INDICATORS):]:
    ax.axis("off")
fig.suptitle("Figure A2. Density plots of all indicators", fontsize=14)
fig.tight_layout(); fig.savefig(C.FIG + "/A2_density.png", dpi=150); plt.close(fig)

# Q-Q plots
fig, axes = plt.subplots(4, 5, figsize=(18, 12))
for ax, col in zip(axes.flat, C.INDICATORS):
    stats.probplot(df[col], dist="norm", plot=ax)
    ax.set_title(col, fontsize=10)
for ax in axes.flat[len(C.INDICATORS):]:
    ax.axis("off")
fig.suptitle("Figure A3. Normal Q-Q plots of all indicators", fontsize=14)
fig.tight_layout(); fig.savefig(C.FIG + "/A3_qqplots.png", dpi=150); plt.close(fig)

# Correlation heatmap (indicators)
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr, annot=False, cmap="RdBu_r", center=0, vmin=-1, vmax=1, square=True, ax=ax)
ax.set_title("Figure A4. Correlation heatmap of indicators", fontsize=14)
fig.tight_layout(); fig.savefig(C.FIG + "/A4_corr_heatmap.png", dpi=150); plt.close(fig)

# Construct correlation heatmap
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(comp.corr(), annot=True, fmt=".3f", cmap="RdBu_r", center=0, vmin=-1, vmax=1, square=True, ax=ax)
ax.set_title("Figure A5. Construct correlation heatmap", fontsize=12)
fig.tight_layout(); fig.savefig(C.FIG + "/A5_construct_corr_heatmap.png", dpi=150); plt.close(fig)

# Scatter matrix of constructs
g = sns.pairplot(comp, diag_kind="kde", plot_kws=dict(s=12, alpha=0.4, color="#4C72B0"))
g.fig.suptitle("Figure A6. Scatter matrix of construct scores", y=1.02, fontsize=14)
g.fig.savefig(C.FIG + "/A6_scatter_matrix.png", dpi=150, bbox_inches="tight"); plt.close(g.fig)

# Boxplots
fig, ax = plt.subplots(figsize=(16, 6))
df[C.INDICATORS].boxplot(ax=ax)
ax.set_title("Figure A7. Boxplots of indicators (outlier screening)", fontsize=14)
fig.tight_layout(); fig.savefig(C.FIG + "/A7_boxplots.png", dpi=150); plt.close(fig)

# Mahalanobis plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(range(N), md, c=np.where(md > crit, "red", "#4C72B0"), s=18)
ax.axhline(crit, color="red", ls="--", label=f"chi2(.999, df={p})={crit:.1f}")
ax.set_xlabel("Case index"); ax.set_ylabel("Mahalanobis D2")
ax.set_title("Figure A8. Mahalanobis distance (multivariate outliers)"); ax.legend()
fig.tight_layout(); fig.savefig(C.FIG + "/A8_mahalanobis.png", dpi=150); plt.close(fig)

# Cook's distance plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.stem(range(N), cooks, markerfmt=" ", basefmt=" ")
ax.axhline(cook_thr, color="red", ls="--", label=f"4/N={cook_thr:.4f}")
ax.set_xlabel("Case index"); ax.set_ylabel("Cook's D")
ax.set_title("Figure A9. Cook's distance (BSUC regression)"); ax.legend()
fig.tight_layout(); fig.savefig(C.FIG + "/A9_cooks.png", dpi=150); plt.close(fig)

print("== PART A done ==")
print(pd.Series(summary).to_string())
print("\nMahalanobis outliers (p<.001):", len(mahal_out))
print("Cook's influential (>4/N):", int((cooks > cook_thr).sum()))
print("\nSkew range: %.3f to %.3f" % (desc.Skewness.min(), desc.Skewness.max()))
print("Kurtosis range: %.3f to %.3f" % (desc.Kurtosis.min(), desc.Kurtosis.max()))
print("Max indicator VIF: %.3f" % vif_ind.VIF.max())
print("Max construct VIF: %.3f" % vif_c.VIF.max())
print("Construct corr:\n", comp.corr().round(3).to_string())
