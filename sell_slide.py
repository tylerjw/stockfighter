from fighter import Fighter
from stockfighter import GM
import matplotlib.pyplot as plt
import math as m
import random
from position import Position
import time as t
from book import Book

venue = 'YSUBEX'
stock = 'KDI'
account = 'RTB82567211'
key = '7f92e11fedbc270b2de73399633d9d78c1d569d4'


def fill_math(fills):
    items = 0
    total = 0
    for fill in fills:
        items += fill['qty']
        total += fill['qty'] * fill['price']

    avg = total / items
    return [items, total, avg]

def test():
    sf = Fighter(venue, account, key)
    pos = Position()

    quote = sf.stock_quote(stock)
    last = int(quote['last'])
    transaction_size = 10
    order = sf.place_new_order(stock, last, transaction_size, 'sell', 'limit')
    if order['ok'] == False:
        print order

    order_id = order['id']
    order_open = True
    fullfilled = 0
    while order_open:
        status = sf.status_for_order(stock, order_id)
        order_open = status['open']
        fill = status['totalFilled']
        if fill != fullfilled:
            fullfilled = fill
            print "total filled = {}".format(fullfilled)

    status = sf.status_for_order(stock, order_id)
    [items, total, avg] = fill_math(status['fills'])
    pos.sell(items, total)
    quote = sf.stock_quote(stock)
    last = int(quote['last'])
    pos.print_pos(last)

def monitor_book():
    sf = Fighter(venue, account, key)

    while True:
        book = Book(sf.orderbook_for_stock(stock))
        print book.ascii()
        print book.totals()
        book.plot_group()

        t.sleep(0.1)

def sell_slide():
    sf = Fighter(venue, account, key)
    pos = Position()

    spread = 15
    transaction_size = 100
    share_limit = 150
    recovery_step = 30

    while True:
        # if lowest_last > target_price:
        #     lowest_last = target_price
        #     print "adjusted to target price of {}".format(target_price)
        quote = sf.stock_quote(stock)
        last = int(quote['last'])
        print "price = {}".format(last)
        order = sf.place_new_order(stock, last, transaction_size, 'buy', 'limit')
        sell = sf.place_new_order(stock, last+spread, transaction_size, 'sell', 'limit')

        if pos.get_position() > share_limit:
            # sell some
            print "recovery sell"
            recovery = sf.place_new_order(stock, 0, recovery_step, 'sell', 'market')
            recovery_open = True
            while recovery_open:
                status = sf.status_for_order(stock, recovery['id'])
                recovery_open = status['open']
            status = sf.status_for_order(stock, recovery['id'])
            [items, total, avg] = fill_math(status['fills'])
            pos.sell(items, total)

        if pos.get_position() < -1*share_limit:
            # buy some
            print "recovery buy"
            recovery = sf.place_new_order(stock, 0, recovery_step, 'buy', 'market')
            recovery_open = True
            while recovery_open:
                status = sf.status_for_order(stock, recovery['id'])
                recovery_open = status['open']
            status = sf.status_for_order(stock, recovery['id'])
            [items, total, avg] = fill_math(status['fills'])
            pos.buy(items, total)

        if order['ok'] == False:
            print "ORDER ERROR!"
            print order
            break
        order_id = order['id']
        order_open = True

        if sell['ok'] == False:
            print "SELL ERROR!"
            print sell
            break
        sell_id = sell['id']
        sell_open = True

        fullfilled = 0
        timeout = 15 # seconds

        start_time = t.clock()

        #wait for order to close
        while order_open:
            status = sf.status_for_order(stock, order_id)
            order_open = status['open']
            fill = status['totalFilled']
            if fill != fullfilled:
                fullfilled = fill
                print "total ordered = {}".format(fullfilled)
            quote = sf.stock_quote(stock)
            new_last = int(quote['last'])
            if(new_last < (last - spread) or
                (t.clock() - start_time) > timeout):
                sf.cancel_order(stock, order_id)
                order_open = False
                # stoping the order and sell for a better price

        #wait for sell to close
        while sell_open:
            status = sf.status_for_order(stock, sell_id)
            sell_open = status['open']
            quote = sf.stock_quote(stock)
            new_last = int(quote['last'])
            if(new_last > (last + 2*spread) or
                (t.clock() - start_time) > timeout):
                sf.cancel_order(stock, sell_id)
                sell_open = False
                # stoping the order and sell for a better price

        status = sf.status_for_order(stock, order_id)
        [items, total, avg] = fill_math(status['fills'])
        pos.buy(items, total)

        status = sf.status_for_order(stock, sell_id)
        [items, total, avg] = fill_math(status['fills'])
        pos.sell(items, total)

        quote = sf.stock_quote(stock)
        last = int(quote['last'])
        pos.print_pos(last)

def main():
    monitor_book()

if __name__ == '__main__':
    main()
