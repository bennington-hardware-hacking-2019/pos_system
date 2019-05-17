# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from psycopg2 import sql

DATABASE = 'tapa'

class DB(object):
    def __init__(self):
        self.conn = psycopg2.connect("dbname='{0}'".format(DATABASE))

    def setup(self):
        """FIXME"""
        print("db is setting up")

    def validate_card(self, card):
        """FIXME"""
        print("db is validating:", card)
        return True

    def lookup(self, item):
        """FIXME"""
        print("db is looking for item in the inventory")

    def get_items(self, cart):
        """FIXME"""
        print("db is getting items information in the store:", cart)
        items = {}

        price = 0
        for item in cart:
            price += 1
            items[item] = price

        return items

    def update_item_status(self, nfc_tag, status):
        """update item status to either available or sold"""
        valid_status = ["available", "sold"]
        if status not in valid_status:
            print("failed to update status:", status)
            return

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("UPDATE inventory SET status = %s WHERE nfc_tag = %s;", (status, nfc_tag,))
        self.conn.commit()
        cur.close()

    def get_item_status(self, nfc_tag):
        """get item status"""
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT status FROM inventory WHERE nfc_tag = %s;", (nfc_tag,))
        result = cur.fetchone()
        cur.close()
        return result["status"]
