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

	def check_stock(self, item_index):
		"""
		check if an item is in stock (admin)
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		# get the buyer
		cur.execute(
			"""
			SELECT item_index
			FROM stock
			WHERE item_index = %s;
			""",
			(item_index,)
		)
		result = cur.fetchone()
		cur.close()
		if result is not None:
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
			SELECT *
			FROM item
			JOIN stock
			ON item.index = stock.item_index;
			"""
		)
		items = cur.fetchall()
		cur.close()
		return items

	def get_items(self, tags):
		"""
		get items information
		returns an array of item dictionaries
		"""
		items = []
		for tag in tags:
			items.append(self.get_item(tag))
		return items

	def get_item(self, tag):
		"""
		get item information
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

	def get_item_by_index(self, index):
		"""
		get item information
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

	def get_all_items(self):
		"""
		get all the items including out of stock
		returns an array of item dictionaries
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			SELECT index AS item_index, *
			FROM item
			"""
		)
		items = cur.fetchall()
		cur.close()
		return items

	def add_item(self, tag, name, desc, cost):
		"""
		adds an item to the DB (for admin)
		returns true if successful
		"""
		cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(
			"""
			INSERT INTO item
			(tag,item,description,cost)
			VALUES
			(%s,%s,%s,%s)
			RETURNING index
			""",
			(tag,name,desc,cost)
		)
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
			SET (item,description,cost) = (%s,%s,%s)
			WHERE index = (%s)
			""",
			(name,desc,cost,index)
		)
		self.conn.commit()
		cur.close()
		return True

	def unstock_item(self, index):
		"""
		removes an item from stock (for admin)
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

	def restock_item(self, index):
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
			(index)
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
		item_index = cur.fetchone()
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
