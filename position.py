class Position(object):
	def __init__(self):
		self.cash = 0
		self.position = 0
		self.netval = 0
		self.items_buy = 0
		self.items_sell = 0
		self.total_buy = 0
		self.total_sell = 0
		self.avg_buy = 0
		self.avg_sell = 0
		self.assets = []

	def print_pos(self):
		print "Assets: "
		print self.assets
		self.netval = self.total_sell - self.total_buy

		outstr = "Cash: ${c:.2f} Position: {p}".format(
			c = self.cash / 100.0,
			p = self.position)

		print outstr

	def get_position(self):
		return self.position

	def assets_original_value(self):
		total_value = 0
		total_items = 0
		for asset in self.assets:
			total_value += asset['value']
			total_items += asset['items']

		return [total_value, total_items]

	def sell(self, items, total):
		self.items_sell += items
		self.total_sell += total
		self.avg_sell = self.total_sell / self.items_sell
		before_position = self.position
		self.position -= items
		self.cash += total

		sell_avg = total / items
		
		if before_position > 0:
			# update assets (remove from the front, fifo)
			removed = 0
			for asset in self.assets:
				asset_items = asset['items']
				asset_value = asset['value']
				if asset_items != 0:
					asset_avg = asset_value / asset_items
					if asset_items > items:
						asset['items'] = asset_items - items
						asset['value'] = asset['items'] * asset_avg
						items = 0
						total = 0
						break
					else:
						items -= asset_items
						asset['items'] = 0
						asset['value'] = 0
						removed += 1
			# purge assets
			while removed > 0:
				self.assets.pop(0)
				removed -= 1

		if self.position < 0:
			# if negative assets add them in
			if items > 0:
				items = items * -1
				value = items * sell_avg
				self.assets.append({'items':items, 'value':value})


	def buy(self, items, total):
		self.items_buy += items
		self.total_buy += total
		self.avg_buy = self.total_buy / self.items_buy
		before_position = self.position
		self.position += items
		self.cash -= total

		if before_position < 0:
			# negative position, negative values to remove
			# update assets (remove from the front, fifo)
			removed = 0
			for asset in self.assets:
				asset_items = asset['items']
				asset_value = asset['value']
				if asset_items != 0:
					asset_avg = -1 * asset_value / asset_items
					if asset_items > items:
						asset['items'] = asset_items + items
						asset['value'] = asset['items'] * asset_avg
						items = 0
						total = 0
						break
					else:
						items -= -1 * asset_items
						asset['items'] = 0
						asset['value'] = 0
						removed += 1
			# purge assets
			while removed > 0:
				self.assets.pop(0)
				removed -= 1

		if self.position > 0:	
			# add to the back, fifo
			self.assets.append({'items':items, 'value':total})
