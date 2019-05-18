# -*- coding: utf-8 -*-

import stripe

# test api key
stripe.api_key = "sk_test_FyFkCuZ9s6C55DVxWA7niTil00Vztm2fgy"


class Payment_Processor(object):
    def setup(self):
        print("payment_processor is setting up")

    def send_invoice(self, card, items):
        print("payment_processor is sending invoice of", items, "to", card)
        return True

    def get_balance(self):
        return stripe.Balance.retrieve()

    def get_balance_history(self, limit):
        return stripe.BalanceTransaction.list(limit=limit)

    def create_charge(self, amount, desc):
        return stripe.Charge.create(
                amount=amount,
                currency="usd",
                source="tok_amex", # test american express token
                description=desc
        )

    def retrieve_charge(self, id):
        return stripe.Charge.retrieve(id)
