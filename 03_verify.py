import pandas as pd, numpy as np
pd.set_option('display.width', 260); pd.set_option('display.max_columns', 100)
df = pd.read_excel("MTVS.xlsx", sheet_name="Sheet1")
blocks = {"UE":["UE1","UE2","UE3","UE4","UE5"],"UX":["UX1","UX2","UX3","UX4","UX5"],
          "BSAT":["BSAT1","BSAT2","BSAT3","BSAT4"],"BSUC":["BSUC1","BSUC2","BSUC3","BSUC4"]}
items=[i for v in blocks.values() for i in v]
C=df[items].corr()
print("FULL ITEM CORRELATION MATRIX")
print(C.round(2).to_string())

print("\nMean |corr| WITHIN vs BETWEEN blocks:")
for a in blocks:
    wi=C.loc[blocks[a],blocks[a]].values
    iu=np.triu_indices(len(blocks[a]),1)
    print(f"  within {a}: {np.abs(wi[iu]).mean():.3f}")
import itertools
for a,b in itertools.combinations(blocks,2):
    sub=C.loc[blocks[a],blocks[b]].values
    print(f"  between {a}-{b}: {np.abs(sub).mean():.3f}")
