# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import SocketIO

import time
import eventlet

import tag_reader
import card_reader
import db
import payment_processor


# initialize flask and socketio
app = Flask(__name__)
app.secret_key = 'yagabeatsTHO'

# ref - stop a loop in background thread
# https://stackoverflow.com/questions/44371041/python-socketio-and-flask-how-to-stop-a-loop-in-a-background-thread
eventlet.monkey_patch()
socketio = SocketIO(app, logger=True, async_mode='eventlet')

# initialize and setup pos_system components
tag_reader = tag_reader.PN532()
card_reader = card_reader.Wiegand()
db = db.DB()
payment_processor = payment_processor.PaymentProcessor()

# FIXME - sim
tag_reader.sim_setup()
card_reader.sim_setup()
db.setup()
payment_processor.setup()

cart = {}
add_tag = False

"""
	websocket routes
"""

@socketio.on('cart_request', namespace='/cart')
def cart_request(payload):
	print(payload)
	socketio.start_background_task(validate_tag())

@socketio.on('checkout_request', namespace='/cart')
def checkout_request(payload):
	# set add_tag to False to stop the loop
	global add_tag
	add_tag = False

	# save the cart
	global cart
	cart = payload.get("data")
	print("===> cart:", cart)

	# tags is a list of tag reading values added in the cart
	tags = []

	# total is the total value of all items in the cart
	total = 0
	for k, v in cart.items():
		# get rid of prefix $ and convert back to float
		total += float(v.get("cost")[1:])
		tags.append(v.get("tag"))

	# wait for customer to tap their card
	# FIXME - sim
	print("reading card")
	card = card_reader.sim_read()
	print("finish reading card:", card)

	# validate the card
	if db.check_card(card):
		card_info = db.get_buyer(card)
		name = card_info.get("name")
		email = card_info.get("email")

		# collect all the items
		items = db.get_items(tags)

		# make sale
		db.make_sale(card, tags)

		# send a confirmation request to the customer
		# TODO - refer to #36. in short, frontend will make stripe payment
		payment_info = {
			"name": name,
			"email": email,
			"card": card,
			"tags": tags,
			"total": total,
			"msg": "a payment link will be sent to " + name + " (" + email + ")"
		}

		print(payment_info)

		# sleep for 5 seconds so that the websocket client is ready to listen again,
		# since it takes sometimes to load into a different page
		time.sleep(5);
		socketio.emit('checkout_response', payment_info, namespace='/checkout')

@socketio.on('tag_request', namespace='/tag')
def tag_request():
	# FIMXE - sim
	tag = tag_reader.sim_read()
	session['tag'] = tag
	socketio.emit('tag_response', True, namespace='/tag')

@socketio.on('card_request', namespace='/card')
def tag_request():
	# FIMXE - sim
	card = card_reader.sim_read()
	session['card'] = card
	socketio.emit('card_response', True, namespace='/card')

"""
	http routes
"""

# -----------
# user routes
# -----------

@app.route('/')
def index():
	cart = {}
	return render_template("index.html.j2")

@app.route('/cart')
# FIXME - name `on_cart` instead of `cart` because `cart` is already used
# for holding items and they are conflicting if name the same.
def on_cart():
	return render_template("cart.html.j2", cart=cart)

@app.route('/checkout')
def checkout():
	return render_template("checkout.html.j2", cart=cart)

@app.route('/help')
def help():
	return render_template('help.html.j2')

@app.route('/about')
def about():
	return render_template('about.html.j2')

@app.route('/pay', methods=['POST'])
def pay():
	payload = request.get_json()

	name = payload.get("name")
	email = payload.get("email")
	card = payload.get("card")
	tags = payload.get("tags")

	# collect all the items
	items = db.get_items(tags)

	# make sale
	db.make_sale(card, tags)

	# FIXME - refer to #36 - stripe api raises connection error
	# charge_id = payment_processor.send_invoice(name, email, items)

	# check payment status
	# resp = {"status": "pending"}
	# if payment_processor.is_paid(charge_id):
	# 	resp["status"] = "done"

	# return jsonify(resp)

	return jsonify({"status": "ok"})

# ------------
# admin routes
# ------------

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
	if 'admin' in session:
		session.clear()
	return redirect(url_for('index'))

@app.route('/items')
def items():
	if 'admin' in session:
		return render_template('items.html.j2', items=db.get_stock())
	else:
		return redirect(url_for('login'))

@app.route('/items/held')
def held():
	if 'admin' in session:
		return render_template('held.html.j2', items=db.get_held())
	else:
		return redirect(url_for('login'))

@app.route('/items/sold')
def sold():
	if 'admin' in session:
		return render_template('sold.html.j2', items=db.get_sold())
	else:
		return redirect(url_for('login'))

@app.route('/items/add', methods=['GET', 'POST'])
def add():
	if 'admin' in session:
		if request.method == 'POST':
			if 'tag' in session:
				tag = session['tag']
				session['tag'] = None
			else:
				tag = None
			name = request.form['item']
			desc = request.form['desc']
			cost = request.form['cost']
			in_stock = 'in_stock' in request.form
			db.add_item(tag, name, desc, cost, in_stock)
			return redirect(url_for('items'))
		elif request.method == 'GET':
			return render_template('add.html.j2')
	else:
		return redirect(url_for('login'))

@app.route('/items/edit/<index>', methods=['GET', 'POST'])
def edit(index):
	if 'admin' in session:
		index = int(index)
		item = db.get_item_by_index(index)
		if item.get("sale_index") is None:
			in_stock = db.check_item(index)
			if request.method == 'GET':
				return render_template('edit.html.j2', item=item, in_stock=in_stock)
			elif request.method == 'POST':
				name = request.form['item']
				desc = request.form['desc']
				cost = request.form['cost']
				db.edit_item(index, name, desc, cost)
				if stock:
					return redirect(url_for('items'))
				else:
					return redirect(url_for('held'))
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))

@app.route('/items/hold/<index>')
def hold(index):
	if 'admin' in session:
		index = str(int(index))
		db.hold_item(index)
		return redirect(url_for('items'))
	else:
		return redirect(url_for('login'))

@app.route('/items/stock/<index>')
def stock(index):
	if 'admin' in session:
		index = str(int(index))
		db.stock_item(index)
		return redirect(url_for('items'))
	else:
		return redirect(url_for('login'))

"""
	utils
"""

def validate_tag():
	"""keep reading for nfc tag item, validate, send it back to the ui"""
	# set add_tag to True to keep reading from tag
	global add_tag
	add_tag = True

	while add_tag:
		try:
			# check for a tag reading
			# FIXME - sim
			tag = tag_reader.sim_read()

			# check if the item exists in the database
			item = db.get_item(tag)
			resp = {
				'index': item.get('index'),
				'name': item.get('name'),
				'tag': tag,
				'description': item.get('description'),
				'cost': item.get('cost')
			}
			# send a response back to the ui client on `cart_response` channel
			socketio.emit('cart_response', resp, namespace='/cart')
		except Exception as e:
			# if a reading fails, we can't really do anything other than passing
			# this and letting the customer tap the card again
			pass
		else:
			pass
		finally:
			pass

def start():
	socketio.run(app, debug=True)