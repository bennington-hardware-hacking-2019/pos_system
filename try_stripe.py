# -*- coding: utf-8 -*-

from payment_processor.api import Payment_Processor


if __name__== "__main__":
    pay = Payment_Processor()
    pay.setup()

    # print(pay.is_paid("ch_1EbaDcE9aH1iiXRr8s1DdXBX"))
    print(pay.get_charges(3))
