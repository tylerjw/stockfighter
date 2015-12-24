#!/usr/bin/env python
import sys
import numpy as np
import pandas as pd
import dateutil.parser
import matplotlib.pyplot as plt

df = pd.read_csv('executions.csv', sep=' ')


taking_prob = df.groupby('account').apply(lambda group: group['taking'].mean()).sort_values()
active = taking_prob[(taking_prob != 0) & (taking_prob != 1)]
gap = active.iloc[1] - active.iloc[0]
rest = active.iloc[-1] - active.iloc[1]

print active

suspicion1 = active.index[0]
print 'Suspicious account from % taking:', suspicion1


largest_trades = df[df.taking].sort_values('qty').tail(10)
print largest_trades[['time', 'account', 'qty', 'price']].to_string()

large_trade_counts = largest_trades.account.value_counts()
suspicion2 = large_trade_counts.index[0]

print 'Suspicious account from trade sizes:', suspicion2
if suspicion1 != suspicion2:
    print >> sys.stderr, "Suspicions don't match"
    sys.exit()


df['tradeqty'] = np.where(df.bors == 'buy', df.qty, -df.qty)
df['ts'] = df['time'].map(dateutil.parser.parse)
suspicious = df.account == suspicion1

plt.plot(df.loc[suspicious, 'ts'], df.loc[suspicious, 'tradeqty'].cumsum())
plt.show()

plt.plot(df.price / 100.)
plt.show()
