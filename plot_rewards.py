import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

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

df = pd.read_csv("contrib_1.csv", thousands=',', encoding='utf-8', dtype=col_types)
df['Power / KVK Contrib'] = df['PreKVK Power'] / df['KVK Contrib']
df.sort_values(by='Power').to_csv('aaa.csv')

sm = df[df['Ranking'] < 800][['Governor ID', 'Name', 'Ranking', 'Power','PreKVK Power', 'KVK Contrib']]
sm = sm.sort_values(by='PreKVK Power', ascending=False)
# sm.to_csv('bbb.csv')

def get_fn(sm):
    x = sm['PreKVK Power']
    y = sm['KVK Contrib']
    z = np.polyfit(x, y, 3)
    p = np.poly1d(z)
    return p

p1 = get_fn(sm)
print(p1)
sm['PowerForScaling'] = (sm['PreKVK Power'] + sm['Power']) / 2
sm = sm.sort_values(by='PowerForScaling', ascending=False)
power_scaler = sm.iloc[300]['PowerForScaling']
print(power_scaler)
print(p1(power_scaler))
print(p1(20000000))
sm['PS1'] = p1(sm['PreKVK Power'])
scaler_effectiveness = 0.25
sm['Scaler'] = (p1(power_scaler) / p1(sm['PowerForScaling'].apply(lambda x: max(25000000, x))))
sm['Scaler_LowPower'] = (sm['Scaler'] - 1) * scaler_effectiveness + 1
sm['Scaled Score'] = sm['KVK Contrib'] * sm['Scaler_LowPower']
df['Scaler_LowPower'] = sm.iloc[300:]['Scaler_LowPower']
df['Scaled Score'] = sm.iloc[300:]['Scaled Score']
df['Scaled Score'] = df[['Scaled Score', 'KVK Contrib']].max(axis=1)
df[['Governor ID', 'Name', 'Ranking', 'Power', 'PreKVK Power', 'KVK Contrib', 'Scaler_LowPower', 'Scaled Score']].sort_values(by='Scaled Score', ascending=False).to_csv('ddd.csv')
#sm.iloc[300:][['Governor ID', 'Name', 'Ranking', 'PreKVK Power', 'KVK Contrib', 'Scaler_LowPower', 'Scaled Score']].to_csv('eee.csv')
x = sm['PreKVK Power'] / 1000000
y = sm['KVK Contrib'] / 1000000
c = np.where(sm['PreKVK Power'] > 45000000, "yellow", "purple")
c1 = np.where(sm['PreKVK Power'] > 45000000, "red", "blue")
z = np.polyfit(x, y, 3)
p = np.poly1d(z)
plt.title('Power/Score plot')
plt.xlabel('Power(mil)')
plt.ylabel('Score(mil)')
plt.ticklabel_format(useOffset=False, style='plain')
plt.scatter(x, y, c=c, alpha=0.8)
plt.plot(x, p(x), "b-")

plt.savefig('sm.png')
