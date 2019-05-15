# -*- coding: utf-8 -*-


class Payment_Processor(object):
    def setup(self):
        print("payment_processor is setting up")

    def send_invoice(self, card, items):
        print("payment_processor is sending invoice of", items, "to", card)
        return True
