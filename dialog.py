#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
Der Hauptdialog für den Annuitätendarlehensrechner.
"""

import matplotlib.pylab as pylab
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QDateEdit,
    QDateTimeEdit,
    QPushButton,
    QFileDialog    
)
from PyQt5.QtCore import (
    QDate
)
import os
import pathlib
import yaml

from kredit import AnnuitaetenKredit
from plot import PlotWindow
from table import TableWindow


class CreditSettings(object):
    def __init__(self):
        """
        Konstruktor.
        """
        self.kreditsumme = 0.0
        self.zins = 0.0
        self.tilgung = 0.0
        self.start_date = "01/2000"

class MainDialog(QWidget):
    """
    Der Hauptdialog für den Annuitätendarlehensrechner.
    """
    def __init__(self):
        super().__init__()

        self._vbox = None
        self._data_grid = None
        self._hbox_buttons = None
        self._hbox_close_button = None
        self._kredit_summe_edit = None
        self._tilgung_prozent_edit = None
        self._zins_prozent_edit = None
        self._start_month_edit = None
        self._monats_rate_label = None
        self._laufzeit_label = None
        self._kosten_label = None
        self._load_button = None
        self._save_button = None
        self._calc_button = None
        self._soti_button = None
        self._table_button = None
        self._table_button = None
        self._plot_button = None
        self._close_button = None

        self._window = None
        self._table_window = None

        self._kredit_verlauf = []

        self.init_ui()

        # Load/initialize settings
        self._credit_dir = os.path.join(pathlib.Path.home(), '.credit')
        self._credit_settings_file = os.path.join(self._credit_dir, 'settings.yaml')
        if not os.path.exists(self._credit_dir):
            os.makedirs(self._credit_dir)
        if not os.path.exists(self._credit_settings_file):
            self._settings = CreditSettings()
            self._save_settings(self._credit_settings_file)
        self._load_settings(self._credit_settings_file)

    def init_ui(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Annuity Loan Calculator')

        self.init_layout()
        self.init_project_buttons()
        self.init_input_fields()
        self.init_calc_buttons()
        self.init_output_fields()
        self.init_show_buttons()
        self.init_close_button()

        self._load_button.clicked.connect(self.load_button_pressed)
        self._save_button.clicked.connect(self.save_button_pressed)
        self._calc_button.clicked.connect(self.calc_button_pressed)
        self._plot_button.clicked.connect(self.plot_button_pressed)
        self._table_button.clicked.connect(self.table_button_pressed)
        self._close_button.clicked.connect(self.close_button_pressed)

        self.show()

    def _load_settings(self, file_name):
        if os.path.exists(file_name):
            try:
                self._settings = yaml.load(open(file_name, 'r'))
                self._kredit_summe_edit.setText("{:.2f}".format(self._settings.kreditsumme))
                self._tilgung_prozent_edit.setText("{:.2f}".format(self._settings.tilgung))
                self._zins_prozent_edit.setText("{:.2f}".format(self._settings.zins))
                self._start_month_edit.lineEdit().setText(self._settings.start_date)
            except yaml.YAMLError as ex:
                print(ex)
    
    def _save_settings(self, file_name):
        save_dir = os.path.dirname(file_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self._settings.kreditsumme = float(self._kredit_summe_edit.text())
        self._settings.zins = float(self._zins_prozent_edit.text())
        self._settings.tilgung = float(self._tilgung_prozent_edit.text())
        self._settings.start_date = self._start_month_edit.lineEdit().text()
        try:
            with open(file_name, mode='w') as file:
                file.write(yaml.dump(self._settings))
        except yaml.YAMLError as ex:
            print(ex)

    def init_layout(self):
        self._vbox = QVBoxLayout()
        self._data_grid = QGridLayout()
        self._hbox_buttons = QHBoxLayout()
        self._hbox_close_button = QHBoxLayout()

        self._vbox.addLayout(self._data_grid)
        self._vbox.addLayout(self._hbox_buttons)
        self._vbox.addLayout(self._hbox_close_button)
        self._vbox.addStretch(1)

        self.setLayout(self._vbox)

    def init_project_buttons(self):
        start_row = 0
        self._load_button = QPushButton("Load Project")
        self._save_button = QPushButton("Save Project")
        hbox = QHBoxLayout()
        hbox.addWidget(self._load_button)
        hbox.addWidget(self._save_button)
        self._data_grid.addLayout(hbox, start_row + 0, 0, 1, 2)

    def init_input_fields(self):
        start_row = 1
        self._data_grid.addWidget(QLabel("Loan Amount"), start_row + 0,0)
        self._data_grid.addWidget(QLabel("Down Payment [%]"), start_row + 1, 0,)
        self._data_grid.addWidget(QLabel("Nominal Interest [%]"), start_row + 2, 0)
        self._data_grid.addWidget(QLabel("Start Date"), start_row + 3, 0)
        self._kredit_summe_edit = QLineEdit()
        self._tilgung_prozent_edit = QLineEdit()
        self._zins_prozent_edit = QLineEdit()
        self._start_month_edit = QDateEdit(QDate.currentDate())     
        self._start_month_edit.setDisplayFormat("MM/yyyy")
        self._start_month_edit.currentSection = QDateTimeEdit.MonthSection
        # self._start_month_edit.setCalendarPopup(True)        
        self._data_grid.addWidget(self._kredit_summe_edit, start_row + 0, 1)
        self._data_grid.addWidget(self._tilgung_prozent_edit, start_row + 1, 1)
        self._data_grid.addWidget(self._zins_prozent_edit, start_row + 2, 1)
        self._data_grid.addWidget(self._start_month_edit, start_row + 3, 1)

    def init_calc_buttons(self):
        start_row = 5
        self._calc_button = QPushButton("Calculate")
        self._soti_button = QPushButton("Extra Down Payments")
        hbox = QHBoxLayout()
        hbox.addWidget(self._calc_button)
        hbox.addWidget(self._soti_button)
        self._data_grid.addLayout(hbox, start_row + 0, 0, 1, 2)
       
    def init_output_fields(self):
        start_row = 6
        self._monats_rate_label = QLabel("...")
        self._laufzeit_label = QLabel("...")
        self._kosten_label = QLabel("...")
        self._data_grid.addWidget(QLabel("Monthly Rate:"), start_row + 0, 0)
        self._data_grid.addWidget(QLabel("Period:"), start_row + 1, 0)
        self._data_grid.addWidget(QLabel("Total Interest:"), start_row + 2, 0)
        self._data_grid.addWidget(self._monats_rate_label, start_row + 0, 1)
        self._data_grid.addWidget(self._laufzeit_label, start_row + 1, 1)
        self._data_grid.addWidget(self._kosten_label, start_row + 2, 1)

    def init_show_buttons(self):
        self._table_button = QPushButton("Show Schedue")
        self._plot_button = QPushButton("Show Chart")
        self._hbox_buttons.addWidget(self._table_button)
        self._hbox_buttons.addWidget(self._plot_button)

    def init_close_button(self):
        self._close_button = QPushButton("Close")
        self._hbox_close_button.addStretch(1)
        self._hbox_close_button.addWidget(self._close_button)

    @property
    def summe(self):
        """
        :returns Betrag des Kredits in Euro
        """
        return float(self._kredit_summe_edit.text())

    @property
    def tilgung(self):
        """
        :returns Tilgungssatz in %
        """
        return float(self._tilgung_prozent_edit.text())

    @property
    def zins(self):
        """
        :returns Zinssatz in %
        """
        return float(self._zins_prozent_edit.text())

    @property
    def monatsrate(self):
        raise NotImplementedError("Setting is not allowed")

    @monatsrate.setter
    def monatsrate(self, x):
        self._monats_rate_label.setText("{0:.2f}".format(x))

    @property
    def laufzeit(self):
        raise NotImplementedError("Setting is not allowed")

    @laufzeit.setter
    def laufzeit(self, x):
        self._laufzeit_label.setText(str(x))

    @property
    def kosten(self):
        raise NotImplementedError("Setting is not allowed")

    @kosten.setter
    def kosten(self, x):
        """
        :param x (float): Gesamtkosten des Kredits.
        """
        self._kosten_label.setText("{0:.2f}".format(x))

    def load_button_pressed(self, e):
        file_name = QFileDialog.getOpenFileName(
            self,
            "Open Project File",
            str(pathlib.Path.home()),
            "Credit Project Files (*.yaml)")[0]
        self._load_settings(file_name)

    def save_button_pressed(self, e):
        file_name = QFileDialog.getSaveFileName(
            self,
            "Save Project File",
            str(pathlib.Path.home()),
            "Credit Project Files (*.yaml)")[0]
        self._save_settings(file_name)

    def calc_button_pressed(self, e):
        kredit = AnnuitaetenKredit(self.summe, self.tilgung, self.zins)
        self._kredit_verlauf = kredit.berechne_kreditverlauf()
        self.monatsrate = kredit.Monatsrate
        self.laufzeit = "{0:d} Jahre {1:d} Monate".format(
            int(self._kredit_verlauf[-1].Monat) // 12,
            self._kredit_verlauf[-1].Monat % 12)
        self.kosten = kredit.GesamtKosten
        
    def table_button_pressed(self, e):
        if len(self._kredit_verlauf):
            if not self._table_window:
                self._table_window = TableWindow(self)
                self._table_window.setModal(True)
            self._table_window.show_table(self._kredit_verlauf, self._start_month_edit.date())
            self._table_window.show()

    def plot_button_pressed(self, e):
        if len(self._kredit_verlauf):
            if not self._window:
                self._window = PlotWindow(self)
                self._window.setModal(True)
            self._window.plot(self._kredit_verlauf)
            self._window.show()

    def close_button_pressed(self):
        self._save_settings(self._credit_settings_file)
        self.close()