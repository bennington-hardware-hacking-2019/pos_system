#!/usr/bin/env python3
"""
	Author: matt n julian
	Date: may 13, 2019
"""
from flask import Flask, session, render_template, request, redirect, url_for
import psycopg2 as psyco
app = Flask(__name__)
app.secret_key = 'yagabeatsTHO'
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/help')
def help():
	return render_template('help.html')

@app.route('/info')
def info():
	return render_template('info.html')

@app.route('/login', methods = ['GET'])
def login():
	return render_template('login.html')

@app.route('/admin', methods = ['POST'])
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

@app.route('/admin/create', methods = ['POST'])
def create():
	if 'admin' in session:
		item_name = request.form['item_name']
		item_desc = request.form['item_desc']
		item_price = request.form['item_price']
	#insert this stuff into whatever


	else:
		return redirect(url_for('login')) #needs testing


#
# # Vue.js API endpoints
#

@app.route('/items', methods = ['GET'])
def items():
	#postgres
	return render_template('data.html', items=items)

if __name__ == "__main__":
	app.run()
