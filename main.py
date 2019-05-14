# -*- coding: utf-8 -*-

from pn532.api import PN532
from prx_3hc.api import PRX_3HC


if __name__== "__main__":
    # setup:
    # - prx_3hc to read Bennington cards
    # - pn532 to read store items
    # - store to get/put items to the store
    # - payment_processor to read store items
    prx_3hc = PRX_3HC()
    pn532 = PN532()

    # keep listening to for read
    print(prx_3hc.read())
    print(pn532.read())
