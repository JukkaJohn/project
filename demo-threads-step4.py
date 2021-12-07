import sys
import threading
import time

import numpy as np

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg


# view
class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        vbox = QtWidgets.QVBoxLayout(central_widget)
        self.plot_widget = pg.PlotWidget()
        vbox.addWidget(self.plot_widget)
        start_button = QtWidgets.QPushButton("Start")
        vbox.addWidget(start_button)

        start_button.clicked.connect(self.start_scan)

        # Experiment
        self.experiment = Experiment()

        # Plot timer
        self.plot_timer = QtCore.QTimer()
        # Roep iedere 100 ms de plotfunctie aan
        self.plot_timer.timeout.connect(self.plot)
        self.plot_timer.start(100)

    def start_scan(self):
        self.experiment.start_scan(0, np.pi, 50)

    def plot(self):
        """Plot data van het experiment"""
        self.plot_widget.clear()
        self.plot_widget.plot(
            self.experiment.x, self.experiment.y, symbol="o", symbolSize=5, pen=None
        )


# model
class Experiment:
    def __init__(self):
        self.x = []
        self.y = []

    def start_scan(self, start, stop, steps):
        """Start a new thread to execute a scan."""
        self._scan_thread = threading.Thread(
            target=self.scan, args=(start, stop, steps)
        )
        self._scan_thread.start()

    def scan(self, start, stop, steps):
        x = np.linspace(start, stop, steps)
        self.x = []
        self.y = []
        for u in x:
            self.x.append(u)
            self.y.append(np.sin(u))
            time.sleep(0.1)
        return self.x, self.y


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
