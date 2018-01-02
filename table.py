#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
Zeigt eine Tabelle mit dem Verlauf der Restschulden.
"""
import sys

from PyQt5.QtWidgets import (
    QDialog,
    QApplication,
    QWidget,
    QAction,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
 
class TableWindow(QDialog):
 
    def __init__(self, parent=None):
        super(TableWindow, self).__init__(parent)
        self.title = 'Kreditverlauf'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.tableWidget = QTableWidget()
 
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
 
    def show_table(self, verlauf, start_date):
        """
        Zeigt die Tabelle mit dem Kreditverlauf.

        :param verlauf (List von KreditverlaufsZwischenstand Objekten): 
               Der Kreditverlauf
        :param start_date (QDate): Start der Kreditlaufzeit
        """
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(verlauf))
        self.tableWidget.setColumnCount(4)

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Zins"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Tilgung"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Sondertilgung"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Restschuld"))

        i = 0
        for zwischenstand in verlauf:
            monat   = QTableWidgetItem(self.calculate_date(start_date, zwischenstand.Monat))
            zins    = QTableWidgetItem("{:.2f}".format(zwischenstand.Zinsanteil))
            tilgung = QTableWidgetItem("{:.2f}".format(zwischenstand.Tilgungsanteil))
            soti    = QTableWidgetItem("{:.2f}".format(zwischenstand.Sondertilgunsanteil))
            rest    = QTableWidgetItem("{:.2f}".format(zwischenstand.Restschuld))
            monat.setTextAlignment(Qt.AlignRight)
            zins.setTextAlignment(Qt.AlignRight)
            tilgung.setTextAlignment(Qt.AlignRight)
            soti.setTextAlignment(Qt.AlignRight)
            rest.setTextAlignment(Qt.AlignRight)
            self.tableWidget.setVerticalHeaderItem(i, monat)
            self.tableWidget.setItem(i, 0, zins)
            self.tableWidget.setItem(i, 1, tilgung)
            self.tableWidget.setItem(i, 2, soti)
            self.tableWidget.setItem(i, 3, rest)
            i += 1

        self.tableWidget.move(0,0)

    def calculate_date(self, start_date, month):
        """
        Berechnet das Datum, das month Monate nach dem Startdatum liegt.

        :param start_date (QDate): Startdatum
        :param month (int): n. Monat nach dem Startdatum
        :return: String Darstellung des aktuellen Monats
        :rtype: str
        """
        current_date = start_date.addMonths(month - 1)
        return "{}/{}".format(current_date.month(), current_date.year())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main = TableWindow()
    main.show()

    sys.exit(app.exec_())