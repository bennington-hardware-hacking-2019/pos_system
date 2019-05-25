# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, emit
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
		self.socketio = SocketIO(self.app, async_mode='eventlet')
		self.checkout = False
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

		# start serving http/websocket endpoints
		self.up()

	def validate_card(self):
		"""keep reading for nfc tag item, validate, send it back to the ui"""
		# set checkout to True to keep reading from tag
		self.checkout = True

		while self.checkout:
			# check for a tag reading
			tag = self.tag_reader.sim_read()

			# check if the item exists in the database
			item = self.db.get_item(tag)
			resp = {
				'item': item.get('item'),
				'description': item.get('description'),
				'cost': item.get('cost')
			}

			print("adding item to the cart:", resp)

			# send a response back to the client on `add_to_cart_response` channel
			emit('add_to_cart_response', resp)

	def up(self):
		"""http/websocket routes definitions"""
		@self.socketio.on('add_to_cart_request')
		def add_to_cart_request(payload):
			print(payload)

			self.socketio.start_background_task(self.validate_card())

		@self.socketio.on('checkout_request')
		def checkout_request(payload):
			print(payload)

			# set checkout to False to stop the loop
			self.checkout = False

			cart = ""
			total = 0
			for k, v in payload.get("data").items():
				cart += k + " "
				# get rid of prefix $ and convert back to float
				total += float(v[1:])

			# set checkout to False to stop the loop
			self.checkout = False

			resp = {
				"msg": "total is " + str(total)[:5] + " for " + cart
			}
			# send a response back to the client on `add_to_cart_response` channel
			emit('checkout_response', resp)


		@self.app.route('/checkout')
		def checkout():
			return render_template('checkout.html.j2')

		@self.app.route('/')
		def index():
			return render_template("index.html.j2")

		@self.app.route('/help')
		def help():
			return render_template('help.html.j2')

		@self.app.route('/about')
		def about():
			return render_template('about.html.j2')

		@self.app.route('/cart')
		def cart():
			return render_template("cart.html.j2")

		@self.socketio.on('add_to_cart_request')
		def add_to_cart_request(payload):
			print(payload)

			# TODO - check for a tag reading
			# check if the item exists in the database

			# send a response back to the client on `server response` channel
			# check for a tag reading
			tag = self.tag_reader.sim_read()

			item = self.db.get_item(tag)
			resp = {
				'item': item.get('item'),
				'description': item.get('description'),
				'cost': item.get('cost')
			}

			emit('add_to_cart_response', resp)

		@self.app.route('/login', methods=['GET', 'POST'])
		def login():
			if 'admin' in session:
				return redirect(url_for('stock'))
			elif request.method == 'POST':
				# long term - postgres from the card_reader
				# temporary - use a pin
				pin = request.form['pin']
				# long term - Hoanh put card_reader via websocket here
				# if pin/card verified
				if pin is not None and pin == "12345":
					session['admin'] = True
					return redirect(url_for('stock'))
				else:
					return render_template('login.html.j2', error=True)
			else:
				return render_template('login.html.j2')

		@self.app.route('/logout')
		def logout():
			if 'admin' in session:
				session.clear()
			return redirect(url_for('index'))

		@self.app.route('/stock')
		def stock():
			if 'admin' in session:
				return render_template('stock.html.j2', stock = self.db.get_stock())
			else:
				return redirect(url_for('login'))

		@self.app.route('/stock/all')
		def all():
			if 'admin' in session:
				return render_template('stock.html.j2', stock = self.db.get_all_items(), all = True)
			else:
				return redirect(url_for('login'))

		@self.app.route('/stock/add', methods=['GET', 'POST'])
		def add():
			if 'admin' in session:
				if request.method == 'POST':
					#Here hoanh!
					#tag = whaaaat
					#dummy tag
					#using random so we can create a lot of dummy data without error handling
					import random
					rand = random.randint(1,101)
					tag = [1,0,68,0,7,4,137,16,98,101,rand]
					name = request.form['item']
					desc = request.form['desc']
					cost = request.form['cost']
					self.db.add_item(tag, name, desc, cost)
					return redirect(url_for('stock'))
				elif request.method == 'GET':
					return render_template('add.html.j2')
			else:
				return redirect(url_for('login')) #needs testing

		@self.app.route('/stock/edit/<index>', methods=['GET', 'POST'])
		def edit(index):
			if 'admin' in session:
				stock = self.db.check_stock(index)
				if request.method == 'GET':
					item = self.db.get_item_by_index(index)
					return render_template('edit.html.j2', item=item, stock=stock)
				elif request.method == 'POST':
					index = int(index)
					name = request.form['item']
					desc = request.form['desc']
					cost = request.form['cost']
					self.db.edit_item(index, name, desc, cost)
					if stock:
						return redirect(url_for('stock'))
					else:
						return redirect(url_for('all'))
			else:
				return redirect(url_for('login'))

		@self.app.route('/stock/un/<index>')
		def unstock(index):
			if 'admin' in session:
				index = str(int(index))
				self.db.unstock_item(index)
				return redirect(url_for('stock'))
			else:
				return redirect(url_for('login'))

		@self.app.route('/stock/re/<index>')
		def restock(index):
			if 'admin' in session:
				index = str(int(index))
				self.db.restock_item(index)
				return redirect(url_for('stock'))
			else:
				return redirect(url_for('login'))

	def start(self):
		# self.app.run(debug=True)
		self.socketio.run(self.app, debug=True)
