#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import server

if __name__== "__main__":
	poss = server.Server()
	poss.setup(True)
	poss.start(True)
