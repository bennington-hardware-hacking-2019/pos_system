import Flask

class UI(object):

	def __init__(self):
		print("ui is initializing")
		# do something

	def setup(self):
		print("ui is setting up")
		# do something

	def add_item(self, item):
		print("Item added to cart")
		print("\nItem name: ",item.get("name"),"\nItem description: ",item.get("description"),"\nItem cost: ",item.get("cost"))

	def checkout(self, sale, items):
		print("Selling items")
		print("\nSale #: ",sale.get("index"))
		print("\nSold ",len(items)," items")
		cost = 0;
		for item in items:
			cost += item.get("cost")
		print("\nTotal cost: ", cost)

	def card_error(self):
		print("We can't find your card, try again?")

	def tag_error(self):
		print("We can't find that item, try again?")
