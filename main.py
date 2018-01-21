#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
Root file for GUI application.
"""

__author__ = "Sofie & Bernd Krietenstein"
__copyright__ = "Copyright (C) 2018 Sofie & Bernd Krietenstein"
__license__ = "see LICENSE file"

import sys

from PyQt5.QtWidgets import QApplication, QWidget

import dialog

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    DIALOG = dialog.MainDialog()
    sys.exit(APP.exec_())
