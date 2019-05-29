#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import card_reader

if __name__== "__main__":
    reader = card_reader.Wiegand()
    reader.setup()
    print(reader.read())
