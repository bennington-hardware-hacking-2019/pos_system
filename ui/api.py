# import Flask

class UI(object):

	def __init__(self):
		# print("ui is initializing")
		pass

	def setup(self):
		# print("ui is setting up")
		pass

	def add_item(self, item):
		print("\n==================")
		print("Item added to cart")
		print("==================")
		print("\nItem:", item.get("item"), "\nDescription:", item.get("description"), "\nCost:", item.get("cost"))

	def checkout(self, sale, items):
		print("\n=============")
		print("Selling items")
		print("=============")
		print("\nSale #:", sale.get("index"))
		print("\nSold", len(items), "items")
		cost = 0;
		for item in items:
			# cost has the postgres money type, in such format
			# $xx.xx. python will read this as string. that said,
			# need to get rid of the $ and convert it back from
			# string to float in order to add up the total cost
			cost += float(item.get("cost")[1:])
		print("\nTotal cost:", cost)

	def card_error(self):
		print("We can't find your card, try again?")

	def tag_error(self):
		print("We can't find that item, try again?")
