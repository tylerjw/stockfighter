from stockfighter import Stockfighter as Fighter
from stockfighter import GM
import matplotlib.pyplot as plt
import math as m
import random
from position import Position
import time as t
from book import Book
import pprint as pp

exchange = 'CQNEX'
symbol = 'ELT'
account = 'JB76422300'
key = '52d0445bb4e4a5e4f7672d3701e55cef1bacc7e1'


def fill_math(fills):
    items = 0
    total = 0
    for fill in fills:
        items += fill['qty']
        total += fill['qty'] * fill['price']

    avg = total / items
    return [items, total, avg]

def test():
    sf = Fighter(exchange, account, key)
    pos = Position()

    quote = sf.symbol_quote(symbol)
    last = int(quote['last'])
    transaction_size = 10
    order = sf.place_new_order(symbol, last, transaction_size, 'sell', 'limit')
    if order['ok'] == False:
        print order

    order_id = order['id']
    order_open = True
    fullfilled = 0
    while order_open:
        status = sf.status_for_order(order_id, symbol)
        order_open = status['open']
        fill = status['totalFilled']
        if fill != fullfilled:
            fullfilled = fill
            print "total filled = {}".format(fullfilled)

    status = sf.status_for_order(order_id, symbol)
    [items, total, avg] = fill_math(status['fills'])
    pos.sell(items, total)
    quote = sf.symbol_quote(symbol)
    last = int(quote['last'])
    pos.print_pos(last)

def monitor_book():
    sf = Fighter(exchange, account, key)

    spreads = []

    for idx in range(200):
        print idx
        book = Book(sf.orderbook_for_stock(symbol))
        print book.totals()
        spread = book.spread()
        if(spread > 0):
            spreads.append(spread)

        t.sleep(0.1)

    plt.plot(spreads)
    plt.show()

def sell_slide_book_smart():
    sf = Fighter(exchange, account, key)

    timeout = 2
    bid_max = 50
    bid_min = 30

    while True:
        book_json = sf.orderbook_for_stock(symbol)
        book = Book(book_json)
        center = book.center()
        if book.total_asks() == 0 or book.total_bids() == 0:
            continue # try again

        spread = int(book.spread() * 0.6)
        print book.totals()
        order_price = int(center - spread/2)
        sell_price = int(center + spread/2)
        bid_size = bid_max
        print bid_size
        print "Order Price: ${:.2f}".format(order_price/100.0)
        print "Sell Price: ${:.2f}".format(sell_price/100.0)
        order = sf.place_new_order(symbol, order_price, bid_size, 'buy', 'limit')
        sell = sf.place_new_order(symbol, sell_price, bid_size, 'sell', 'limit')

        # bid_size = bid_max
        # print bid_size
        # spread = int(spread / 2)
        # order_price = int(center - spread/2)
        # sell_price = int(center + spread/2)
        # print "Order Price: ${:.2f}".format(order_price/100.0)
        # print "Sell Price: ${:.2f}".format(sell_price/100.0)
        # order2 = sf.place_new_order(symbol, order_price, bid_size, 'buy', 'limit')
        # sell2 = sf.place_new_order(symbol, sell_price, bid_size, 'sell', 'limit')

        # bid_size = random.randrange(bid_min,bid_max,2)
        # print bid_size
        # spread = int(spread / 2)
        # order_price = int(center - spread/2)
        # sell_price = int(center + spread/2)
        # print "Order Price: ${:.2f}".format(order_price/100.0)
        # print "Sell Price: ${:.2f}".format(sell_price/100.0)
        # order3 = sf.place_new_order(symbol, order_price, bid_size, 'buy', 'limit')
        # sell3 = sf.place_new_order(symbol, sell_price, bid_size, 'sell', 'limit')

        # bid_size = random.randrange(bid_min,bid_max,2)
        # print bid_size
        # spread = int(spread / 2)
        # order_price = int(center - spread/2)
        # sell_price = int(center + spread/2)
        # print "Order Price: ${:.2f}".format(order_price/100.0)
        # print "Sell Price: ${:.2f}".format(sell_price/100.0)
        # order4 = sf.place_new_order(symbol, order_price, bid_size, 'buy', 'limit')
        # sell4 = sf.place_new_order(symbol, sell_price, bid_size, 'sell', 'limit')

        # bid_size = random.randrange(bid_min,bid_max,2)
        # print bid_size
        # spread = int(spread / 2)
        # order_price = int(center - spread/2)
        # sell_price = int(center + spread/2)
        # print "Order Price: ${:.2f}".format(order_price/100.0)
        # print "Sell Price: ${:.2f}".format(sell_price/100.0)
        # order5 = sf.place_new_order(symbol, order_price, bid_size, 'buy', 'limit')
        # sell5 = sf.place_new_order(symbol, sell_price, bid_size, 'sell', 'limit')

        if order['ok'] == False:
            print "ORDER ERROR!"
            print order
            break

        if sell['ok'] == False:
            print "SELL ERROR!"
            print sell
            break

        bought = wait_for_order(sf, symbol,order['id'],timeout)
        sold = wait_for_order(sf, symbol,sell['id'],timeout)

        # bought2 = wait_for_order(sf, symbol,order2['id'],timeout)
        # sold2 = wait_for_order(sf, symbol,sell2['id'],timeout)

        # bought3 = wait_for_order(sf, symbol,order3['id'],timeout)
        # sold3 = wait_for_order(sf, symbol,sell3['id'],timeout)

        # bought4 = wait_for_order(sf, symbol,order4['id'],timeout)
        # sold4 = wait_for_order(sf, symbol,sell4['id'],timeout)

        # bought5 = wait_for_order(sf, symbol,order5['id'],timeout)
        # sold5 = wait_for_order(sf, symbol,sell5['id'],timeout)

def update_pos(sf, pos, symbol, order_id):
    status = sf.status_for_order(order_id, symbol)
    [items, total, avg] = fill_math(status['fills'])
    if status['direction'] == 'buy':
        pos.buy(items, total)
    else:
        pos.sell(items, total)

def wait_for_order(sf, symbol, order_id, timeout):
    order_open = True
    start_time = t.clock()
    while order_open:
        status = sf.status_for_order(order_id, symbol)
        order_open = status['open']
        if order_open:
            time_now = t.clock()
            if ((t.clock() - start_time) > timeout):
                # sf.cancel_order(order_id, symbol)
                # print 'caneled order: {}'.format(order_id)
                order_open = False
        else:
            t.sleep(0.1)

    status = sf.status_for_order(order_id, symbol)
    n_fullfilled = status['totalFilled']
    return n_fullfilled

def sell_slide():
    sf = Fighter(exchange, account, key)
    pos = Position()

    spread = 15
    transaction_size = 100
    share_limit = 150
    recovery_step = 30

    while True:
        # if lowest_last > target_price:
        #     lowest_last = target_price
        #     print "adjusted to target price of {}".format(target_price)
        quote = sf.symbol_quote(symbol)
        last = int(quote['last'])
        print "price = {}".format(last)
        order = sf.place_new_order(symbol, last, transaction_size, 'buy', 'limit')
        sell = sf.place_new_order(symbol, last+spread, transaction_size, 'sell', 'limit')

        if pos.get_position() > share_limit:
            # sell some
            print "recovery sell"
            recovery = sf.place_new_order(symbol, 0, recovery_step, 'sell', 'market')
            recovery_open = True
            while recovery_open:
                status = sf.status_for_order(symbol, recovery['id'])
                recovery_open = status['open']
            status = sf.status_for_order(symbol, recovery['id'])
            [items, total, avg] = fill_math(status['fills'])
            pos.sell(items, total)

        if pos.get_position() < -1*share_limit:
            # buy some
            print "recovery buy"
            recovery = sf.place_new_order(symbol, 0, recovery_step, 'buy', 'market')
            recovery_open = True
            while recovery_open:
                status = sf.status_for_order(symbol, recovery['id'])
                recovery_open = status['open']
            status = sf.status_for_order(symbol, recovery['id'])
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
            status = sf.status_for_order(order_id, symbol)
            order_open = status['open']
            fill = status['totalFilled']
            if fill != fullfilled:
                fullfilled = fill
                print "total ordered = {}".format(fullfilled)
            quote = sf.symbol_quote(symbol)
            new_last = int(quote['last'])
            if(new_last < (last - spread) or
                (t.clock() - start_time) > timeout):
                sf.cancel_order(order_id, symbol)
                order_open = False
                # stoping the order and sell for a better price

        #wait for sell to close
        while sell_open:
            status = sf.status_for_order(symbol, sell_id)
            sell_open = status['open']
            quote = sf.symbol_quote(symbol)
            new_last = int(quote['last'])
            if(new_last > (last + 2*spread) or
                (t.clock() - start_time) > timeout):
                sf.cancel_order(symbol, sell_id)
                sell_open = False
                # stoping the order and sell for a better price

        status = sf.status_for_order(order_id, symbol)
        [items, total, avg] = fill_math(status['fills'])
        pos.buy(items, total)

        status = sf.status_for_order(symbol, sell_id)
        [items, total, avg] = fill_math(status['fills'])
        pos.sell(items, total)

        quote = sf.symbol_quote(symbol)
        last = int(quote['last'])
        pos.print_pos(last)

def main():
    sell_slide_book_smart()

if __name__ == '__main__':
    main()
