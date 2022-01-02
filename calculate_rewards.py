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

df = pd.read_csv("C:\\Development\\rok\\rok\\2338_20211229_cleanup.csv", thousands=',', encoding='utf-8', dtype=col_types)

# Some data cleanup
str_cols = ['Name', 'ASCII Name', 'Governor ID', 'Alliance']
int_cols = ['Power', 'Total Kills', 'Kill Points', 'T1 Kills', 'T2 Kills', 'T3 Kills', 'T4 Kills', 'T5 Kills', 'RSS Assistance', 'Alliance Helps', 'Dead Troops']
for col in str_cols:
    df[col] = df[col].fillna('#N/A')
for col in int_cols:
    df[col] = df[col].fillna(0)

df = df.drop(df[df['Name'] == 'failsafe-triggered'].index)

# Data sanity
first_scan = df['Date'].min()
last_scan = df['Date'].max()
df.sort_values(['Governor ID', 'Date'], inplace=True)

# Calculate rewards

grouped_df = df.groupby('Governor ID')

contribs = {
    'T4 Kills' : 1,
    'T5 Kills' : 2,
    'Dead Troops' : 6,
    'RSS Assistance' : 0.004
}

df["KVK contrib"] = 0
for col, weight in contribs.items():
    df[f"{col} Contrib"] = grouped_df[col].transform(lambda x: (x.iloc[-1] - x.iloc[0]) * weight)
    df["KVK contrib"] += df[f"{col} Contrib"]

df.groupby('Governor ID').last().to_csv('contrib.csv')