#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
Collect error messages.
"""

__author__ = "Sofie & Bernd Krietenstein"
__copyright__ = "Copyright (C) 2018 Sofie & Bernd Krietenstein"
__license__ = "see LICENSE file"

import logging

_LEVEL = logging.DEBUG

LOGGER = logging.getLogger('errors')
LOGGER.setLevel(_LEVEL)
_CONSOLE_HANDLER = logging.StreamHandler()
_CONSOLE_HANDLER.setLevel(logging.ERROR)
_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_CONSOLE_HANDLER.setFormatter(_FORMATTER)
LOGGER.addHandler(_CONSOLE_HANDLER)
