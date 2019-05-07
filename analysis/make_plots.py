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

df = pd.concat(dfs, ignore_index=True)
method_cats = CategoricalDtype(categories=["grid", 
                                           "nl2sol", 
                                           "ego"], 
                               ordered=True)
df["method"] = df["method"].astype(method_cats)
df = df.set_index(["method", "T", "duration_years"]).drop(columns=["interface"])

# plot evaluations
p = (ggplot(df.reset_index(), aes(x="T", y="duration_years", color="%eval_id")) + 
     geom_point() + 
     scale_color_cmap(name='jet') +
     facet_wrap("~method"))
p.save(dpi=300, filename="plot_eval_id.png")

p = (ggplot(df.reset_index(), aes(x="T", y="duration_years", color="rmse")) + 
     geom_point() + 
     facet_wrap("~method"))
p.save(dpi=300, filename="plot_rmse.png")
#%%
# see how results and number of evaluations are influenced by method
sum_df = df.drop(columns=["%eval_id"]).groupby("method").agg([np.count_nonzero, np.min])
sum_df.columns = sum_df.columns.map('|'.join).str.strip('|')

p = (ggplot(sum_df.reset_index(), (aes(x="rmse|count_nonzero", y="rmse|amin", color="method"))) + geom_point())
p.save(dpi=300, filename="plot_summary.png")

#%%
# summarized best Ts and durations
best_df=df[df.rmse.isin(sum_df["rmse|amin"].values)].reset_index()
best_df.to_csv("summary.txt", sep="\t")