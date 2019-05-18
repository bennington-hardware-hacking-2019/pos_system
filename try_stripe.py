# -*- coding: utf-8 -*-

from payment_processor.api import Payment_Processor


if __name__== "__main__":
    pay = Payment_Processor()
    pay.setup()

    print(pay.get_balance())
