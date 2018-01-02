#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
Window für die grafische Anzeige eines Kreditverlaufs.
"""

import sys

from PyQt5.QtWidgets import (
    QDialog,
    QApplication,
    QPushButton,
    QVBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class PlotWindow(QDialog):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(close_button)
        self.setLayout(layout)

    def plot(self, kredit_verlauf):
        '''
        Kreditverlauf zeichnen
        '''
        # instead of ax.hold(False)
        self.figure.clear()

        monate = [x.Monat for x in kredit_verlauf]
        zinsen = [x.Zinsanteil for x in kredit_verlauf]
        tilgung = [(x.Tilgungsanteil + x.Sondertilgunsanteil)
                   for x in kredit_verlauf]
        rest = [x.Restschuld for x in kredit_verlauf]

        # create an axis
        ax1 = self.figure.add_subplot(211)
        ax2 = self.figure.add_subplot(212)

        # plot data
        color = 'cornflowerblue'
        ax1.plot(monate, rest, linestyle='-', color=color, linewidth=1)

        ax2.bar(monate, zinsen, 1, color='#d62728')
        ax2.bar(monate, tilgung, 1, bottom=zinsen)

        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())