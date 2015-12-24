#!/usr/bin/env python
import sys
import numpy as np
import pandas as pd
import dateutil.parser
import matplotlib.pyplot as plt

df = pd.read_csv('executions.csv', sep=' ')

mean_qty = df.groupby('account').apply(lambda group: group['qty'].mean()).sort_values()
print mean_qty

df = pd.read_csv('position.csv', sep=' ')

position = [row['position'] for i,row in df.iterrows() if row['account'] == 'mm']

plt.plot(position, label='mm position')
plt.show()

pnl = [row['pnl'] for i,row in df.iterrows() if row['account'] == 'mm']

plt.plot(pnl, label='mm pnl')
plt.show()

me = 'TMB48479412'

position = [row['position'] for i,row in df.iterrows() if row['account'] == me]

plt.plot(position, label='my position')
plt.show()

pnl = [row['pnl'] for i,row in df.iterrows() if row['account'] == me]

plt.plot(pnl, label='my pnl')
plt.show()
