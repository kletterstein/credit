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
    QMessageBox,
    QAction,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy
)
from PyQt5.QtCore import (
    Qt,
    QDate
)
from PyQt5.QtGui import (
    QPalette,
    QIcon
)

import conf
import log
 
class SotiDialog(QDialog):
    
    def __init__(self, parent=None, sotis=None):
        super(SotiDialog, self).__init__(parent)
        self.title = 'Enter Unscheduled Redemptions'
        self.width = 600
        self.height = 600
        if parent:
            pg = parent.frameGeometry()
            self.left = pg.left() + pg.width() / 2 - self.width / 2
            self.top = pg.top() + pg.height() / 2 - self.height / 2
        else:
            self.left = 200
            self.top = 200
        
        self._table_widget = None
        
        self.initUI()

        if sotis:
            for payment in sotis:
                self._add_payment(payment)

        self._table_widget.clearFocus()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self._table_widget = QTableWidget()
        # self._table_widget.setRowCount(1)
        self._table_widget.setColumnCount(2)
        self._table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("Date"))
        self._table_widget.setHorizontalHeaderItem(1, QTableWidgetItem("Payment"))

        add_button = QPushButton('+')
        add_button.clicked.connect(self._add_payment)
        remove_button = QPushButton('-')
        remove_button.clicked.connect(self._remove_payment)
        sort_button = QPushButton("Sort")
        sort_button.clicked.connect(self._sort_table)
        close_button = QPushButton('Close')
        close_button.clicked.connect(self._close)

        # Vertical layout for +- and sort buttons
        table_buttons_layout = QVBoxLayout()
        table_buttons_layout.addWidget(add_button)
        table_buttons_layout.addWidget(remove_button)
        table_buttons_layout.addWidget(sort_button)

        # Horizontal layout for table and buttons
        table_layout = QHBoxLayout()
        table_layout.addWidget(self._table_widget)
        table_layout.addLayout(table_buttons_layout)

        # Vertical layout for table/buttons and close button
        layout = QVBoxLayout()
        layout.addLayout(table_layout)
        layout.addWidget(close_button)
        self.setLayout(layout)

        # Set size policy
        self._table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        # Cosmetics
        self._table_widget.horizontalHeader().setStyleSheet(
            "::section { background-color:lightGray }")

    def _add_payment(self, payment=None):
        """
        Add a line with a new extra payment.

        :param payment (tuple(str, float)): Extra payment for a month.
        """
        self._table_widget.insertRow(self._table_widget.rowCount())
        current_row = self._table_widget.rowCount() - 1
        if payment:
            month = QDate.fromString(payment[0], conf.DATE_FORMAT)
            amount = payment[1]
        else:
            month = QDate.currentDate()
            amount = 0.0
        month_edit = QDateEdit(month)
        month_edit.setDisplayFormat(conf.DATE_FORMAT)
        month_edit.currentSection = QDateTimeEdit.MonthSection
        self._table_widget.setCellWidget(current_row, 0, month_edit)
        self._table_widget.setItem(current_row, 1, QTableWidgetItem(str(amount)))

    def _remove_payment(self):
        """
        Remove the current row.
        """
        self._table_widget.removeRow(self._table_widget.currentRow())

    def _sort_table(self):
        """
        Sort the table date-wise
        """
        # later...
        pass

    def _close(self):
        """
        Close dialog after successful validation.
        """
        # Implement validation here
        validation_error = self._validate()
        if not validation_error:
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Validation error",
                validation_error)

    def _validate(self):
        """
        Validate table. Payments must be convertable into float. Only one
        payment per month is allowed.
        """
        # Make sure, payments are convertable into float.
        current_row = 0
        try:
            for row_no in range(self._table_widget.rowCount()):
                current_row = row_no
                float(self._table_widget.item(row_no, 1).text())
        except ValueError:
            return "Invalid values in table in row {}".format(current_row + 1)
        # Make sure, only on payment per month is made
        row_count = self._table_widget.rowCount()
        if row_count > 1:
            for row_no in range(row_count):
                for row_no2 in range(row_no + 1, row_count):
                    date1 = self._table_widget.cellWidget(row_no, 0).date()
                    date2 = self._table_widget.cellWidget(row_no2, 0).date()
                    if date1 == date2:
                        return (
                            "Ambiguous payments in rows {} and {}\n"
                            "Only one payment per month is allowed.".format(
                                row_no + 1,
                                row_no2 + 1))
        return None

    @property
    def payments(self):
        """
        :returns: List of extra payments.
        :rtype: list(QDate, float)
        """
        payment_list = []
        try:
            for row_no in range(self._table_widget.rowCount()):
                date_edit = self._table_widget.cellWidget(row_no, 0)
                date = date_edit.date().toString(conf.DATE_FORMAT)
                amount = float(self._table_widget.item(row_no, 1).text())
                payment_list.append((date, amount))
        except Exception as ex:
            log.LOGGER.error(ex)
        return payment_list

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = SotiDialog()
    main.show()

    sys.exit(app.exec_())
