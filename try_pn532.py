#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tag_reader

if __name__== "__main__":
    reader = tag_reader.PN532()
    reader.setup()
    print(reader.read())
