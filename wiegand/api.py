#!/usr/bin/python3
from RPi.GPIO import *
import time
import json

class Wiegand26:
    #Reads pin numbers for input pins from JSON
    #Facility number is also set from JSON
    def __init__(self):
        config = {}
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        self.data0 = config["data0"]
        self.data1 = config["data1"]
        self.facility = config["facility"]

    #Sets data pins to IN
    def setup(self):
        setwarnings(False)
        setmode(BOARD)
        setup(self.data0, IN)
        setup(self.data1, IN)

    # When Card returns wrong Facility 
    class FacilityError(Exception):
        pass

    # When Card returns wrong bit parity  
    class ReadError(Exception):
        pass

    # Loops until Card is detected and returns ID value
    def read(self):
        start = time.time()
        capture = ''
        while True:
            if input(self.data0) == LOW:
                capture += '0'
                time.sleep(.0001)
                start = time.time()
            elif input(self.data1) == LOW:
                capture += '1'
                time.sleep(.0001)
                start = time.time()
            # Evaluates to true if there are no incoming bits
            elif time.time() - start > .5 and capture != '':
                # Throws error if one side has the wrong parity
                if int(capture[1:9], 2) != 32:
                    raise self.FacilityError

                # Throws error if one side has the wrong parity
                if capture[0:13].count('1') % 2 != 0 or \
                   capture[13:26].count('1') % 2 == 0:
                    raise self.ReadError

                return int(capture[11:25], 2)

# Check a single card's ID
if __name__ == "__main__":
    wiegand = Wiegand26()
    wiegand.setup()
    print("Card Number: " + str(wiegand.read()))
 
