# -*- coding: utf-8 -*-

from db import DB


if __name__== "__main__":
    db = DB()
    db.setup()
    print(db.get_item_status(66666))

    db.update_item_status(66666, "sold")

    print(db.get_item_status(66666))
