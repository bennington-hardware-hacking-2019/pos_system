from RPi.GPIO import *
import time
import exceptions

class Wiegand26:
    # Reads pin numbers for input pins from JSON
    # Facility number is also set from JSON
    def __init__(self):
        self.data0 = 13
        self.data1 = 15
        self.facility = 32

    # Sets data pins to IN
    def setup(self):
        setwarnings(False)
        setmode(BOARD)
        setup(self.data0, IN)
        setup(self.data1, IN)

    # Loops until Card is detected and returns ID value
    def read(self):
        capture = ''
        while True:

            if input(self.data0) == LOW:
                capture += '0'
                time.sleep(.0001)

            elif input(self.data1) == LOW:
                capture += '1'
                time.sleep(.0001)

            # Evaluates to true if there are no incoming bits
            elif len(capture) == 26:

                # Throws error if one side has the wrong parity
                if int(capture[1:9], 2) != 32:
                    raise exceptions.FacilityError

                # Throws error if one side has the wrong parity
                if capture[0:13].count('1') % 2 != 0 or \
                   capture[13:26].count('1') % 2 == 0:
                    raise exceptions.ReadError

                return int(capture[11:25], 2)
