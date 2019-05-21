# when card returns wrong facility 
class FacilityError(Exception):
	pass

# when card returns wrong bit parity  
class ReadError(Exception):
    pass
