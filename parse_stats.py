import pandas as pd

col_types = {
    'Governor ID': 'string',
    'Total Kills': 'int',
    'Kill Points': 'int',
    'T1 Kills':pd.Int64Dtype,
    'T2 Kills':pd.Int64Dtype,
    'T3 Kills':pd.Int64Dtype,
    'T4 Kills':pd.Int64Dtype,
    'T5 Kills':pd.Int64Dtype,
    'RSS Assistance':pd.Int64Dtype,
    'Alliance Helps':pd.Int64Dtype,
    'Dead Troops':pd.Int64Dtype
}
df = pd.read_csv("2338_20211229.csv", thousands=',', encoding='utf-8', dtype=col_types, chunksize=10)
for i, chunk in enumerate(df):
    print(f"{i} chunk OK")

# df = pd.read_csv('2338_20211229.csv', thousands=',', encoding='utf-8', dtype=col_types)
# df.sort_values(['Governor ID', 'Date'], inplace=True)
# df['KP Diff'] = df.groupby(['Governor ID'])['Kill Points'].diff().fillna(0)
# df.to_csv('out.csv')