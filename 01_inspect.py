import pandas as pd
import numpy as np

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 100)

xls = pd.ExcelFile("MTVS.xlsx")
print("Sheet names:", xls.sheet_names)
df = pd.read_excel("MTVS.xlsx", sheet_name=xls.sheet_names[0])
print("\nShape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nDtypes:\n", df.dtypes)
print("\nHead:\n", df.head())
print("\nMissing per column:\n", df.isna().sum())
print("\nTotal missing:", df.isna().sum().sum())
print("\nDescribe:\n", df.describe().T)
