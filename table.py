#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
Shows a table with the credit schedule.
"""

__author__ = "Sofie & Bernd Krietenstein"
__copyright__ = "Copyright (C) 2018 Sofie & Bernd Krietenstein"
__license__ = "see LICENSE file"

import sys

from PyQt5.QtWidgets import (
    QDialog,
    QApplication,
    QWidget,
    QPushButton,
    QAction,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QVBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class TableDialog(QDialog):

    def __init__(self, parent=None):
        super(TableDialog, self).__init__(parent)
        self.title = 'Schedule'
        self.width = 600
        self.height = 600
        pg = parent.frameGeometry()
        self.left = pg.left() + pg.width() / 2 - self.width / 2
        self.top = pg.top() + pg.height() / 2 - self.height / 2
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self._table_widget = QTableWidget()
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self._table_widget)
        self.layout.addWidget(close_button)
        self.setLayout(self.layout)

        # Set size policy
        self._table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        # Cosmetics
        self._table_widget.horizontalHeader().setStyleSheet(
            "::section { background-color:lightGray }")

    def show_table(self, verlauf, start_date):
        """
        Shows the table.

        :param verlauf (list of KreditverlaufsZwischenstand objects): 
               The schedule
        :param start_date (QDate): start of the schedule
        """
        self._table_widget.clear()
        self._table_widget.setRowCount(len(verlauf))
        self._table_widget.setColumnCount(4)

        self._table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("Interest"))
        self._table_widget.setHorizontalHeaderItem(1, QTableWidgetItem("Rate of\nRedemption"))
        self._table_widget.setHorizontalHeaderItem(2, QTableWidgetItem("Unscheduled\nRedemption"))
        self._table_widget.setHorizontalHeaderItem(3, QTableWidgetItem("Balance"))

        i = 0
        for zwischenstand in verlauf:
            monat   = QTableWidgetItem(self.calculate_date(start_date, zwischenstand.Monat))
            zins    = QTableWidgetItem("{:.2f}".format(zwischenstand.Zinsanteil))
            tilgung = QTableWidgetItem("{:.2f}".format(zwischenstand.Tilgungsanteil))
            soti    = QTableWidgetItem("{:.2f}".format(zwischenstand.Sondertilgungsanteil))
            rest    = QTableWidgetItem("{:.2f}".format(zwischenstand.Restschuld))
            monat.setTextAlignment(Qt.AlignRight)
            zins.setTextAlignment(Qt.AlignRight)
            tilgung.setTextAlignment(Qt.AlignRight)
            soti.setTextAlignment(Qt.AlignRight)
            rest.setTextAlignment(Qt.AlignRight)
            self._table_widget.setVerticalHeaderItem(i, monat)
            self._table_widget.setItem(i, 0, zins)
            self._table_widget.setItem(i, 1, tilgung)
            self._table_widget.setItem(i, 2, soti)
            self._table_widget.setItem(i, 3, rest)
            i += 1

        # self._table_widget.move(0,0)

    def calculate_date(self, start_date, month):
        """
        Calculates the date month months after the start date.

        :param start_date (QDate): stat date
        :param month (int): n-th month after sart date
        :return: string representation of the date
        :rtype: str
        """
        current_date = start_date.addMonths(month - 1)
        return "{}/{}".format(current_date.month(), current_date.year())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main = TableDialog()
    main.show()

    sys.exit(app.exec_())