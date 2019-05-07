import pandas as pd
from pandas.api.types import CategoricalDtype
import glob
import numpy as np
from plotnine import *

files = glob.glob("*.dat")
dfs = []
for file in files:
    df = pd.read_csv(file, engine="python", sep="\s+")
    df["method"] = file.split('.')[0].split("_")[-1]
    dfs.append(df)
#%%
df = pd.concat(dfs, ignore_index=True)
method_cats = CategoricalDtype(categories=["grid", 
                                           "nl2sol", 
                                           "ego"], 
                               ordered=True)
df["method"] = df["method"].astype(method_cats)
df = df.set_index(["method", "T", "duration_years"]).drop(columns=["%eval_id", "interface"])

# plot evaluations
p = (ggplot(df.reset_index(), aes(x="T", y="duration_years", fill="rmse", color="rmse")) + 
     geom_point() + 
     facet_wrap("~method"))
print(p)
#%%
# see how results and number of evaluations are influenced by method
sum_df = df.groupby("method").agg([np.count_nonzero, np.min])
sum_df.columns = sum_df.columns.map('|'.join).str.strip('|')

p = (ggplot(sum_df.reset_index(), (aes(x="rmse|count_nonzero", y="rmse|amin", color="method"))) + geom_point())
print(p)

#%%
# summarized best Ts and durations
best_df=df[df.rmse.isin(sum_df["rmse|amin"].values)].reset_index()
print(best_df)