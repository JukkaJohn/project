import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
import pyqtgraph as pg
from pythondaq.controllers.arduino_device import list_devices
from pythondaq.models.diode_experiment import DiodeExperiment

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    """Creates a graphical user interface

    Args:
        QtWidgets: Creates an external window with graphical widgets
    """

    def __init__(self):
        """This function contains buttons and makes a layout.
        """
        self.device = None

        # call __init__() from parent class
        super().__init__()
        connected_devices = list_devices()
        # within this it creates a layout. Within the layout widgets are created
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        # add layouts and widgets
        vbox = QtWidgets.QVBoxLayout(central_widget)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        self.plot_widget = pg.PlotWidget()
        hbox.addWidget(self.plot_widget)

        # This button determines the start of range of measurements
        self.start_button = QtWidgets.QDoubleSpinBox()
        hbox.addWidget(self.start_button)
        self.start_button.valueChanged.connect(self.change)
        self.start_button.setMinimum(0)
        self.start_button.setMaximum(3.3)
        self.start_button.setFixedWidth(60)

        # This button determines the end of range of measurements
        self.end_button = QtWidgets.QDoubleSpinBox()
        hbox.addWidget(self.end_button)
        self.end_button.valueChanged.connect(self.change)
        self.end_button.setMaximum(3.3)
        self.end_button.setMinimum(0)
        self.end_button.setFixedWidth(60)

        # This button determines the number of times one value in the range is measured
        self.point_button = QtWidgets.QSpinBox()
        hbox.addWidget(self.point_button)
        self.point_button.valueChanged.connect(self.change)
        self.point_button.setMinimum(1)
        self.point_button.setMaximum(10)
        self.point_button.setFixedWidth(60)

        # Layout of start, end and point button
        self.formlayout = QtWidgets.QFormLayout()
        self.formlayout.addRow(self.tr("&start"), self.start_button)
        self.formlayout.addRow(self.tr("&stop"), self.end_button)
        self.formlayout.addRow(self.tr("&step"), self.point_button)
        hbox.addLayout(self.formlayout)

        # This button starts the mesasurements
        self.start_measurement = QtWidgets.QPushButton("Measure")
        self.start_measurement.setFixedWidth(300)
        hbox.addWidget(self.start_measurement)
        self.start_measurement.clicked.connect(self.start_scan)
        self.start_measurement.setFixedWidth(120)

        # This button closes the window
        self.quit = QtWidgets.QPushButton("quit")
        self.quit.setFixedWidth(300)
        self.quit.clicked.connect(self.shut)
        hbox.addWidget(self.quit)
        self.quit.setFixedWidth(120)

        # This button saves the data from the measurements
        self.save = QtWidgets.QPushButton("save")
        self.save.setFixedWidth(300)
        self.save.clicked.connect(self.save_data)
        hbox.addWidget(self.save)
        self.save.setFixedWidth(120)

        # Layout from start, quit and save buttons
        self.formlayout = QtWidgets.QHBoxLayout()
        self.formlayout.addWidget(self.start_measurement)
        self.formlayout.addWidget(self.quit)
        self.formlayout.addWidget(self.save)
        vbox.addLayout(self.formlayout)

        # This button lets you choose the device
        self.devices = QtWidgets.QComboBox()
        self.devices.addItems(connected_devices)
        self.devices.currentTextChanged.connect(self.open)
        hbox.addWidget(self.devices)
        self.devices.setFixedWidth(120)

        # Plot timer
        self.plot_timer = QtCore.QTimer()
        # Calls the measurement function every 100 ms
        self.plot_timer.timeout.connect(self.plot)
        self.plot_timer.start(100)

    def open(self):
        """This function opens the selected device

        Returns:
            The opened device
        """
        if self.device != None:
            self.device.close()
        self.device = DiodeExperiment(self.devices.currentText())
        return self.device

    def save_data(self):
        """This function calls another function to save the data
        """
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        self.device.save(filename)

    def change(self):
        """This function stores the input values of the start, end and point button

        Returns:
            The input values
        """
        start_value = self.start_button.value()
        end_value = self.end_button.value()
        step_value = self.point_button.value()

        return start_value, end_value, step_value

    def start_scan(self):
        """This function calls another function, which excecutes measurements and gives data.
        """
        self.device = DiodeExperiment(self.devices.currentText())
        self.device.start_scan(
            self.start_button.value(),
            self.end_button.value(),
            self.point_button.value(),
        )

    def plot(self):
        """This function plots the data from the measurements
        """
        self.plot_widget.clear()
        self.plot_widget.plot(
            self.device.U_led, self.device.I, symbol="o", symbolSize=5, pen=None,
        )
        self.plot_widget.setLabel("left", "current(I)")
        self.plot_widget.setLabel("bottom", "voltage(U)")

        width = 2 * np.array(self.device.error_U_led_list)
        print(width)
        height = 2 * np.array(self.device.error_I_mean_list)

        # plotting errors
        x = np.array(self.device.U_led)
        y = np.array(self.device.I)
        error_bars = pg.ErrorBarItem(x=x, y=y, width=width, height=height)
        self.plot_widget.addItem(error_bars)

    def shut(self):
        """Closes the window
        """
        self.close()


def main():
    """This function launches the external window
    """
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
