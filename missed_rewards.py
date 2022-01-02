import pandas as pd
import numpy as np

col_types = {
    'Governor ID': 'string',
    'Total Kills': 'float',
    'Kill Points': 'float',
    'T1 Kills':'float',
    'T2 Kills':'float',
    'T3 Kills':'float',
    'T4 Kills':'float',
    'T5 Kills':'float',
    'RSS Assistance':'float',
    'Alliance Helps':'float',
    'Dead Troops':'float'
}

df_good = pd.read_csv("contrib.csv", thousands=',', encoding='utf-8', dtype=col_types)
df_bad = pd.read_csv("2338_circles.csv", thousands=",", encoding='utf-8', dtype=col_types)

df_good = df_good[['Date', 'Name', 'Governor ID', 'KVK contrib']].rename(columns={ 'Date' : 'Date_Good', 'KVK contrib': 'KVK contrib Good'})
df_bad = df_bad[['Gov Id', 'Formula']].rename(columns={ 'Gov Id' : 'Governor ID'})

df = df_good.merge(df_bad, on='Governor ID', how='outer')

df.to_csv('out.csv')