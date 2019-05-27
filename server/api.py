# -*- coding: utf-8 -*-
import time

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO
from threading import Lock

import tag_reader
import card_reader
import db
import payment_processor

# ref - stop a loop in background thread
# https://stackoverflow.com/questions/44371041/python-socketio-and-flask-how-to-stop-a-loop-in-a-background-thread
import eventlet
eventlet.monkey_patch()

class Server(object):
	def __init__(self):
		# initialize flask and socketio
		self.app = Flask(__name__)
		self.app.secret_key = 'yagabeatsTHO'
		self.socketio = SocketIO(self.app, logger=True, async_mode='eventlet')
		self.cart = {}
		self.add_tag = False
		self.tag_reader = tag_reader.PN532()
		self.card_reader = card_reader.Wiegand()
		self.db = db.DB()
		self.payment_processor = payment_processor.PaymentProcessor()

	def setup(self, sim=False):
		# check if simuation is enabled
		if sim:
			self.tag_reader.sim_setup()
			self.card_reader.sim_setup()
		else:
			self.tag_reader.setup()
			self.card_reader.setup()

		self.db.setup()
		self.payment_processor.setup()

		# start serving all endpoints
		self.sockets()
		self.https()

	def sockets(self):
		"""websocket routes"""

		def validate_tag():
			"""keep reading for nfc tag item, validate, send it back to the ui"""
			# set add_tag to True to keep reading from tag
			self.add_tag = True

			while self.add_tag:
				try:
					# check for a tag reading
					# FIXME - sim
					print("sim_read")
					tag = self.tag_reader.sim_read()

					# check if the item exists in the database
					item = self.db.get_item(tag)
					resp = {
						'index': item.get('index'),
						'name': item.get('name'),
						'tag': tag,
						'description': item.get('description'),
						'cost': item.get('cost')
					}
					# send a response back to the ui client on `cart_response` channel
					self.socketio.emit('cart_response', resp, namespace='/cart')
					if item in self.cart:
						print("adding item to the cart:", resp)
					else:
						print("duplicate item not added", resp)
				except Exception as e:
					# if a reading fails, we can't really do anything other than passing
					# this and letting the customer tap the card again
					pass
				else:
					pass
				finally:
					pass

		@self.socketio.on('cart_request', namespace='/cart')
		def cart_request(payload):
			print(payload)
			self.socketio.start_background_task(validate_tag())

		@self.socketio.on('checkout_request', namespace='/cart')
		def checkout_request(payload):
			# set add_tag to False to stop the loop
			self.add_tag = False

			# save the cart
			self.cart = payload.get("data")
			print("===> cart:", self.cart)

			# tags is a list of tag reading values added in the cart
			tags = []

			# total is the total value of all items in the cart
			total = 0
			for k, v in self.cart.items():
					# get rid of prefix $ and convert back to float
					total += float(v.get("cost")[1:])
					tags.append(v.get("tag"))


			# wait for customer to tap their card
			# FIXME - sim
			print("reading card")
			card = self.card_reader.sim_read()
			print("finish reading card: ", card)

			# validate the card
			if self.db.check_card(card):
				# collect all the items
				# items = self.db.get_items(tags)

				# make sale
				# self.db.make_sale(card, tags)

				# send a payment confirmation request to the customer
				card_info = self.db.get_buyer(card)
				print(card_info)
				name = card_info.get("name")
				email = card_info.get("email")

				# TODO - frontend could utilize payment_info as follows:
				# - display `total` amount of values in the cart
				# - show `msg` and ask for customer's confirmation
				# - send `card` and `tags` data to `/receipt` endpoint to make the sale 
				payment_info = {
					"card": card,
					"tags": tags,
					"total": total,
					"msg": "a payment link will be sent to " + name + " (" + email + ")"
				}

				print(payment_info)
				# sleep for 5 seconds so that the websocket client is ready to listen again,
				# since it takes sometimes to load into a different page
				time.sleep(5);
				self.socketio.emit('checkout_response', payment_info, namespace='/checkout')

			# FIXME - payment processing is not working yet. it might be because how we
			# handle threading at the moment. need to look into this more.
			# charge_id = self.payment_processor.send_invoice(name, email, items)

			# # check payment status
			# if self.payment_processor.is_paid(charge_id):
			#		 pay_info = {
			#				 "msg": name + " has paid"
			#		 }

			#		 emit('checkout_response', pay_info)

		@self.socketio.on('admin_tag_add_request')
		def admin_tag_add_request():
			self.tag_reader.sim_setup()
			tag = self.tag_reader.sim_read()
			session['added_tag'] = tag
			self.socketio.of("/tag").emit('admin_tag_add_response', True)

	def https(self):
		"""http routes"""

		# ----------- #
		# USER ROUTES #
		# ----------- #

		@self.app.route('/')
		def index():
			self.cart = {}
			return render_template("index.html.j2")

		@self.app.route('/cart')
		def cart():
			return render_template("cart.html.j2", cart=self.cart)

		@self.app.route('/checkout')
		def checkout():
			return render_template("checkout.html.j2", cart=self.cart)

		@self.app.route('/help')
		def help():
			return render_template('help.html.j2')

		@self.app.route('/about')
		def about():
			return render_template('about.html.j2')

		# ------------ #
		# ADMIN ROUTES #
		# ------------ #

		@self.app.route('/login', methods=['GET', 'POST'])
		def login():
			if 'admin' in session:
				return redirect(url_for('items'))
			elif request.method == 'POST':
				# TODO (long term) - postgres from the card_reader
				# temporary - use a pin
				pin = request.form['pin']
				# TODO (long term) - put card_reader via websocket here
				# if pin/card verified
				if pin is not None and pin == "12345":
					session['admin'] = True
					return redirect(url_for('items'))
				else:
					return render_template('login.html.j2', error=True)
			else:
				return render_template('login.html.j2')

		@self.app.route('/logout')
		def logout():
			if 'admin' in session:
				session.clear()
			return redirect(url_for('index'))

		@self.app.route('/items')
		def items():
			if 'admin' in session:
				return render_template('items.html.j2', items=self.db.get_stock())
			else:
				return redirect(url_for('login'))

		@self.app.route('/items/held')
		def held():
			if 'admin' in session:
				return render_template('held.html.j2', items=self.db.get_held())
			else:
				return redirect(url_for('login'))

		@self.app.route('/items/sold')
		def sold():
			if 'admin' in session:
				return render_template('sold.html.j2', items=self.db.get_sold())
			else:
				return redirect(url_for('login'))

		@self.app.route('/items/add', methods=['GET', 'POST'])
		def add():
			if 'admin' in session:
				if request.method == 'POST':
					tag = session['added_tag']
					name = request.form['item']
					desc = request.form['desc']
					cost = request.form['cost']
					session['added_tag'] = None
					in_stock = 'in_stock' in request.form
					self.db.add_item(tag, name, desc, cost, in_stock)
					return redirect(url_for('items'))
				elif request.method == 'GET':
					return render_template('add.html.j2')
			else:
				return redirect(url_for('login'))

		@self.app.route('/items/edit/<index>', methods=['GET', 'POST'])
		def edit(index):
			if 'admin' in session:
				index = int(index)
				item = self.db.get_item_by_index(index)
				if item.get("sale_index") is None:
					in_stock = self.db.check_item(index)
					if request.method == 'GET':
						return render_template('edit.html.j2', item=item, in_stock=in_stock)
					elif request.method == 'POST':
						name = request.form['item']
						desc = request.form['desc']
						cost = request.form['cost']
						self.db.edit_item(index, name, desc, cost)
						if stock:
							return redirect(url_for('items'))
						else:
							return redirect(url_for('held'))
				else:
					return redirect(url_for('login'))
			else:
				return redirect(url_for('login'))

		@self.app.route('/items/hold/<index>')
		def hold(index):
			if 'admin' in session:
				index = str(int(index))
				self.db.hold_item(index)
				return redirect(url_for('items'))
			else:
				return redirect(url_for('login'))

		@self.app.route('/items/stock/<index>')
		def stock(index):
			if 'admin' in session:
				index = str(int(index))
				self.db.stock_item(index)
				return redirect(url_for('items'))
			else:
				return redirect(url_for('login'))

	def start(self):
		self.socketio.run(self.app, debug=True)
