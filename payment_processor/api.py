# -*- coding: utf-8 -*-

import stripe

# test api key
stripe.api_key = "sk_test_FyFkCuZ9s6C55DVxWA7niTil00Vztm2fgy"


class PaymentProcessor(object):
	def setup(self):
		"""FIXME"""
		# print("payment_processor is setting up")
		pass

	def send_invoice(self, name, email, items):
		"""send invoice"""
		total_cost = 0
		for item in items:
			total_cost += float(item.get("cost")[1:])

		desc = "Charge " + name + " (" + email + ")" + " for a total of " + str(total_cost)
		return self.create_charge(int(total_cost * 100), desc)

	def get_balance(self):
		"""get stripe account balance"""
		return stripe.Balance.retrieve()

	def get_balance_history(self, limit):
		"""get stripe balance history"""
		return stripe.BalanceTransaction.list(limit=limit)

	def create_charge(self, amount, desc):
		"""create a charge and return its id"""
		print(desc)
		charge = stripe.Charge.create(
				amount=amount,
				currency="usd",
				source="tok_amex", # test american express token
				description=desc
		)

		return charge.get("id")

	def get_charges(self, limit):
		"""get a list of charges"""
		return stripe.Charge.list(limit=limit)

	def is_paid(self, id):
		"""return charnge status whether is is paid or not"""
		return stripe.Charge.retrieve(id).get("paid")

	def get_charge(self, id):
		"""return a charnge"""
		return stripe.Charge.retrieve(id)
