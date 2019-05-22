import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tag_reader
import db


treader = tag_reader.PN532()

treader.simulate_setup()

database = db.DB()


print("Please tap the tag")

tag = treader.simulate_read()
print(tag)
print("Item name:")
item_name = input()
print("Item description:")
item_desc = input()
print("Item cost:")
item_cost = input()

# item_name = request.form['item_name']
# item_desc = request.form['item_desc']
# item_price = request.form['item_price']

database.add_item(tag,item_name,desc,cost)
