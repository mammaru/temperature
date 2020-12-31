import codecs
from datetime import datetime, timedelta
import json
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def load_csv_jma():
    df_orig = pd.read_csv("data/1900-2020_daily_high.csv", skiprows=[0,1,2,4], encoding="shift_jis")
    #df_orig = pd.read_csv("data/1900-2020_daily_low.csv", skiprows=[0,1,2,4,5], encoding="shift_jis")
    #df_orig = pd.read_csv("data/1900-2020_daily_mean.csv", skiprows=[0,1,2,4], encoding="shift_jis")
    # create data
    df = pd.DataFrame()
    for index, row in df_orig.iterrows():
        try:
            r = str(int(row[0]))
            c = str(int(row[1])) + "/" + str(int(row[2]))
            t = row[3]
            if not (c in df.columns):
                df[c] = np.nan
            if not (r in df.index):
                df.loc[r] = np.nan
            df.at[r, c] = t
        except:
            pass
    df = df.fillna(df.mean())
    t_mean = float(df_orig.iloc[:, [3]].mean())
    t_min = float(df_orig.iloc[:, [3]].min())
    t_max = float(df_orig.iloc[:, [3]].max())
    return {"df":df, "mean":t_mean, "min":t_min, "max":t_max}

def load_json_tk():
    df_orig = pd.read_json("data/temperature.json")
    df_orig.index = range(1876, 2019, 1)
    date_list = [datetime(2020, 6, 1) + timedelta(days=i) for i in range(122)]
    df_orig.columns = [d.strftime("%m/%d") for d in date_list]
    def is_number(s):
        try:
            float(s)
            return s
        except:
            return np.nan
    df = df_orig.applymap(is_number)
    df = df.fillna(df.mean())
    t_mean = float(df.mean().mean())
    t_min = float(df.min(numeric_only=True).min())
    t_max = float(df.max(numeric_only=True).max())
    return {"df":df, "mean":t_mean, "min":t_min, "max":t_max}    

def write_json(d):
    json.dump({"table":d["df"].values.tolist(),
               "years":d["df"].index.tolist(),
               "dates":d["df"].columns.tolist(),
               "mean":d["mean"],
               "min":d["min"],
               "max":d["max"]},
              codecs.open("data/data.json", 'w', encoding='utf-8'),
              sort_keys=False,
              indent=2)
    

if __name__ == "__main__":
    d = load_csv_jma()
    #d = load_json_tk()
    df = d["df"] 
    t_mean = d["mean"]
    t_min = d["min"]
    t_max = d["max"]
    #json.dump(df.values.tolist(), codecs.open("data/data.json", 'w', encoding='utf-8'), sort_keys=False, indent=2)
    write_json(d)
    print("head:", df.head(5))
    print("mean:", t_mean, " min:", t_min, " max:", t_max)
    
    # visualize
    plt.figure(figsize=(20, 16))

    #sns.heatmap(df, cmap="bwr", vmax=t_max, vmin=t_min, center=t_mean, linewidth=0)
    #sns.heatmap(df, cmap="RdBu_r", vmax=t_max, vmin=t_min, center=t_mean, linewidth=0)
    #sns.heatmap(df, cmap="nipy_spectral", vmax=t_max, vmin=t_min, center=t_mean, linewidth=0)
    sns.heatmap(df, cmap="jet", vmax=t_max, vmin=t_min, center=t_mean, linewidth=0)

    #cmap = sns.diverging_palette(250, 10, n=20)
    #cmap = sns.hls_palette(20, h=.66, l=0.5, s=1)
    #sns.heatmap(df, cmap=cmap, vmax=t_max, vmin=t_min, center=t_mean, linewidth=0)

    myColors = ((0.0, 0.0, 1.0, 1.0),
                (0.1, 0.1, 0.9, 1.0),
                (0.2, 0.2, 0.8, 1.0),
                (0.3, 0.3, 0.7, 1.0),
                (0.4, 0.4, 0.6, 1.0),
                (0.5, 0.5, 0.5, 1.0),
                (0.6, 0.4, 0.4, 1.0),
                (0.7, 0.3, 0.3, 1.0),
                (0.8, 0.2, 0.2, 1.0),
                (0.9, 0.1, 0.1, 1.0),
                (1.0, 0.0, 0.0, 1.0))
    #cmap = LinearSegmentedColormap.from_list('Custom', myColors, len(myColors))
    #sns.heatmap(df, cmap=cmap, vmax=t_max, vmin=t_min, center=t_mean, linewidth=0)
    #sns.heatmap(df, cmap=cmap, linewidth=0)

    plt.savefig('img/heatmap.png')