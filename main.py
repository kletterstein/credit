#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
Root file für die GUI-Anwendung.
"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget

import dialog

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    DIALOG = dialog.MainDialog()
    sys.exit(APP.exec_())