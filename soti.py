#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
A dialog for entering extra dwon payments.
"""
import sys

from PyQt5.QtWidgets import (
    QDialog,
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QDateEdit,
    QDateTimeEdit,
    QAction,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtCore import (
    Qt,
    QDate
)
from PyQt5.QtGui import QIcon
 
class SotiDialog(QDialog):
    
    def __init__(self, parent=None, sotis=None):
        super(SotiDialog, self).__init__(parent)
        self.title = 'Enter Unscheduled Redemptions'
        self.width = 600
        self.height = 600
        pg = parent.frameGeometry()
        self.left = pg.left() + pg.width() / 2 - self.width / 2
        self.top = pg.top() + pg.height() / 2 - self.height / 2
        
        self._table_widget = None
        
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self._table_widget = QTableWidget()
        self._table_widget.setRowCount(1)
        self._table_widget.setColumnCount(2)
        self._table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("Date"))
        self._table_widget.setHorizontalHeaderItem(1, QTableWidgetItem("Payment"))

        # Add first row
        month_edit = QDateEdit(QDate.currentDate())     
        month_edit.setDisplayFormat("MM/yyyy")
        month_edit.currentSection = QDateTimeEdit.MonthSection
        self._table_widget.setCellWidget(0, 0, month_edit)
        self._table_widget.setItem(0, 1, QTableWidgetItem("Enter Amount"))

        add_button = QPushButton('+')
        add_button.clicked.connect(self._add_payment)
        remove_button = QPushButton('-')
        remove_button.clicked.connect(self._remove_payment)
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)
 
        # Vertical layout for +- buttons
        table_buttons_layout = QVBoxLayout()
        table_buttons_layout.addWidget(add_button)
        table_buttons_layout.addWidget(remove_button)

        # Horizontal layout for table and buttons
        table_layout = QHBoxLayout()
        table_layout.addWidget(self._table_widget)
        table_layout.addLayout(table_buttons_layout)

        # Vertical layout for table/buttons and close button
        layout = QVBoxLayout()
        layout.addLayout(table_layout)
        layout.addWidget(close_button)
        self.setLayout(layout)

    def _add_payment(self):
        """
        Add a line with a new extra payment.
        """
        self._table_widget.insertRow(self._table_widget.rowCount())
        current_row = self._table_widget.rowCount() - 1
        month_edit = QDateEdit(QDate.currentDate())
        month_edit.setDisplayFormat("MM/yyyy")
        month_edit.currentSection = QDateTimeEdit.MonthSection
        self._table_widget.setCellWidget(current_row, 0, month_edit)
        self._table_widget.setItem(current_row, 1, QTableWidgetItem("Enter Amount"))

    def _remove_payment(self):
        """
        Remove the current row.
        """
        self._table_widget.removeRow(self._table_widget.currentRow())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main = SotiDialog()
    main.show()

    sys.exit(app.exec_())