import pandas as pd
import numpy as np

col_types = {
    'Governor ID': 'string',
    'Gov Id': 'string',
    'Total Kills': 'int',
    'Kill Points': 'int',
    'T1 Kills':'int',
    'T2 Kills':'int',
    'T3 Kills':'int',
    'T4 Kills':'int',
    'T5 Kills':'int',
    'RSS Assistance':'int64',
    'Alliance Helps':'int',
    'Dead Troops':'int'
}

df_good = pd.read_csv("contrib.csv", thousands=',', encoding='utf-8', dtype=col_types)
df_bad = pd.read_csv("2338_circles.csv", thousands=",", encoding='utf-8', dtype=col_types)

df_good = df_good[['Date', 'Name', 'Governor ID', 'KVK Contrib']].rename(columns={ 'Date' : 'Date_Good', 'KVK Contrib': 'KVK Contrib'}).sort_values(by=['KVK Contrib'], ascending=False)
df_good['New Ranking'] = df_good.reset_index().index + 1
df_bad = df_bad[['Gov Id', 'Formula']].sort_values(by=['Formula'], ascending=False)
df_bad['Old Ranking'] = df_bad.reset_index().index + 1

df = df_good.merge(df_bad, left_on='Governor ID', right_on='Gov Id', how='outer').sort_values(by='Old Ranking')
df['Old Ranking'] = df['Old Ranking'].fillna(9999)
df['New Ranking'] = df['New Ranking'].fillna(9999)
df = df.astype({'Old Ranking': 'int', 'New Ranking': 'int'})

df[['Governor ID', 'Name', 'KVK Contrib', 'Formula', 'Old Ranking', 'New Ranking']].to_csv('out.csv')