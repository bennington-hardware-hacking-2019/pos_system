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
        # print("controller is setting up")
        
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
        # print("controller is running")

        # FIXME - instead of running the system sequentially, figure out how
        # to communicate by sending/catching signals from/to other components
        # for now, let the sensor run in a defined protocol, nfc read from a
        # number of defined number of cards

        # FIXME - instead of using an array, can use a dictionary to make sure
        # the uniqueness of a tag
        tags = []

        # check for a tag reading
        for i in range(3):
            tag = self.tag_reader.read()
            
            # check if the item exists
            item = self.db.get_item(tag)

            if item is not None:
                # add the item to the cart
                tags.append(tag)

                # send the tag's item to the ui
                self.ui.add_item(item)
            else:
                print("invalid tag item")

        # check for a card reading
        card = self.card_reader.read()

        if self.db.check_card(card):
            # collect all the items
            items = self.db.get_items(tags)

            # make the sale
            sale = self.db.make_sale(card, tags)

            # update the ui
            self.ui.checkout(sale, items)

            # send invoice to the customer
            card_info = self.db.get_buyer(card)
            name = card_info.get("name")
            email = card_info.get("email")
            charge_id = self.payment_processor.send_invoice(name, email, items)

            # FIXME - check if it's paid
            # realistically would check it later
            if self.payment_processor.is_paid(charge_id):
                print(name, "has paid")

            # FIXME - add logic to update the stock after an item is purchased
        else:
            self.ui.card_error();
