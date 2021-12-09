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

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.resize(300, 200)

        tab1 = QtWidgets.QWidget()
        tab2 = QtWidgets.QWidget()
        tab3 = QtWidgets.QWidget()

        # Add tabs
        self.tabs.addTab(tab1, "Tab 1")
        self.tabs.addTab(tab2, "Tab 2")
        self.tabs.addTab(tab3, "Tab 3")

        tab1_layout = QtWidgets.QVBoxLayout()
        self.plot_widget_UI = pg.PlotWidget()
        tab1_layout.addWidget(self.plot_widget_UI)
        tab1.setLayout(tab1_layout)

        tab2_layout = QtWidgets.QVBoxLayout()
        self.plot_widget_PR = pg.PlotWidget()
        tab2_layout.addWidget(self.plot_widget_PR)
        tab2.setLayout(tab2_layout)

        tab3_layout = QtWidgets.QVBoxLayout()
        self.plot_widget_UU = pg.PlotWidget()
        tab3_layout.addWidget(self.plot_widget_UU)
        tab3.setLayout(tab3_layout)

        # Set the layout
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.tabs)
        # self.setLayout(layout)
        vbox.addWidget(self.tabs)

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
        self.point_button.setMinimum(2)
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
        self.plot_widget_PR.clear()
        self.plot_widget_PR.plot(
            self.device.powers,
            self.device.R,
            symbol="o",
            symbolSize=5,
            pen=None,
            xlim=10,
        )
        self.plot_widget_PR.setYRange(0, 1000)
        self.plot_widget_PR.setXRange(0, 1)
        self.plot_widget_PR.setLabel("left", "power(W)")
        self.plot_widget_PR.setLabel("bottom", "resistance(Ohm)")

        width_PR = 2 * np.array(self.device.error_R)
        height_PR = 2 * np.array(self.device.error_power)

        # plotting errors
        x_PR = np.array(self.device.powers)
        y_PR = np.array(self.device.R)
        error_bars = pg.ErrorBarItem(x=x_PR, y=y_PR, width=width_PR, height=height_PR)
        self.plot_widget_PR.addItem(error_bars)

        self.plot_widget_UI.clear()
        self.plot_widget_UI.plot(
            self.device.U_led, self.device.I, symbol="o", symbolSize=5, pen=None,
        )
        self.plot_widget_UI.setYRange(0, 0.02)
        self.plot_widget_UI.setLabel("left", "current(I)")
        self.plot_widget_UI.setLabel("bottom", "voltage(U)")

        width_UI = 2 * np.array(self.device.error_U_led_list)
        height_UI = 2 * np.array(self.device.error_I_mean_list)

        # plotting errors
        x_UI = np.array(self.device.U_led)
        y_UI = np.array(self.device.I)
        error_bars = pg.ErrorBarItem(x=x_UI, y=y_UI, width=width_UI, height=height_UI)
        self.plot_widget_UI.addItem(error_bars)

        self.plot_widget_UU.clear()
        self.plot_widget_UU.plot(
            self.device.vch0, self.device.U_led, symbol="o", symbolSize=5, pen=None,
        )

        self.plot_widget_UU.setLabel("left", "voltage_sun(U)")
        self.plot_widget_UU.setLabel("bottom", "voltage_channel0(U)")

        height_UU = 2 * np.array(self.device.error_U_led_list)
        width_UU = 2 * np.array(self.device.err_ch0)

        # plotting errors
        x_UU = np.array(self.device.vch0)
        y_UU = np.array(self.device.U_led)
        error_bars = pg.ErrorBarItem(x=x_UU, y=y_UU, witdh=width_UU, height=height_UU)
        self.plot_widget_UU.addItem(error_bars)

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
