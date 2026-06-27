import pandas as pd, numpy as np
from itertools import combinations, product
pd.set_option('display.width', 220); pd.set_option('display.max_columns', 100)

df = pd.read_csv("data_with_composites.csv")
comp = {"UE":"UE_comp","UX":"UX_comp","BSAT":"BSAT_comp","BSUC":"BSUC_comp"}

# ---------- Direct calibration (Ragin) ----------
# anchors on 7-point scale: full-in=6.0, crossover=4.0, full-out=2.0
def calibrate(x, full_in=6.0, cross=4.0, full_out=2.0):
    x = np.asarray(x, float)
    # log-odds target at thresholds (fsQCA uses 0.953 ~ ln(19)=2.944)
    LA = np.log(0.95/0.05)
    dev = x - cross
    out = np.empty_like(x)
    up = x >= cross
    s_up = LA/(full_in - cross)
    s_dn = LA/(cross - full_out)
    z = np.where(up, dev*s_up, dev*s_dn)
    m = np.exp(z)/(1+np.exp(z))
    # cap exact extremes
    m = np.clip(m, 0.0001, 0.9999)
    return m

fz = {}
for k,c in comp.items():
    fz[k] = calibrate(df[c].values)
F = pd.DataFrame(fz)
print("CALIBRATION SUMMARY (fuzzy membership) anchors 6/4/2")
print(F.describe(percentiles=[.25,.5,.75]).round(3).T[["mean","min","25%","50%","75%","max"]])
print("\nRaw composite anchors check: full-in>=6, crossover=4, full-out<=2")

# ---------- Necessity analysis ----------
def consistency_nec(cond, outcome):  # necessity
    return np.sum(np.minimum(cond, outcome))/np.sum(outcome)
def coverage_nec(cond, outcome):
    return np.sum(np.minimum(cond, outcome))/np.sum(cond)

Y = F["BSUC"].values
notY = 1-Y
print("\n"+"="*70)
print("NECESSARY CONDITION ANALYSIS for HIGH BSUC (threshold consistency>=0.90)")
print("="*70)
print(f"{'Condition':14s}{'Consistency':>13s}{'Coverage':>11s}")
for k in ["UE","UX","BSAT"]:
    for sign,lab in [(F[k].values,k),(1-F[k].values,"~"+k)]:
        print(f"{lab:14s}{consistency_nec(sign,Y):13.3f}{coverage_nec(sign,Y):11.3f}")

# ---------- Sufficiency: truth table for UE,UX,BSAT -> BSUC ----------
conds = ["UE","UX","BSAT"]
fzc = {k: F[k].values for k in conds}
n = len(df)
# membership in each corner = min over conditions of (m if 1 else 1-m)
rows=[]
for combo in product([1,0], repeat=3):   # 1=present,0=absent
    mem = np.ones(n)
    for c,present in zip(conds, combo):
        mem = np.minimum(mem, fzc[c] if present else 1-fzc[c])
    # cases best classified here = mem>0.5
    incol = mem>0.5
    freq = int(incol.sum())
    # sufficiency consistency: sum(min(mem,Y))/sum(mem)
    cons = np.sum(np.minimum(mem,Y))/np.sum(mem) if np.sum(mem)>0 else np.nan
    rows.append({"UE":combo[0],"UX":combo[1],"BSAT":combo[2],"n":freq,
                 "raw_consist":round(cons,3)})
tt=pd.DataFrame(rows).sort_values("n",ascending=False).reset_index(drop=True)
print("\n"+"="*70)
print("TRUTH TABLE  (conditions UE,UX,BSAT -> BSUC).  freq thr=3, consistency thr=0.80")
print("="*70)
print(tt.to_string(index=False))

passed = tt[(tt["n"]>=3)&(tt["raw_consist"]>=0.80)]
print(f"\nRows meeting BOTH thresholds (freq>=3 & consistency>=0.80): {len(passed)}")
print(passed.to_string(index=False) if len(passed) else "  -> NONE")

# ---------- Sufficiency consistency of single & combined high conditions ----------
print("\n"+"="*70)
print("SUFFICIENCY of selected configurations for HIGH BSUC")
print("="*70)
def suf(cond):
    return np.sum(np.minimum(cond,Y))/np.sum(cond), np.sum(np.minimum(cond,Y))/np.sum(Y)
tests={
 "UE":fzc["UE"], "UX":fzc["UX"], "BSAT":fzc["BSAT"],
 "UE*UX":np.minimum(fzc["UE"],fzc["UX"]),
 "UE*BSAT":np.minimum(fzc["UE"],fzc["BSAT"]),
 "UX*BSAT":np.minimum(fzc["UX"],fzc["BSAT"]),
 "UE*UX*BSAT":np.minimum.reduce([fzc["UE"],fzc["UX"],fzc["BSAT"]]),
}
print(f"{'Config':14s}{'Consistency':>13s}{'Coverage':>11s}")
for k,v in tests.items():
    cs,cv=suf(v)
    print(f"{k:14s}{cs:13.3f}{cv:11.3f}")

# Also test for ~BSUC (negated outcome) to be thorough
print("\nSufficiency for NEGATED outcome ~BSUC (any config consistent?):")
for k,v in tests.items():
    cs=np.sum(np.minimum(v,notY))/np.sum(v)
    print(f"  {k:14s} consistency(~BSUC)={cs:.3f}")

F.to_csv("fuzzy_scores.csv", index=False)
print("\nSaved fuzzy_scores.csv")
