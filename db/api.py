# -*- coding: utf-8 -*-


class DB(object):
    def setup(self):
        print("db is setting up")

    def validate_card(self, card):
        print("db is validating:", card)
        return True

    def lookup(self, item):
        print("db is looking for item in the inventory")

    def get_items(self, cart):
        print("db is getting items information in the store:", cart)
        items = {}

        price = 0
        for item in cart:
            price += 1
            items[item] = price

        return items
