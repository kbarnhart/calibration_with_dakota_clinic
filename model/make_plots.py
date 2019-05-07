import pandas as pd
import glob
from plotnine import *

files = glob.glob("*.dat")
dfs = []
for file in files:
    df = pd.read_csv(file, engine="python", sep="\s+")
    df["method"] = file.split('.')[0].split("_")[-1]
    dfs.append(df)

df = pd.concat(dfs)
#%%
    
p = (ggplot(df, aes(x="T", y="duration_years", fill="rmse", color="rmse")) + 
     geom_point() + 
     facet_wrap("~method"))
print(p)