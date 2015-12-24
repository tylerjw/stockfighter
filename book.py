from stockfighter import Stockfighter
import pprint as pp
import matplotlib.pyplot as plt
import numpy as np

class Book(object):
	def __init__(self, book):
		self.book = book
		self.venue = book['venue']
		self.ok = book['ok']
		self.asks = book['asks']
		self.bids = book['bids']

	def pprint(self):
		pp.pprint(self.book)

	def ascii(self):
		outstr = '{b:>10}  \t{p:<10}\t{s:<10}\n'.format(
				b = '',
				p = 'Price',
				s = 'Ask Size'
				)
		if self.asks != None:
			for ask in self.asks:
				outstr += '{b:>10}  \t${p:<10.2f}\t{s:<10}\n'.format(
					b = '',
					p = ask['price']/100.0,
					s = ask['qty']
					)
		outstr += '--------------------------------------\n'
		if self.bids != None:
			for bid in self.bids:
				outstr += '{b:>10}  \t${p:<10.2f}\t{s:<10}\n'.format(
					b = bid['qty'],
					p = bid['price']/100.0,
					s = ''
					)
		outstr += '{b:>10}  \t{p:10}\t{s:<10}\n'.format(
			b = 'Bid Size',
			p = 'Price',
			s = ''
			)
		return outstr

	def ascii_group(self):
		outstr = '{b:>10}  \t{p:<10}\t{s:<10}\n'.format(
				b = '',
				p = 'Price',
				s = 'Ask Size'
				)

		if self.asks != None:
			size = 0
			price = 0
			for ask in self.asks:
				if price == 0:
					price = ask['price']
					size = ask['qty']
				elif ask['price'] == price:
					size += ask['qty']
				else:
					outstr += '{b:>10}  \t${p:<10.2f}\t{s:<10}\n'.format(
						b = '',
						p = price/100,
						s = size
						)
					price = ask['price']
					size = ask['qty']
			if size != 0:
				outstr += '{b:>10}  \t${p:<10.2f}\t{s:<10}\n'.format(
					b = '',
					p = price/100,
					s = size
					)

		outstr += '--------------------------------------\n'
		if self.bids != None:
			size = 0
			price = 0
			for bid in self.bids:
				if price == 0:
					price = bid['price']
					size = bid['qty']
				elif bid['price'] == price:
					size += bid['qty']
				else:
					outstr += '{b:>10}  \t${p:<10.2f}\t{s:<10}\n'.format(
						b = size,
						p = price/100.0,
						s = ''
						)
					price = bid['price']
					size = bid['qty']
			if size != 0:
				outstr += '{b:>10}  \t${p:<10.2f}\t{s:<10}\n'.format(
					b = size,
					p = price/100.0,
					s = ''
					)

		outstr += '{b:>10}  \t{p:10}\t{s:<10}\n'.format(
			b = 'Bid Size',
			p = 'Price',
			s = ''
			)
		return outstr

	def minimum_ask(self):
		min_ask = -1.0
		if self.asks != None:
			for ask in self.asks:
				if min_ask == -1.0:
					min_ask = ask['price']
				elif min_ask < ask['price']:
					min_ask = ask['price']
		return min_ask

	def maximum_bid(self):
		max_bid = -1.0
		if self.bids != None:
			for bid in self.bids:
				if max_bid == -1.0:
					max_bid = bid['price']
				elif max_bid > bid['price']:
					max_bid = bid['price']
		return max_bid

	def maximum_ask(self):
		max_ask = -1.0
		if self.asks != None:
			for ask in self.asks:
				if max_ask == -1.0:
					max_ask = ask['price']
				elif max_ask > ask['price']:
					max_ask = ask['price']
		return max_ask

	def minimum_bid(self):
		min_bid = -1.0
		if self.bids != None:
			for bid in self.bids:
				if min_bid == -1.0:
					min_bid = bid['price']
				elif min_bid > bid['price']:
					min_bid = bid['price']
		return min_bid

	def total_asks(self):
		total = 0
		if self.asks != None:
			for ask in self.asks:
				total += ask['qty']
		return total

	def total_bids(self):
		total = 0
		if self.bids != None:
			for bid in self.bids:
				total += bid['qty']
		return total

	def spread(self):
		return self.minimum_ask() - self.maximum_bid()

	def center(self):
		return self.maximum_bid() + self.spread()/2

	def totals(self):
		outstr = 'Total Asks: {}\n'.format(self.total_asks())
		outstr += 'Total Bids: {}\n'.format(self.total_bids()) 
		outstr += 'Minimum Ask: ${:.2f}\n'.format(self.minimum_ask()/100.0)
		outstr += 'Maximum Bid: ${:.2f}\n'.format(self.maximum_bid()/100.0)
		outstr += 'Spread: ${:.2f}\n'.format(self.spread()/100.0)
		outstr += 'Center: ${:.2f}\n'.format(self.center()/100.0)

		return outstr

	def plot_group(self):
		points = []
		if self.asks != None:
			for ask in self.asks:
				points.append([ask['price']/100.0, ask['qty']])
		if self.bids != None:
			for bid in self.bids:
				points.append([bid['price']/100.0, -1 * bid['qty']])

		xs = list(set([p[0] for p in points]))
		ys = [sum([p[1] for p in points if p[0] == x]) for x in xs]
		plt.stem(xs,ys, '-.')
		plt.show()

	def plot(self):
		points = []
		if self.asks != None:
			for ask in self.asks:
				points.append([ask['price']/100.0, ask['qty']])
		if self.bids != None:
			for bid in self.bids:
				points.append([bid['price']/100.0, -1 * bid['qty']])

		xs = [p[0] for p in points]
		ys = [p[1] for p in points]
		plt.stem(xs,ys, '-.')
		plt.show()

if __name__ == '__main__':
	exchange = 'TESTEX'
	stock = 'FOOBAR'
	key = '7f92e11fedbc270b2de73399633d9d78c1d569d4'
	account = 'FAE25277384'
	sf = Stockfighter(exchange, account, key)

	b = Book(sf.orderbook_for_stock(stock))

	print b.ascii()
	print b.totals()
	b.plot()
