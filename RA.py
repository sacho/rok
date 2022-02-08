import pandas as pd
import numpy as np

col_types = {
    'Governor ID': 'string',
    'Total Kills': 'int64',
    'Kill Points': 'int64',
    'T1 Kills':'int64',
    'T2 Kills':'int64',
    'T3 Kills':'int64',
    'T4 Kills':'int64',
    'T5 Kills':'int64',
    'RSS Assistance':'int64',
    'Alliance Helps':'int64',
    'Dead Troops':'int64'
}

df = pd.read_csv("2338_newest_sanitized.csv", thousands=',', encoding='utf-8', dtype=col_types)

# Some data cleanup
str_cols = ['Name', 'ASCII Name', 'Governor ID', 'Alliance']
int_cols = ['Power', 'Total Kills', 'Kill Points', 'T1 Kills', 'T2 Kills', 'T3 Kills', 'T4 Kills', 'T5 Kills', 'RSS Assistance', 'Alliance Helps', 'Dead Troops']
for col in str_cols:
    df[col] = df[col].fillna('#N/A')
for col in int_cols:
    df[col] = df[col].fillna(0)

df = df.drop(df[df['Name'] == 'failsafe-triggered'].index)

df = df.groupby(by='Governor ID').apply(lambda x: x.iloc[0])[['Name', 'Governor ID', 'Alliance', 'Power']].to_csv('alliances.csv', index=False)
