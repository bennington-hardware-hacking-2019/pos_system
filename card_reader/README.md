# Wiegand 26 Bit Reader
Module for reading Wiegand 26 Bit Output
on a Raspberry Pi 3

## Source
Clone the repository using:
``` 
git clone "https://github.com/bennington-hardware-hacking-2019/wiegand26.git"
```

## Hardware Setup
1. Power the reader.
2. Connect the data0 and data0
to GPIO pins on the Pi. 
3. Change the values of `data0` and `data1`
in `config.json` to the physical pins.
	- Note: If you wish to change the
	facility number, this can also be found
	in `config.json` under `facility`.

## Basic Usage
To read the value of a single card, just run
`./wiegand_26_bit.py` and hold the target 
card up to the reader.

## Functionality and API
All readings are processed by the `Wiegand26`
object, so initialization of the `Wiegand26`
allows interface with Wiegand Input.

`Wiegand26` Functions:

- `setup` - Configures the Pi to allow input
to be read. This function should always 
be run before anything else *(other than*
`__init__`*)*
- `read` - Returns the Card Number as an
integer. Also, it can raise the following
exceptions.
	- `FacilityError` - Exception for
	when the Facility does not match
	the preconfigured one.
	- `ReadError` - Exception when the
	card is read incorrectly. This is
	caught by the parity bits.
