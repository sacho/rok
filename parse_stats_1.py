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

df = pd.read_csv("2338_imperium_1.csv", thousands=',', encoding='utf-8', dtype=col_types)

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
zr.to_csv('zeroes.csv')

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

bs = grouped_df.first()
bs.to_csv('bbs.csv')
bbs = bs[(bs['KP By Kills'] != bs['Kill Points']) | (bs['Dead Troops'] == 0) | (bs['RSS Assistance'] == 0)]
bbs.to_csv('bbs_bad.csv')


# Calculate rewards

contribs = {
    'T4 Kills' : 1,
    'T5 Kills' : 2,
}

df["KVK Contrib"] = 0
df["Kills Contrib"] = 0
for col, weight in contribs.items():
    df[f"{col} Contrib"] = grouped_df[col].transform(lambda x: (x.iloc[-1] - x.iloc[0]) * weight)
    df["Kills Contrib"] += df[f"{col} Contrib"]

kills = ['T1 Kills', 'T2 Kills', 'T3 Kills', 'T4 Kills', 'T5 Kills']
df['Total Kills'] = 0
for col in kills:
    df['Total Kills'] += grouped_df[col].transform(lambda x: (x.iloc[-1] - x.iloc[0]))
df[f"Deads Contrib"] = grouped_df['Dead Troops'].transform(lambda x: (x.iloc[-1] - x.iloc[0]) * 6)
df[f"RSS Contrib"] = grouped_df['RSS Assistance'].transform(lambda x: min(1000000000, (x.iloc[-1] - x.iloc[0])) * 0.004)
df[f"PreKVK Power"] = grouped_df['Power'].transform(lambda x: x.iloc[0])
df[f"Fighting Contrib"] = df["Kills Contrib"] + df["Deads Contrib"]
df["KVK Contrib"] = df["Fighting Contrib"] + df[["Fighting Contrib", "RSS Contrib"]].min(axis=1)


banned = pd.read_csv('banned_ids.csv', thousands=',', encoding='utf-8', dtype=col_types)
contrib = df[~df['Governor ID'].isin(banned['Governor ID'])].groupby('Governor ID').last().sort_values(by='KVK Contrib', ascending=False)
contrib['Ranking'] = contrib.reset_index().index.astype('int') + 1
contrib[['Name', 'Date', 'Ranking', 'KVK Contrib', 'Kills Contrib', 'Deads Contrib', 'RSS Contrib']].to_csv('contrib.csv', index=False)
contrib[['Name', 'Date', 'Ranking', 'KVK Contrib', 'Kills Contrib', 'Deads Contrib', 'RSS Contrib', 'Power', 'PreKVK Power', 'Total Kills']].sort_values(by='PreKVK Power', ascending=False).to_csv('contrib_1.csv', index=False)

# print(df[(df['Date'] == '2021-12-01') & (df["Power"] > 0)]["Power"].min())