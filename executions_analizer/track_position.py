#!/usr/bin/env python
import json
import stockfighter as sf
import autobahn.twisted.websocket as ws

exchange = 'CQNEX'
symbol = 'ELT'
account = 'JB76422300'


def get_protocol(account):
    class AccountSnooper(ws.WebSocketClientProtocol):
        def onConnect(self, response):
            self.cash = 0
            self.position = 0
            print("Server connected: {0}".format(response.peer))

        def onOpen(self):
            print("WebSocket connection open.")

        def onMessage(self, payload, isBinary):
            text = payload.decode('utf8')

            result = json.loads(text)
            assert result['ok'], result

            # print 'Trade:', result

            if result['order']['direction'] == 'buy':
                self.cash -= result['price'] * result['filled']
                self.position += result['filled']
            else:
                self.cash += result['price'] * result['filled']
                self.position -= result['filled']

            if self.position > 250:
                # emergency correction
                print "EMERGENCY SELL!"
                sf.place_order(account, exchange, symbol, 0, 50, 'sell', 'market')
            if self.position < -250:
                # emergency correction
                print "EMERGENCY BUY!"
                sf.place_order(account, exchange, symbol, 0, 50, 'buy', 'market')

            print 'account={}, position={}, pnl={:.2f}'.format(result['account'], self.position, (self.cash + self.position * result['price']) / 100.)

        def onClose(self, wasClean, code, reason):
            print("WebSocket connection closed: {} {}".format(account, reason))
            reactor.callLater(1, watch_account, account)

    return AccountSnooper


def watch_account(account):
    url = u'wss://api.stockfighter.io/ob/api/ws/{}/venues/{}/executions'.format(account, exchange)
    factory = ws.WebSocketClientFactory(url, debug=False)
    factory.protocol = get_protocol(account)

    print url

    contextFactory = ssl.ClientContextFactory()

    ws.connectWS(factory, contextFactory)


accounts = set()
def check_order(order_id):
    global accounts

    account = sf.get_order_account(exchange, symbol, order_id)
    print 'account:', account

    if account not in accounts:
        print account
        watch_account(account)
        accounts.add(account)

    reactor.callLater(1, check_order, order_id + 1)


if __name__ == '__main__':
    import sys

    from twisted.python import log
    from twisted.internet import reactor, ssl

    log.startLogging(sys.stdout)

    watch_account(account)

    # reactor.callLater(1, check_order, 1)
    reactor.run()
