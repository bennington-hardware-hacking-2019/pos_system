# -*- coding: utf-8 -*-

from RPi.GPIO import *
import time

from . import exceptions

rest = .0001


# Wiegand is the NFC card reader module
class Wiegand(object):
	def __init__(self):
		# set data line 0 to be input from pin 18
		self.data0 = 18

		# set data line 1 to be input from pin 22
		self.data1 = 22

		# facility code is set to be 32 for our use cases
		self.facility = 32

	def setup(self):
		"""set data pin to input pin"""
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

			# evaluates to true if there are no incoming bits
			elif len(capture) == 26:
				# throws error if the facility code doesn't match
				if int(capture[1:9], 2) != self.facility:
					raise exceptions.FacilityError

				# throws error if one side has the wrong parity
				if capture[0:13].count('1') % 2 != 0 or \
				   capture[13:26].count('1') % 2 == 0:
					raise exceptions.ReadError

				# return an integer representation of an array of bits
				return int(capture[11:25], 2)

	def sim_setup(self):
		"""FIXME - simulate setup, only used for testing purposes"""
		# print("wiegand is setting up")
		pass

	def sim_read(self):
		"""FIXME - simulate reading, only used for testing purposes"""
		time.sleep(rest)
		return 7114
