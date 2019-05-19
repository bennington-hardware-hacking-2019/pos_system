# -*- coding: utf-8 -*-

from RPi.GPIO import *
import time
import exceptions

rest = .0001


class Wiegand(object):
    def __init__(self):
        # set data line 0 to be input from pin 13
        self.data0 = 13

        # set data line 1 to be input from pin 15
        self.data1 = 15

        # falicity code is set to be 32 for our use case
        self.facility = 32

    def setup(self):
        """set data pins to input pins"""
        setwarnings(False)
        setmode(BOARD)

        setup(self.data0, IN)
        setup(self.data1, IN)

    def read(self):
        """return the card reading value as an integer format"""
        capture = ''
        while True:
            if input(self.data0) == LOW:
                capture += '0'
                time.sleep(rest)

            elif input(self.data1) == LOW:
                capture += '1'
                time.sleep(rest)

            # Evaluates to true if there are no incoming bits
            elif len(capture) == 26:
                # throws error if one side has the wrong parity
                if int(capture[1:9], 2) != 32:
                    raise exceptions.FacilityError

                # throws error if one side has the wrong parity
                if capture[0:13].count('1') % 2 != 0 or \
                   capture[13:26].count('1') % 2 == 0:
                    raise exceptions.ReadError

                # return an integer representation of an array of bits
                return int(capture[11:25], 2)
