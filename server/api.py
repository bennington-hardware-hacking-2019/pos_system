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
            return render_template("base.html.j2", variable="Oy")

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
            #postgres for card - long term
            #get the pin from the login form - temporary
            pin = int(request.form['pin'])

            #if password/card verified

            if (pin == 123):
                session['username'] = 'admin' #Temporary
                return render_template('inventory.html')
            else:
                return redirect(url_for('login')) #needs testing

        @self.app.route('/admin/create', methods = ['GET', 'POST'])
        def create():
            if 'username' in session:
                if request.method == 'POST':
                    name = request.form['name']
                    desc = request.form['desc']
                    cost = request.form['cost']

                    #insert this stuff into whatever
                    db.create(name, desc, cost)

                    return redirect(url_for('items'))
                elif request.method == 'GET':
                    return render_template('create.html')
            else:
                return redirect(url_for('login')) #needs testing

        #
        # Vue.js API endpoints
        #
        @self.app.route('/items', methods = ['GET'])
        def items():
            #postgres
            item = db.items()
            return render_template('data.html', items=items)

    def start(self):
    # self.app.run(debug=True)
        self.socketio.run(self.app, debug=True)
