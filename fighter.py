import os
from six.moves.urllib.parse import urljoin
import requests

class Fighter(object):
	base_url = 'https://api.stockfighter.io/ob/api/'

	def __init__(self, venue, account, api_key=None):
		self.venue = venue
		self.account = account
		self.api_key = api_key

		self.headers = {
		'X-Starfighter-Authorization': self.api_key
		}

	def _get(self, *args, **kwargs):
		kwargs['headers'] = self.headers if 'headers' not in kwargs else kwargs['headers']
		return requests.get(*args, **kwargs)

	def _post(self, *args, **kwargs):
		kwargs['headers'] = self.headers if 'headers' not in kwargs else kwargs['headers']
		return requests.post(*args, **kwargs)

	def _delete(self, *args, **kwargs):
		kwargs['headers'] = self.headers if 'headers' not in kwargs else kwargs['headers']
		return requests.delete(*args, **kwargs)

	def venue_stocks(self):
		"""List the stocks avalible for trading on the venue.

		https://starfighter.readme.io/docs/list-stocks-on-venue
		"""
		url = urljoin(self.base_url, 'venues/{0}/stocks'.format(self.venue))
		return self._get(url).json()

	def orderbook_for_stock(self, stock):
		"""Get the orderbook for a particular stock.

		https://starfighter.readme.io/docs/get-orderbook-for-stock
		"""
		url_fragment = "venues/{venue}/stocks/{stock}".format(
			venue = self.venue,
			stock = stock)

		url = urljoin(self.base_url, url_fragment)
		return self._get(url).json()

	def stock_quote(self, stock):
		"""Get a quote for a particular stock.

		https://starfighter.readme.io/docs/a-quote-for-a-stock
		"""
		url_fragment = "venues/{venue}/stocks/{stock}/quote".format(
			venue = self.venue,
			stock = stock)

		url = urljoin(self.base_url, url_fragment)
		return self._get(url).json()

	def place_new_order(self, stock, price, qty, direction, order_type):
		"""Place an order for a stock.

		https://starfighter.readme.io/docs/place-new-order
		"""
		url_fragment = "venues/{venue}/stocks/{stock}/orders".format(
			venue = self.venue,
			stock = stock)

		data = {
			"stock": stock,
			"price": price,
			"venue": self.venue,
			"account": self.account,
			"qty": qty,
			"direction": direction,
			"orderType": order_type
		}

		url = urljoin(self.base_url, url_fragment)
		resp = self._post(url, json=data)
		return resp.json()

	def status_for_order(self, stock, order_id):
		url_fragment = 'venues/{venue}/stocks/{stock}/orders/{order_id}'.format(
			venue = self.venue,
			stock = stock,
			order_id = order_id
			)
		url = urljoin(self.base_url,url_fragment)
		return self._get(url).json()

	def status_for_all_orders(self):
		"""Status for all orderbook_for_stock
		https://starfighter.readme.io/docs/status-for-all-orders
		"""
		url_fragment = 'venues/{venue}/accounts/{account}/orders'.format(
			venue = self.venue,
			account = self.account)

		url = urljoin(self.base_url, url_fragment)
		return self._get(url, headers=self.headers).json()

	def cancel_order(self, stock, order_id):
		"""Cancel an order"""
		url_fragment = 'venues/{venue}/stocks/{stock}/orders/{order_id}'.format(
            venue=self.venue,
            stock=stock,
            order_id=order_id,
        )
		url = urljoin(self.base_url, url_fragment)
		return self._delete(url, headers=self.headers).json()
