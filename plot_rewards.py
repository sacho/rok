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
df['Power / KVK Contrib'] = df['Power'] / df['KVK Contrib']
df.sort_values(by='Power').to_csv('aaa.csv')

sm = df[df['Ranking'] < 800][['Governor ID', 'Name', 'Ranking', 'Power', 'KVK Contrib']]
sm1 = sm
sm2 = df[(df['Ranking'] < 800) & (df['Ranking'] > 300)][['Name', 'Power', 'KVK Contrib']]
sm = sm.sort_values(by='KVK Contrib', ascending=False)
# sm.to_csv('bbb.csv')

def get_fn(sm):
    x = sm['Power']
    y = sm['KVK Contrib']
    z = np.polyfit(x, y, 3)
    p = np.poly1d(z)
    return p

p1 = get_fn(sm)
p2 = get_fn(sm1)
print(p1)
print(p2)
print(p1(10000000))
power_scaler = sm[sm['Ranking'] == 300].iloc[0]['Power']
print(power_scaler)
sm['PS1'] = p1(sm['Power'])
sm['PS2'] = p2(sm['Power'])
sm.to_csv('eee.csv')
x = sm['Power'] / 1000000
y = sm['KVK Contrib'] / 1000000
c = np.where(sm['Power'] > 45000000, "yellow", "purple")
c1 = np.where(sm['Power'] > 45000000, "red", "blue")
z = np.polyfit(x, y, 3)
p = np.poly1d(z)
plt.title('Power/Score plot')
plt.xlabel('Power(mil)')
plt.ylabel('Score(mil)')
plt.ticklabel_format(useOffset=False, style='plain')
plt.scatter(x, y, c=c, alpha=0.8)
plt.plot(x, p(x), "b-")

plt.savefig('sm.png')
