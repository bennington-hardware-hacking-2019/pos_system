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

        @self.app.route('/')
        def index():
            # FIXME - suffix .j2 instead of .html? variable Oy?
            return render_template("base.html.j2", variable="Oy")

        @self.app.route('/checkout')
        def checkout():
            return render_template('checkout.html')

        @self.app.route('/help')
        def help():
            return render_template('help.html')

        @self.app.route('/info')
        def info():
            return render_template('info.html')

        @self.app.route('/login', methods = ['GET'])
        def login():
            return render_template('login.html')

        @self.app.route('/admin', methods = ['POST'])
        def admin():
            # postgres for card - long term
            # get the pin from the login form - temporary
            pin = int(request.form['pin'])

            # if password/card verified

            if (pin == 123):
                session['username'] = 'admin' # temporary
                return render_template('inventory.html')
            else:
                return redirect(url_for('login')) # needs testing

        @self.app.route('/admin/create', methods = ['GET', 'POST'])
        def create():
            if 'username' in session:
                if request.method == 'POST':
                    name = request.form['name']
                    desc = request.form['desc']
                    cost = request.form['cost']

                    # insert this stuff into whatever
                    db.create(name, desc, cost)

                    return redirect(url_for('items'))
                elif request.method == 'GET':
                    return render_template('create.html')
            else:
                return redirect(url_for('login')) # needs testing

        @self.app.route('/items', methods = ['GET'])
        def items():
            # postgres
            item = db.items()
            return render_template('data.html', items=items)

    def start(self):
        self.socketio.run(self.app, debug=True)
