# pn532

PN532 NFC/RFID Native Python API for your Raspberry Pi.

## Installing

To install the package, simply issue a git clone:
```sh
git clone https://github.com/hoanhan101/pn532.git
```

## Using

### API

There are 2 main methods that we care about at the moment, one is `setup()`
and one is `read()`.
- `setup()` takes an optional boolean parameter, `enable_logging`, which is to
  enable debugging messages. This should be always be called first so that the
  sensor is initialized and setup properly.
- `read()` returns the card reading value as an array of 11-bytes. This will block and
  only return once a card is detected. Sample readings can be found [here](output/raw.txt).

### Examples

Setup the device, get the reading and print it to the console.
```python
from pn532.api import PN532


if __name__== "__main__":
    nfc = PN532()

    # setup the device
    nfc.setup()

    # keep reading until a value is returned
    read = nfc.read()
    print(read)
```

## Developing

To install necessary development tools:
```sh
make init
```

To run tests:
```sh
make test
```

## Reference
- [PN532 data sheet](https://www.nxp.com/docs/en/nxp/data-sheets/PN532_C1.pdf)
- [PN532 user manual](https://www.nxp.com/docs/en/user-guide/141520.pdf)
