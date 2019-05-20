# -*- coding: utf-8 -*-

import os
import sys
# make it so tests behave as if they were run in the project directory (pretend we are in the outside folder)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import payment_processor
