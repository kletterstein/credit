#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Calcuate the schedule of an annuity loan.
"""

__author__ = "Sofie & Bernd Krietenstein"
__copyright__ = "Copyright (C) 2018 Sofie & Bernd Krietenstein"
__license__ = "see LICENSE file"

class KreditverlaufsZwischenstand(object):
    """
    One line in a credit schedule.
    """
    def __init__(self, monat, zins, tilgung, soti, restschuld):
        """
        C'tor.

        :param monat (int): number of month in a credit schedule
        :param zins (float): interest part of this month's rate.
        :param tilgung (float): redemption part of this month's rate.
        :param soti (float): extra payment in this month.
        :param restschuld (float): Current balance after this month's rate was paid.
        """
        self.Monat = monat
        self.Zinsanteil = zins
        self.Tilgungsanteil = tilgung
        self.Sondertilgungsanteil = soti
        self.Restschuld = restschuld


class AnnuitaetenKredit(object):
    """
    Calulator for annuity loans.
    """

    def __init__(self, betrag, tilgung, zins):
        """
        Initializes the annuity loan calcuator

        :param betrag (float): loan amount
        :param tilgung (float): redemption rate in %
        :param zins (float): nominal interest in %
        """
        self._t0 = tilgung / 100.0
        self._z = zins / 100.0
        self._s0 = betrag

        self._zges = 0.0 # sum of interest
        self._m = 0 # month
        self._ms  = 0.0 # month's rate
        self._mtil = 0.0 # current redemption amount
        self._stil = 0.0 # extra redemption
        self._mzins = 0.0 # current interest amount
        self._s  = self._s0 # balance

        self._verlauf = [] # list of KreditverlaufsZwischenstand objects

    def _monatsschritt(self, sondertilgung=0.0):
        """
        Calulates all values for next month.

        :param sondertilgung (float): extra payment for this month
        """
        self._stil = sondertilgung
        if self._m == 1:
            self._ms = (self._s0 * self._t0 + self._s0 * self._z) / 12
            self._mtil = (self._s0 * self._t0) / 12 + self._stil
            if self._mtil > self._s:
                self._mtil = self._s
            self._mzins = self._s0 * self._z / 12
            self._s = self._s0 - self._mtil
            self._zges = self._mzins
            # self._zeff = self._z
        else:
            self._mzins = self._s * self._z / 12
            self._mtil = self._ms - self._mzins + self._stil
            if self._mtil > self._s:
                self._mtil = self._s
            # self._teff = self._mtil / self._s0 * 12
            self._s = self._s - self._mtil
            self._zges = self._zges + self._mzins

    def berechne_kreditverlauf(self, sondertilgungen={}):
        """
        Calculate schedule.

        :param sondertilgungen (dict of (int,float)): Extra payments.
               key: month, value: amount.
        :return: schedule. A KreditverlaufsZwischenstand object is created for
                 each month containing the values
                 (month, interest, redemption, extra payment, balance)
        :rtype: list of KreditverlaufsZwischenstand objects.
        """
        self._m = 1
        if self._s == 0.0:
            self._verlauf.append(
                KreditverlaufsZwischenstand(
                    self._m, 0.0, 0.0, 0.0, 0.0))
        while self._s > 0:
            if self._m - 1 in sondertilgungen:
                self._monatsschritt(sondertilgungen[self._m - 1])
            else:
                self._monatsschritt()
            self._verlauf.append(
                KreditverlaufsZwischenstand(
                    self._m, self._mzins, self._mtil - self._stil, self._stil, self._s))
            self._m += 1
        return self._verlauf

    @property
    def GesamtKosten(self):
        """
        Sum of interest payments.
        """
        return self._zges

    @property
    def Monatsrate(self):
        """
        Monthly rate.
        """
        return self._verlauf[0].Zinsanteil + self._verlauf[0].Tilgungsanteil
