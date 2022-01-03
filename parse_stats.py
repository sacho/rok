import pandas as pd
import numpy as np

col_types = {
    'Governor ID': 'string',
    'Total Kills': 'int',
    'Kill Points': 'int',
    'T1 Kills':'int',
    'T2 Kills':'int',
    'T3 Kills':'int',
    'T4 Kills':'int',
    'T5 Kills':'int',
    'RSS Assistance':'int',
    'Alliance Helps':'int',
    'Dead Troops':'int'
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

# Data sanity
first_scan = df['Date'].min()
last_scan = df['Date'].max()
df.sort_values(['Governor ID', 'Date'], inplace=True)

kill_columns = ['T1 Kills', 'T2 Kills', 'T3 Kills', 'T4 Kills', 'T5 Kills']
kill_weights = [1/5, 2, 4, 10, 20]


df['KP By Kills'] = np.floor(df[kill_columns] * kill_weights).sum(axis=1)

df[df['KP By Kills'] != df['Kill Points']].to_csv("kp_mismatch.csv")

non_zero_cols = ['Kill Points', 'RSS Assistance', 'Dead Troops', 'T5 Kills', 'T4 Kills']
zr = df[(df[non_zero_cols] == 0).any(axis=1)]
zr[(zr['Date'] == first_scan) | (zr['Date'] == last_scan)].to_csv('zeroes.csv')

growing_cols = ['Kill Points'] + kill_columns + ['RSS Assistance', 'Dead Troops']
diff_cols = [f"{x}_diff" for x in growing_cols]
grouped_df = df.groupby(['Governor ID'])
for col in growing_cols:
    df[f"{col}_diff"] = grouped_df[col].diff().fillna(0)
br = df.loc[(df[diff_cols] < 0).any(axis=1)]
br.to_csv('diff_mismatch.csv')
br_imp = br[(br['Date'] == first_scan) | (br['Date'] == last_scan)]
br_imp.to_csv('diff_mismatch_important.csv')

# No real pre-kvk stats. A lot of people only have stats from z4 opening so we'll have to fudge them a little bit..

no_baseline_stats = grouped_df.filter(lambda g: (g['Date'] > '2021-12-09').all()).drop_duplicates(subset=['Governor ID'])
no_baseline_stats.to_csv('no_baseline_stats.csv')

# Bad baseline stats

bbs = grouped_df.first()
bbs.to_csv('bbs.csv')
pd.concat([bbs[bbs['KP By Kills'] != bbs['Kill Points']]]).to_csv('bbs_bad.csv')


# Calculate rewards

contribs = {
    'T4 Kills' : 1,
    'T5 Kills' : 2,
    'Dead Troops' : 6
}

df["KVK contrib"] = 0
for col, weight in contribs.items():
    df[f"{col} Contrib"] = grouped_df[col].transform(lambda x: (x.iloc[-1] - x.iloc[0]) * weight)
    df["KVK contrib"] += df[f"{col} Contrib"]
df[f"RSS Contrib"] = grouped_df['RSS Assistance'].transform(lambda x: (x.iloc[-1] - x.iloc[0]) * weight)
df["KVK contrib + RSS"] += df[f"RSS Contrib"]

contrib = df.groupby('Governor ID').last().sort_values(by='KVK contrib')
contrib['Ranking'] = contrib.reset_index().index
contrib[['Governor ID', 'Name', 'Date', 'KVK contrib', 'RSS Contrib', 'KVK contrib + RSS']].to_csv('contrib.csv')

# print(df[(df['Date'] == '2021-12-01') & (df["Power"] > 0)]["Power"].min())