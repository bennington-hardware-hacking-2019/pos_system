# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, join_room, emit

import tag_reader
import card_reader
import db
import payment_processor

class Server(object):
	def __init__(self):
		# initialize flask and socketio
		self.app = Flask(__name__)
		self.app.secret_key = 'yagabeatsTHO'
		self.socketio = SocketIO(self.app)
		self.is_read = False
		self.tag_reader = tag_reader.PN532()
		self.card_reader = card_reader.Wiegand()
		self.db = db.DB()
		self.payment_processor = payment_processor.PaymentProcessor()

	def setup(self, sim=False):
		if sim:
			self.tag_reader.sim_setup()
			self.card_reader.sim_setup()
		else:
			self.tag_reader.setup()
			self.card_reader.setup()

		self.db.setup()
		self.payment_processor.setup()

		@self.app.route('/')
		def index():
			return render_template("index.html.j2")

		@self.app.route('/cart')
		def cart():
			return "checkout here"

		@self.socketio.on('server request')
		def on_server_request(payload):
			print(payload)

			# TODO - check for a tag reading
			# check if the item exists in the database

			# send a response back to the client on `server response` channel
			# check for a tag reading
			tag = self.tag_reader.read()

			item = self.db.get_item(tag)
			resp = {
					'item': item.get('item'),
					'description': item.get('description'),
					'cost': item.get('cost')
					}

			emit('server response', resp)

		@self.app.route('/help')
		def help():
			return render_template('help.html.j2')

		@self.app.route('/about')
		def info():
			return render_template('about.html.j2')

		@self.app.route('/login', methods = ['GET'])
		def login():
			return render_template('login.html.j2')

		@self.app.route('/stock', methods = ['POST'])
		def stock():
			#postgres for card - long term
			#get the pin from the login form - temporary
			pin = int(request.form['pin'])
			#if password/card verified
			if (pin == 123):
				session['username'] = 'admin' #Temporary
				stock = self.db.get_stock()
				return render_template('stock.html.j2',stock = stock)
			else:
				return redirect(url_for('login')) #needs testing

		@self.app.route('/stock/add', methods = ['GET', 'POST'])
		def add():
			if 'username' in session:
				if request.method == 'POST':
					name = request.form['name']
					desc = request.form['desc']
					cost = request.form['cost']
					self.db.add_item(name, desc, cost)
					return redirect(url_for('admin'))
				elif request.method == 'GET':
					return render_template('add.html.j2')
			else:
				return redirect(url_for('login')) #needs testing

	def start(self):
		# self.app.run(debug=True)
		self.socketio.run(self.app, debug=True)
