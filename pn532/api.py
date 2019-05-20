# -*- coding: utf-8 -*-
#
# api.py contains a set of core functions
#

from . import register
from .smbus2.smbus2 import SMBus, i2c_msg

import time
import logging

# rest time in second betweet each read/write transaction
REST_INTERVAL = 0.5 

# maximum block size for each read transaction
BLOCK_SIZE = 20

class PN532(object):
    def __init__(self):
        # i2c device address
        self.address = register.PN532_DEFAULT_ADDRESS

        # smbus object
        self.bus = SMBus(1)

        # logger object
        self.logger = logging.getLogger()

    def setup(self, enable_logging=False):
        """setup the device"""
        if enable_logging:
            self.use_logging()

        self.sam_config()

    def use_logging(self):
        """use debug logging"""
        # setup a custom formatting message
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-5s | %(message)s")
        )
        self.logger.addHandler(handler)

        # set logging level to DEBUG
        self.logger.setLevel(logging.DEBUG)

    def read(self):
        """return a raw reading value as an array of bytes"""
        self.in_list_passive_target()

        while True:
            read = self.read_addr(BLOCK_SIZE)
            # check the first 3 bytes to see if a card is detected or not
            if read[:3] != [0x00, 0x80, 0x80]:
                # TODO - the first 9 bytes are configs bytes so we're not really
                # interested in getting these at the moment, though they could
                # be used for validation in the future
                return read[9:]

    def sam_config(self):
        """send SAMConfiguration command"""
        self.write_addr(
            construct_frame([register.PN532_COMMAND_SAMCONFIGURATION, 0x01, 0x01, 0x00])
        )
        self.read_addr(BLOCK_SIZE)

    def in_list_passive_target(self):
        """send InListPassiveTarget command"""
        self.write_addr(
            construct_frame([register.PN532_COMMAND_INLISTPASSIVETARGET, 0x01, 0x00])
        )
        self.read_addr(BLOCK_SIZE)

    def write_addr(self, data):
        """write to its own address with given block data"""
        time.sleep(REST_INTERVAL)

        self.bus.write_i2c_block_data(self.address, self.address, data)
        self.logger.debug("write_addr: %s", data)

    def read_addr(self, length):
        """read from its own address a given-length of block data"""
        time.sleep(REST_INTERVAL)

        buf = []
        msg = i2c_msg.read(self.address, length)
        self.bus.i2c_rdwr(msg)

        for b in msg:
            buf.append(b)

        self.logger.debug("read_addr: %s", buf)
        return buf

def construct_frame(data):
    """construct frame for communicating between host controller and pn532"""
    # begin with 6-bytes frame structure
    buf = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    buf[0] = register.PN532_PREAMBLE
    buf[1] = register.PN532_STARTCODE1
    buf[2] = register.PN532_STARTCODE2
    buf[3] = len(data) + 1           # number of bytes in data and frame identifier field
    buf[4] = (~buf[3] & 0xFF) + 0x01 # packet length checksum
    buf[5] = register.PN532_HOSTTOPN532

    tmp_sum = register.PN532_HOSTTOPN532
    for b in data:
        tmp_sum += b
        buf.append(b)

    buf.append((~tmp_sum & 0xFF) + 0x01) # data checksum
    buf.append(register.PN532_POSTAMBLE)

    return buf
