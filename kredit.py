#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Berechnung des Verlaufs von Annitätendarlehen.
"""

class KreditverlaufsZwischenstand(object):
    """
    Beschreibt eine Zeile in einem Kreditverlauf.
    """
    def __init__(self, monat, zins, tilgung, soti, restschuld):
        """
        Konstruktor.

        :param monat (int): Nummer des Monats im Kreditverlauf
        :param zins (float): Zinsanteil in der Monatsrate.
        :param tilgung (float): Tilgungsteil in der Monatsrate.
        :param soti (float): In diesem Monat gezahlte Sondertilgung.
        :param restschuld (float): Aktueller Saldo des Kreditkontos nach Abzug
               der Tilgungszahlungen.
        """
        self.Monat = monat
        self.Zinsanteil = zins
        self.Tilgungsanteil = tilgung
        self.Sondertilgunsanteil = soti
        self.Restschuld = restschuld


class AnnuitaetenKredit(object):
    """
    Berechnet einen Kreditverlauf unter Berücksichtigung von Sondertilgungen.
    """

    def __init__(self, betrag, tilgung, zins):
        """
        Initialisiert den Kreditrechner

        :param betrag (float): Der Betrag der Darlehenssumme
        :param tilgung (float): Der Tilgungssatz in Prozent
        :param zins (float): Der nominale Zinssatz
        """
        self._t0 = tilgung / 100.0
        self._z = zins / 100.0
        self._s0 = betrag

        self._zges = 0.0 # Zinssumme
        self._m = 0 # Monat
        self._ms  = 0.0 # Monatssumme
        self._mtil = 0.0 # aktuelle Tilgung
        self._mzins = 0.0 # aktueller Zinsbetrag
        self._s  = self._s0 # verbliebene Summe

        self._verlauf = [] # Liste der einzelnen Beträge des Kreditverlaufs

    def _monatsschritt(self, sondertilgung=0.0):
        """
        Berechnet alle Werte für den naechsten Monat.

        :param sondertilgung (float): Sondertilgung für diesen Monat
        """
        if self._m == 1:
            self._ms = (self._s0 * self._t0 + self._s0 * self._z) / 12
            self._mtil = (self._s0 * self._t0) / 12 + sondertilgung
            if self._mtil > self._s:
                self._mtil = self._s
            self._mzins = self._s0 * self._z / 12
            self._s = self._s0 - self._mtil
            self._zges = self._mzins
            # self._zeff = self._z
        else:
            self._mzins = self._s * self._z / 12
            self._mtil = self._ms - self._mzins + sondertilgung
            if self._mtil > self._s:
                self._mtil = self._s
            # self._teff = self._mtil / self._s0 * 12
            self._s = self._s - self._mtil
            self._zges = self._zges + self._mzins

    def berechne_kreditverlauf(self, sondertilgungen={}):
        """
        Berechnet den Kreditverlauf.

        :param sondertilgungen (dict of (int,float)): Die Sondertilgungen.
               key: Monat, value: Sondertilgung.
        :return: Kreditverlauf. Für jeden Monat wird ein Objekt vom Typ
                 KreditverlaufsZwischenstand mit den Werten
                 (Monat, Zinsanteil, Tilgungsanteil, Sondertilgung, Restschuld)
                 geliefert.
        :rtype: Liste von KreditverlaufsZwischenstand-Objekten.
        """
        self._m = 1
        while self._s > 0:
            if self._m in sondertilgungen:
                self._monatsschritt(sondertilgungen[self._m])
            else:
                self._monatsschritt()
            self._verlauf.append(
                KreditverlaufsZwischenstand(
                    self._m, self._mzins, self._mtil, 0, self._s))
            self._m += 1
        return self._verlauf

    @property
    def GesamtKosten(self):
        """
        Summe der Zinszahlungen.
        """
        return self._zges

    @property
    def Monatsrate(self):
        """
        Betrag der monatlichen Rate.
        """
        return self._verlauf[0].Zinsanteil + self._verlauf[0].Tilgungsanteil
