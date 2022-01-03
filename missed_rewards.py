import pandas as pd
import numpy as np

col_types = {
    'Governor ID': 'string',
    'Gov Id': 'string',
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

df_good = df_good[['Date', 'Name', 'Governor ID', 'KVK contrib']].rename(columns={ 'Date' : 'Date_Good', 'KVK contrib': 'KVK contrib'}).sort_values(by=['KVK contrib'], ascending=False)
df_good['New Ranking'] = df_good.reset_index().index
df_bad = df_bad[['Gov Id', 'Formula']].sort_values(by=['Formula'], ascending=False)
df_bad['Old Ranking'] = df_bad.reset_index().index

df = df_good.merge(df_bad, left_on='Governor ID', right_on='Gov Id', how='outer').sort_values(by='Old Ranking')

df.to_csv('out.csv')