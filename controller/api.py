# -*- coding: utf-8 -*-

import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tag_reader
import card_reader
import db
import ui
import payment_processor

class Controller(object):

	def __init__(self):
		self.tag_reader = tag_reader.PN532()
		self.card_reader = card_reader.Wiegand26()
		self.db = db.DB()
		self.ui = ui.UI()
		self.payment_processor = payment_processor.Payment_Processor()

	def setup(self):
		print("pos_controller is setting up")
		self.tag_reader.setup()
		self.card_reader.setup()
		self.db.setup()
		self.ui.setup()
		self.payment_processor.setup()

	def run(self):
		"""
		run the pos_system (for demo purposes)
		return False whenever an error is occured to end the session
		"""
		print("controller is running")

		tags = [] # the tags in the cart
		# open the loop
		while True:
			# check for a tag reading
			tag = self.tag_reader.read()
			# if there is one
			if tag is not None: # this probably isn't the way to check
				# check if the item exists
				item = self.db.get_item(tag)
				if item is not None: # this probably isn't the way to check
					# add the item to the cart
					tags.append(tag) # will this add a tag many many times? need to check for repeat values
					# send the tag's item to the ui
					self.ui.add_item(item)
					time.sleep(.125)
				else:
					self.ui.tag_error()
				# should sales begin here? ie. self.db.make_sale()
			# check for a card reading
			card = self.card_reader.read()
			# if there is one
			if card is not None: # this probably isn't the way to check
				# check if the card exists
				if self.db.check_card(card):
					# collect all the items
					items = self.db.get_items(tags)
					# make the sale
					sale = self.db.make_sale(card, tags)
					# update the ui
					self.ui.checkout(sale, items)
					# restart the loop
					tags = []
				else:
					self.ui.card_error();
