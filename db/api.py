# -*- coding: utf-8 -*-

import datetime
import uuid
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

    def validate_card(self, nfc_card):
        """check if the card exists in the store"""
        print("db is validating:", nfc_card)
        if self.get_card(nfc_card) is None:
            print("db failed to validate:", nfc_card)
            return False

        print("db successfully validated:", nfc_card)
        return True

    def get_card(self, nfc_card):
        """get a card information"""
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM account WHERE nfc_card = %s;", (nfc_card,))
        result = cur.fetchone()
        cur.close()

        return result

    def get_available_items(self, cart):
        """return a map of item information from the cart
           format:
             <nfc_tag>: {"item":<item>, "description":<description", "price":<price"}}
        """
        print("db is getting items information in the store:", cart)
        d = {}
        for i in cart:
            item = self.get_available_item(i)
            try:
                d[item.get("nfc_tag")] = {
                        "item": item.get("item"),
                        "description": item.get("description"),
                        "price": float(item.get("price"))
                }
            except AttributeError as e:
                # if the tag is None, there is nothing we really do here
                pass

        return d

    def get_available_item(self, nfc_tag):
        """get item informations for a available item"""
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM inventory WHERE nfc_tag = %s AND status = %s;", (nfc_tag, "available",))
        result = cur.fetchone()
        cur.close()

        return result
    
    def update_sold_items(self, items):
        """update items status to sold"""
        for item in items:
            self.update_item_status(item, "sold")

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

    def create_pending_transaction(self, card, items):
        """create a pending transaction for purchasing items"""
        # FIXME - this generates a random uuid, but not sure if this is how we
        # should use it though
        transaction_id = str(uuid.uuid4())
        bennington_id = int(self.get_card(card).get("bennington_id"))
        date_added = datetime.datetime.now()

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        for nfc_tag in items:
            cur.execute("INSERT INTO transaction (transaction_id, bennington_id, nfc_tag, date_added, status) VALUES (%s, %s, %s, %s, %s);",
                    (transaction_id, bennington_id, nfc_tag, date_added, "pending"))

        self.conn.commit()
        cur.close()

        return transaction_id

    def get_transaction(self, id):
        """get transaction information for a given transaction id"""
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM transaction WHERE transaction_id = %s;", (id,))
        result = cur.fetchall()
        cur.close()

        return result
