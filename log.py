#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
Collect error messages.
"""
import logging

_LEVEL = logging.DEBUG

LOGGER = logging.getLogger('errors')
LOGGER.setLevel(_LEVEL)
_CONSOLE_HANDLER = logging.StreamHandler()
_CONSOLE_HANDLER.setLevel(logging.ERROR)
_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_CONSOLE_HANDLER.setFormatter(_FORMATTER)
LOGGER.addHandler(_CONSOLE_HANDLER)
