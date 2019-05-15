# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pn532
import prx_3hc
import store
import payment_processor


class Controller(object):
    def __init__(self):
        self.prx_3hc = prx_3hc.PRX_3HC()
        self.pn532 = pn532.PN532()
        self.store = store.Store()
        self.payment_processor = payment_processor.Payment_Processor()

    def setup(self):
        print("controller is setting up")

        self.prx_3hc.setup()
        self.pn532.setup()
        self.store.setup()
        self.payment_processor.setup()

    def run(self):
        """run the system sequentially (only for demo purposes)
           return False whenever an error is occured to end the session
        """
        print("controller is running")

        # tap a bennington card to start a check out session
        bennington_card = self.prx_3hc.read()

        # if the card is invalid (not in the store), end the session
        if not self.store.validate_card(bennington_card):
            return False

        # scan a number of nfc tags and add them to a cart
        cart = []
        for i in range(3):
            cart.append(self.pn532.read())

        # tap the bennington card again to end the checkout session
        # if the card is not the same card as before, end the session
        if not bennington_card == self.prx_3hc.read():
            return False

        # get informations for items in the card and update their status
        items = self.store.get_items(cart)

        if len(items) == 0:
            return False

        # send an invoice to the person
        if not self.payment_processor.send_invoice(bennington_card, items):
            return False

        return True
