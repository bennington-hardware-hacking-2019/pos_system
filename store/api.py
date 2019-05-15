# -*- coding: utf-8 -*-


class Store(object):
    def setup(self):
        print("store is setting up")

    def validate_card(self, card):
        print("store is validating:", card)
        return True

    def lookup(self, item):
        print("store is looking for item in the inventory")

    def get_items(self, cart):
        print("store is getting items information in the store:", cart)
        items = {}

        price = 0
        for item in cart:
            price += 1
            items[item] = price

        return items
