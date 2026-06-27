import pandas as pd, numpy as np
from scipy import stats
from plssem import PLSSEM
pd.set_option('display.width', 220); pd.set_option('display.max_columns', 100)

df = pd.read_excel("MTVS.xlsx", sheet_name="Sheet1")
measurement = {
    "UE":["UE1","UE2","UE3","UE4","UE5"],"UX":["UX1","UX2","UX3","UX4","UX5"],
    "BSAT":["BSAT1","BSAT2","BSAT3","BSAT4"],"BSUC":["BSUC1","BSUC2","BSUC3","BSUC4"]}
structural = {"BSAT":["UE","UX"], "BSUC":["UE","UX","BSAT"]}

base = PLSSEM(df, measurement, structural).fit()
orig_w = {c: base.weights[c].copy() for c in measurement}

# direct path point estimates
direct = {("UE","BSAT"):base.paths["BSAT"]["UE"], ("UX","BSAT"):base.paths["BSAT"]["UX"],
          ("BSAT","BSUC"):base.paths["BSUC"]["BSAT"], ("UE","BSUC"):base.paths["BSUC"]["UE"],
          ("UX","BSUC"):base.paths["BSUC"]["UX"]}
ind = {"UE": base.paths["BSAT"]["UE"]*base.paths["BSUC"]["BSAT"],
       "UX": base.paths["BSAT"]["UX"]*base.paths["BSUC"]["BSAT"]}

# ---- Bootstrap ----
B = 5000
rng = np.random.default_rng(20240627)
n = len(df)
keys = list(direct.keys())
boot_direct = {k: np.empty(B) for k in keys}
boot_ind = {"UE": np.empty(B), "UX": np.empty(B)}
boot_r2 = {"BSAT": np.empty(B), "BSUC": np.empty(B)}

for b in range(B):
    idx = rng.integers(0, n, n)
    s = df.iloc[idx].reset_index(drop=True)
    try:
        m = PLSSEM(s, measurement, structural, max_iter=300).fit()
    except Exception:
        for k in keys: boot_direct[k][b]=np.nan
        boot_ind["UE"][b]=np.nan; boot_ind["UX"][b]=np.nan
        boot_r2["BSAT"][b]=np.nan; boot_r2["BSUC"][b]=np.nan
        continue
    # sign alignment per construct vs original weights
    sign = {}
    for c in measurement:
        d = np.dot(m.weights[c], orig_w[c])
        sign[c] = 1.0 if d >= 0 else -1.0
    def adj(a,bb,endo):
        return m.paths[endo][a]*sign[a]*sign[endo]
    boot_direct[("UE","BSAT")][b]=adj("UE","BSAT","BSAT")
    boot_direct[("UX","BSAT")][b]=adj("UX","BSAT","BSAT")
    boot_direct[("BSAT","BSUC")][b]=adj("BSAT","BSUC","BSUC")
    boot_direct[("UE","BSUC")][b]=adj("UE","BSUC","BSUC")
    boot_direct[("UX","BSUC")][b]=adj("UX","BSUC","BSUC")
    boot_ind["UE"][b]=adj("UE","BSAT","BSAT")*adj("BSAT","BSUC","BSUC")
    boot_ind["UX"][b]=adj("UX","BSAT","BSAT")*adj("BSAT","BSUC","BSUC")
    boot_r2["BSAT"][b]=m.r2["BSAT"]; boot_r2["BSUC"][b]=m.r2["BSUC"]

def summ(est, arr):
    arr=arr[~np.isnan(arr)]
    se=arr.std(ddof=1)
    t=est/se if se>0 else np.nan
    p=2*(1-stats.t.cdf(abs(t), df=n-1))
    lo,hi=np.percentile(arr,[2.5,97.5])
    return se,t,p,lo,hi

print("="*90)
print("STRUCTURAL MODEL - DIRECT EFFECTS (bootstrap, B=%d)"%B)
print("="*90)
print(f"{'Path':16s}{'beta':>9s}{'SE':>9s}{'t':>9s}{'p':>10s}{'CI2.5':>9s}{'CI97.5':>9s}{'sig':>6s}")
hyp_map={("UE","BSAT"):"H1a",("UX","BSAT"):"H1b",("BSAT","BSUC"):"H2",("UE","BSUC"):"H3a",("UX","BSUC"):"H3b"}
for k in keys:
    se,t,p,lo,hi=summ(direct[k], boot_direct[k])
    sig = "yes" if (lo>0 or hi<0) else "no"
    print(f"{hyp_map[k]} {k[0]}->{k[1]:6s}{direct[k]:9.4f}{se:9.4f}{t:9.3f}{p:10.4f}{lo:9.4f}{hi:9.4f}{sig:>6s}")

print("\n"+"="*90)
print("INDIRECT (MEDIATION) EFFECTS")
print("="*90)
for k in ["UE","UX"]:
    se,t,p,lo,hi=summ(ind[k], boot_ind[k])
    sig = "yes" if (lo>0 or hi<0) else "no"
    lbl = f"{k}->BSAT->BSUC"
    print(f"H4 {lbl:18s} est={ind[k]:8.4f} SE={se:.4f} t={t:.3f} p={p:.4f} CI[{lo:.4f},{hi:.4f}] sig={sig}")

print("\nR2 (bootstrap mean / CI):")
for k in ["BSAT","BSUC"]:
    arr=boot_r2[k][~np.isnan(boot_r2[k])]
    print(f"  {k}: point={base.r2[k]:.4f} adj={base.r2_adj[k]:.4f} bootmean={arr.mean():.4f} CI[{np.percentile(arr,2.5):.4f},{np.percentile(arr,97.5):.4f}]")

# ---- Controls model: ATT_1, ATT_2 -> BSUC (single-indicator) ----
print("\n"+"="*90)
print("CONTROL VARIABLES (ATT_1, ATT_2 -> BSUC), OLS on composite scores")
print("="*90)
sc = base.scores.copy()
sc["ATT_1"]=(df["ATT_1"]-df["ATT_1"].mean())/df["ATT_1"].std(ddof=1)
sc["ATT_2"]=(df["ATT_2"]-df["ATT_2"].mean())/df["ATT_2"].std(ddof=1)
import numpy as np
Xc=sc[["UE","UX","BSAT","ATT_1","ATT_2"]].values
Xc=np.column_stack([np.ones(n),Xc])
y=sc["BSUC"].values
beta,_,_,_=np.linalg.lstsq(Xc,y,rcond=None)
yhat=Xc@beta; resid=y-yhat
sigma2=(resid@resid)/(n-Xc.shape[1])
covb=sigma2*np.linalg.inv(Xc.T@Xc)
se=np.sqrt(np.diag(covb)); tvals=beta/se
pvals=2*(1-stats.t.cdf(np.abs(tvals),df=n-Xc.shape[1]))
names=["const","UE","UX","BSAT","ATT_1","ATT_2"]
for nme,b_,s_,t_,p_ in zip(names,beta,se,tvals,pvals):
    print(f"  {nme:6s} b={b_:8.4f} SE={s_:.4f} t={t_:7.3f} p={p_:.4f}")
ss_res=resid@resid; ss_tot=((y-y.mean())**2).sum()
print(f"  R2 with controls = {1-ss_res/ss_tot:.4f}")

np.savez("boot_results.npz",
    direct={f"{k[0]}->{k[1]}":direct[k] for k in keys},
    allow_pickle=True)
print("\nDone.")
