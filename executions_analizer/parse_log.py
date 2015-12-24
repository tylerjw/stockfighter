#!/usr/bin/env python
import re
import sys

print 'time account qty price bors taking incomingId standingId'

for line in sys.stdin:
    match = re.search('Trade: (.+)', line)
    if match:
        trade = eval(match.group(1))

        print trade['filledAt'], trade['account'], trade['filled'], trade['price'], trade['order']['direction'], trade['order']['id'] == trade['incomingId'], trade['incomingId'], trade['standingId']
