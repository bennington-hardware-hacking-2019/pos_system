# Exceptions for Wiegand 26 Bit Object

# When Card returns wrong Facility
class FacilityError(Exception):
	pass

# When Card returns wrong bit parity
class ReadError(Exception):
	pass
