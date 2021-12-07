import sys
import time

import numpy as np

from PyQt5 import QtWidgets
import pyqtgraph as pg


# view
class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        self.x = []
        self.y = []
        super().__init__()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        vbox = QtWidgets.QVBoxLayout(central_widget)
        self.plot_widget = pg.PlotWidget()
        vbox.addWidget(self.plot_widget)
        start_button = QtWidgets.QPushButton("Start")
        vbox.addWidget(start_button)

        start_button.clicked.connect(self.plot)

        # Experiment
        self.experiment = Experiment()

    def plot(self):
        """Plot data van het experiment"""
        self.plot_widget.clear()
        x, y = self.experiment.scan(0, np.pi, 50)
        self.plot_widget.plot(x, y, symbol="o", symbolSize=5, pen=None)
        self.experiment.scan(0, np.pi, 50)
        self.plot_widget.plot(
            self.experiment.x, self.experiment.y, symbol="o", symbolSize=5, pen=None
        )


# model
class Experiment:
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
