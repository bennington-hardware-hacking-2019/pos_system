from .context import payment_processor

import unittest

class StripeTestAccount(unittest.TestCase):
    def test_is_paid(self):
        pay = payment_processor.PaymentProcessor()
        pay.setup()
        self.assertTrue(pay.is_paid("ch_1EbaDcE9aH1iiXRr8s1DdXBX"))
