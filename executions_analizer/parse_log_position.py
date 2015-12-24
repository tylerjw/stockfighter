#!/usr/bin/env python
import re
import sys

print 'account position pnl'

for line in sys.stdin:
    match = re.search('account=([\-\w]+), position=(-?\d+), pnl=(-?[\d\.]+)', line)
    if match:
        account = match.group(1)
        position = match.group(2)
        pnl = match.group(3)

        print account, position, pnl
