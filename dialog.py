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
    QPushButton
)
from PyQt5.QtCore import (
    QDate
)
from kredit import AnnuitaetenKredit
from plot import PlotWindow
from table import TableWindow


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

        self._kredit_summe_edit.setText("300000")
        self._tilgung_prozent_edit.setText("1")
        self._zins_prozent_edit.setText("1.5")

    def init_ui(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Annuitätsdarlehenrechner')

        self.init_layout()
        self.init_input_fields()
        self.init_calc_buttons()
        self.init_output_fields()
        self.init_show_buttons()
        self.init_close_button()

        self._calc_button.clicked.connect(self.calc_button_pressed)
        self._plot_button.clicked.connect(self.plot_button_pressed)
        self._table_button.clicked.connect(self.table_button_pressed)
        self._close_button.clicked.connect(self.close_button_pressed)

        self.show()

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

    def init_input_fields(self):
        self._data_grid.addWidget(QLabel("Kreditsumme [€]"), 0,0)
        self._data_grid.addWidget(QLabel("Tilgung [%]"), 1, 0,)
        self._data_grid.addWidget(QLabel("Nominalzins [%]"), 2, 0)
        self._data_grid.addWidget(QLabel("Startdatum"), 3, 0)
        self._kredit_summe_edit = QLineEdit()
        self._tilgung_prozent_edit = QLineEdit()
        self._zins_prozent_edit = QLineEdit()
        self._start_month_edit = QDateEdit(QDate.currentDate())     
        self._start_month_edit.setDisplayFormat("MM/yyyy")
        self._start_month_edit.currentSection = QDateTimeEdit.MonthSection
        self._data_grid.addWidget(self._kredit_summe_edit, 0, 1)
        self._data_grid.addWidget(self._tilgung_prozent_edit, 1, 1)
        self._data_grid.addWidget(self._zins_prozent_edit, 2, 1)
        self._data_grid.addWidget(self._start_month_edit, 3, 1)

    def init_calc_buttons(self):
        self._calc_button = QPushButton("Berechnen")
        self._soti_button = QPushButton("Sondertilgungen")
        hbox = QHBoxLayout()
        hbox.addWidget(self._calc_button)
        hbox.addWidget(self._soti_button)
        self._data_grid.addLayout(hbox, 4, 0, 1, 2)
       
    def init_output_fields(self):
        self._monats_rate_label = QLabel("...")
        self._laufzeit_label = QLabel("...")
        self._kosten_label = QLabel("...")
        self._data_grid.addWidget(QLabel("Monatsrate [€]:"), 5, 0)
        self._data_grid.addWidget(QLabel("Laufzeit:"), 6, 0)
        self._data_grid.addWidget(QLabel("Kosten [€]:"), 7, 0)
        self._data_grid.addWidget(self._monats_rate_label, 5, 1)
        self._data_grid.addWidget(self._laufzeit_label, 6, 1)
        self._data_grid.addWidget(self._kosten_label, 7, 1)

    def init_show_buttons(self):
        self._table_button = QPushButton("Zeige Kreditverlauf")
        self._plot_button = QPushButton("Zeige Grafik")
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
                self._table_window.show()
            self._table_window.show_table(self._kredit_verlauf, self._start_month_edit.date())

    def plot_button_pressed(self, e):
        if len(self._kredit_verlauf):
            if not self._window:
                self._window = PlotWindow(self)
                self._window.show()
            self._window.plot(self._kredit_verlauf)

    def close_button_pressed(self):
        self.close()