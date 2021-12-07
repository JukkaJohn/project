import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
import pyqtgraph as pg
from pythondaq.controllers.arduino_device import list_devices
from pythondaq.models.diode_experiment import DiodeExperiment
import time

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        self.device = None

        # roep de __init__() aan van de parent class
        super().__init__()
        connected_devices = list_devices()
        # hierbinnen maak je een layout en hang je andere widgets
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        # voeg geneste layouts en widgets toe
        vbox = QtWidgets.QVBoxLayout(central_widget)
        # self.textedit = QtWidgets.QTextEdit()
        # vbox.addWidget(self.textedit)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        self.plot_widget = pg.PlotWidget()
        hbox.addWidget(self.plot_widget)

        self.start_button = QtWidgets.QDoubleSpinBox()
        hbox.addWidget(self.start_button)
        self.start_button.valueChanged.connect(self.change)
        self.start_button.setMinimum(0)
        self.start_button.setMaximum(3.3)
        self.start_button.setFixedWidth(60)

        self.end_button = QtWidgets.QDoubleSpinBox()
        hbox.addWidget(self.end_button)
        self.end_button.valueChanged.connect(self.change)
        self.end_button.setMaximum(3.3)
        self.end_button.setMinimum(0)
        self.end_button.setFixedWidth(60)

        self.point_button = QtWidgets.QSpinBox()
        hbox.addWidget(self.point_button)
        self.point_button.valueChanged.connect(self.change)
        self.point_button.setMinimum(2)
        self.point_button.setMaximum(10)
        self.point_button.setFixedWidth(60)

        self.formlayout = QtWidgets.QFormLayout()
        self.formlayout.addRow(self.tr("&start"), self.start_button)
        self.formlayout.addRow(self.tr("&stop"), self.end_button)
        self.formlayout.addRow(self.tr("&step"), self.point_button)
        hbox.addLayout(self.formlayout)

        self.start_measurement = QtWidgets.QPushButton("Measure")
        self.start_measurement.setFixedWidth(300)
        hbox.addWidget(self.start_measurement)
        self.start_measurement.clicked.connect(self.measure)
        self.start_measurement.setFixedWidth(120)

        self.quit = QtWidgets.QPushButton("quit")
        self.quit.setFixedWidth(300)
        self.quit.clicked.connect(self.shut)
        hbox.addWidget(self.quit)
        self.quit.setFixedWidth(120)

        self.save = QtWidgets.QPushButton("save")
        self.save.setFixedWidth(300)
        self.save.clicked.connect(self.save_data)
        hbox.addWidget(self.save)
        self.save.setFixedWidth(120)

        self.formlayout = QtWidgets.QHBoxLayout()
        self.formlayout.addWidget(self.start_measurement)
        self.formlayout.addWidget(self.quit)
        self.formlayout.addWidget(self.save)
        vbox.addLayout(self.formlayout)

        self.devices = QtWidgets.QComboBox()
        self.devices.addItems(connected_devices)
        self.devices.currentTextChanged.connect(self.open)
        hbox.addWidget(self.devices)
        self.devices.setFixedWidth(120)

    def open(self):
        if self.device != None:
            self.device.close()
        self.device = DiodeExperiment(self.devices.currentText())
        return self.device

    def save_data(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        self.device.save(filename)

    def change(self):
        start_value = self.start_button.value()
        end_value = self.end_button.value()
        step_value = self.point_button.value()

        return start_value, end_value, step_value

    def measure(self):
        self.device = DiodeExperiment(self.devices.currentText())
        self.plot_widget.clear()
        self.U_led, _, _, _ = self.device.scan(
            self.start_button.value(),
            self.end_button.value(),
            self.point_button.value(),
        )
        _, self.I, _, _ = self.device.scan(
            self.start_button.value(),
            self.end_button.value(),
            self.point_button.value(),
        )
        print(self.U_led)
        print(self.I)
        print(len(self.U_led))
        self.plot_widget.plot(
            self.device.U_led,
            self.device.I,
            symbol=None,
            pen={"color": "k", "width": 5},
        )

        self.plot_widget.setLabel("left", "current(I)")
        self.plot_widget.setLabel("bottom", "voltage(U)")

    def shut(self):
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
