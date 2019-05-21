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
        self.card_reader = card_reader.Wiegand()
        self.db = db.DB()
        self.ui = ui.UI()
        self.payment_processor = payment_processor.PaymentProcessor()

    def setup(self):
        print("pos_controller is setting up")
        
        # FIXME - disable hardware dep for now
        self.tag_reader.simulate_setup()
        self.card_reader.simulate_setup()

        self.db.setup()
        self.ui.setup()
        self.payment_processor.setup()

    def run(self):
        """
        run the pos_system (for demo purposes)
        return False whenever an error is occured to end the session
        """
        print("controller is running")

        # FIXME - instead of using an array, can use a dictionary to make sure
        # the uniqueness of a tag
        tags = []

        # check for a tag reading
        tag = self.tag_reader.simulate_read()
        
        # check if the item exists
        item = self.db.get_item(tag)

        if item is not None:
            # add the item to the cart
            tags.append(tag)

            # send the tag's item to the ui
            self.ui.add_item(item)

        print(tags)

        # check for a card reading
        card = self.card_reader.simulate_read()

        if self.db.check_card(card):
            # collect all the items
            items = self.db.get_items(tags)
            print(items)

            # make the sale
            # sale = self.db.make_sale(card, tags)

            # update the ui
            # self.ui.checkout(sale, items)
        else:
            self.ui.card_error();
