from fighter import Fighter
from stockfighter import GM
import matplotlib.pyplot as plt
import math as m
import random

venue = 'SDCBEX'
stock = 'CAH'
account = 'PLB830907'
key = '7f92e11fedbc270b2de73399633d9d78c1d569d4'

def start():
    gm = GM(key)
    gm.start('chock_a_block')

def main():
    sf = Fighter(venue, account, key)

    print sf.venue_stocks()
    book = sf.orderbook_for_stock(stock)

    last_price = []

    quote = sf.stock_quote(stock)
    lowest_last = int(quote['last'])

    print lowest_last

    purchased = 0 # current state
    target = 100000 # small target

    # target_price = 9765

    sf.place_new_order(stock, 0, 100000, 'buy', 'market')

    # while purchased < target:
    #     # if lowest_last > target_price:
    #     #     lowest_last = target_price
    #     #     print "adjusted to target price of {}".format(target_price)

    #     buy_amount = random.randrange(1000,5000,2)
    #     print "buy_amount = {}".format(buy_amount)
    #     print "price = {}".format(lowest_last)
    #     order = sf.place_new_order(stock, lowest_last, buy_amount, 'buy', 'limit')
    #     # sf.place_new_order(stock, lowest_last+500, buy_amount, 'sell', 'limit')
    #     # for sells in range(100):
    #     #     sf.place_new_order(stock, lowest_last-100, 1, 'sell', 'limit')

    #     if order['ok'] == False:
    #         print order
    #         break
    #     order_id = order['id']
    #     order_open = True

    #     new_low = 0
    #     fullfilled = 0

    #     #wait for order to close
    #     while order_open:
    #         quote = sf.stock_quote(stock)
    #         if 'last' in quote.keys():
    #             price = quote['last']
    #             last_price.append(price)
    #             if new_low == 0:
    #                 new_low = price
    #             if price < new_low:
    #                 new_low = price

    #         status = sf.status_for_order(stock, order_id)
    #         order_open = status['open']
    #         fill = status['totalFilled']
    #         if fill != fullfilled:
    #             fullfilled = fill
    #             print "total filled = {}".format(fullfilled)

    #     lowest_last = int(new_low * 0.999)
    #     purchased += buy_amount

    # plt.plot(last_price)
    # plt.ylabel('last')
    # plt.show()

if __name__ == '__main__':
    main()
