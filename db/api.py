# -*- coding: utf-8 -*-

import datetime
import psycopg2
import psycopg2.extras # we need a dictionary for each row

DATABASE = 'tapa'

class DB(object):
	def __init__(self):
		# uses our DATABASE variable to set the dbname and create a connection
		self.conn = psycopg2.connect("dbname='{0}'".format(DATABASE))

	def setup(self):
		"""
		FIXME
		"""
		# print("db is setting up")
		pass

	def check_card(self, card):
		"""
		check if the card exists in the db
		"""
		# print("db is validating: ", card)
		if self.get_buyer(card) is None:
			# print("db failed to validate: ", card)
			return False
		else:
			# print("db successfully validated: ", card)
			return True

	def check_item(self, index):
		"""
		check if an item is in stock (admin)
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		# get the stocked item
		cur.execute(
			"""
			SELECT item_index
			FROM stock
			WHERE item_index = %s;
			""",
			(index,)
		)
		result = cur.fetchone()
		cur.close()
		if result is not None:
			return True
		else:
			return False

	def check_sale(self, index):
		"""
		check if the sale has been paid
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		# get the stocked item
		cur.execute(
			"""
			SELECT date_paid
			FROM sale
			WHERE index = %s;
			""",
			(index,)
		)
		date = cur.fetchone()
		cur.close()
		if date is not None and date is not '':
			return True
		else:
			return False

	def get_buyer(self, card):
		"""
		get buyer information from card
		returns a dictionary buyer object
		"""
		# use psycopg extras to return a fancy dictionary for each row
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		# get the buyer
		cur.execute(
			"""
			SELECT *
			FROM buyer
			WHERE card = %s;
			""",
			(card,)
		)
		buyer = cur.fetchone()
		cur.close()
		return buyer

	def add_buyer(self, name, email, card):
		"""
		add buyer name, email and card
		returns True
		"""
		# use psycopg extras to return a fancy dictionary for each row
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		# get the buyer
		cur.execute(
			"""
			INSERT INTO buyer
			(name, email, card)
			VALUES (%s, %s, %s)
			""",
			(name, email, card)
		)
		self.conn.commit()
		cur.close()
		return True

	def get_items(self, tags):
		"""
		get items from tags
		returns an array of item dictionaries
		"""
		items = []
		for tag in tags:
			items.append(self.get_item(tag))
		return items

	def get_item(self, tag):
		"""
		get item information from tag
		returns an item dictionary
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			SELECT *
			FROM item
			JOIN stock
			ON item.index = stock.item_index
			WHERE item.tag = %s
			""",
			(tag,)
		)
		item = cur.fetchone()
		cur.close()
		return item

	# FIXME - this function is almost a repeat of get item — can they merge?
	def get_item_by_index(self, index):
		"""
		get item information from index
		returns an item dictionary
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			SELECT *
			FROM item
			WHERE item.index = %s
			""",
			(index,)
		)
		item = cur.fetchone()
		cur.close()
		return item

	# FIXME - this function is almost a repeat of get items — can they merge?
	def get_stock(self):
		"""
		get all in stock items
		returns an array of item dictionaries
		"""
		# print("db is getting all in stock items")
		# use psycopg extras to return a fancy dictionary for each row
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		# get the buyer
		cur.execute(
			"""
			SELECT item.*
			FROM item
			JOIN stock
			ON item.index = stock.item_index;
			"""
		)
		items = cur.fetchall()
		cur.close()
		return items

	# FIXME - this function is almost a repeat of get items — can they merge?
	def get_sold(self):
		"""
		get all the sold items
		returns an array of item dictionaries
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			SELECT item.*, sale.date_added as date_sold, sale.date_paid
			FROM item
			JOIN sale
			ON item.sale_index = sale.index
			"""
		)
		items = cur.fetchall()
		cur.close()
		return items

	# FIXME - this function is almost a repeat of get items — can they merge?
	def get_held(self):
		"""
		get all the held items (items that aren't in stock, and aren't sold)
		returns an array of item dictionaries
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			SELECT *
			FROM item
			WHERE item.sale_index IS NULL AND item.index NOT IN (SELECT item_index FROM stock)
			"""
		)
		items = cur.fetchall()
		cur.close()
		return items

	def add_item(self, tag, name, desc, cost, in_stock=True):
		"""
		adds an item to the DB (for admin)
		returns true if successful
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			INSERT INTO item
			(tag,name,description,cost)
			VALUES
			(%s,%s,%s,%s)
			RETURNING index
			""",
			(tag,name,desc,cost)
		)
		if in_stock:
			item_index = cur.fetchone().get("index")
			cur.execute(
				"""
				INSERT INTO stock
				(item_index)
				VALUES
				(%s)
				""",
				(item_index,)
			)
		self.conn.commit()
		cur.close()
		return True

	def edit_item(self, index, name, desc, cost):
		"""
		edits an item in the DB (for admin)
		returns true if successful
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			UPDATE item
			SET (name,description,cost) = (%s,%s,%s)
			WHERE index = (%s)
			""",
			(name,desc,cost,index)
		)
		self.conn.commit()
		cur.close()
		return True

	def hold_item(self, index):
		"""
		removes an item from stock but doesn't delete it (for admin)
		returns true if successful
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			DELETE FROM stock
			WHERE item_index = (%s)
			""",
			(index,)
		)
		self.conn.commit()
		cur.close()
		return True

	def stock_item(self, index):
		"""
		moves an item to stock (for admin)
		returns true if successful
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			INSERT INTO stock
			(item_index)
			VALUES (%s)
			""",
			(index,)
		)
		self.conn.commit()
		cur.close()
		return True

	def sell_items(self, tags, sale_index):
		"""
		add sale_index to items
		returns a boolean
		"""
		for tag in tags:
			self.sell_item(tag, sale_index)
		return True

	def sell_item(self, tag, sale_index):
		"""
		add sale_index to item
		returns a boolean
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			UPDATE item
			SET sale_index = %s
			WHERE tag = %s
			RETURNING index
			""",
			(sale_index, tag,)
		)
		item_index = cur.fetchone().get("index")
		cur.execute(
			"""
			DELETE FROM stock
			WHERE item_index = %s
			""",
			(item_index,)
		)
		self.conn.commit()
		cur.close()
		return True

	def make_sale(self, card, tags):
		"""
		create a sale of items
		returns a sale dictionary
		"""
		bennington_id = int(self.get_buyer(card).get("bennington_id"))
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			INSERT INTO sale (
				bennington_id
			) VALUES (%s)
                        RETURNING index;
			""",
			(bennington_id,)
		)
		sale = cur.fetchone()
		self.sell_items(tags, sale.get("index"))
		self.conn.commit()
		cur.close()
		return sale

	def get_sale(self, index):
		"""
		get sale information for a given index
		returns a sale dictionary
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			SELECT *
			FROM sale
			WHERE index = %s;
			""",
			(index,)
		)
		sale = cur.fetchone()
		cur.close()
		return sale

	def get_unpaid(self):
		"""
		get unpaid sales
		returns an array of sale dictionaries
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			SELECT *
			FROM sale
			WHERE date_paid = NULL;
			"""
		)
		sales = cur.fetchall()
		cur.close()
		return sales
