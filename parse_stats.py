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

df = pd.read_csv("2338_newest_cleanup.csv", thousands=',', encoding='utf-8', dtype=col_types)

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
df[(df[non_zero_cols] == 0).any(axis=1)].to_csv('zeroes.csv')

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

df.groupby('Governor ID').last().to_csv('contrib.csv')

print(df[(df['Date'] == '2021-12-01') & (df["Power"] > 0)]["Power"].min())