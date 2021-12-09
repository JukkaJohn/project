from pythondaq.controllers.arduino_device import list_devices, ArduinoVISADevice
import numpy as np
import csv
from statistics import stdev
import time
import threading


# Open device and print identification


class DiodeExperiment:
    def __init__(self, port):
        """opens the selected device

        Args:
            port (str): selected device
        """
        self.device = ArduinoVISADevice(port)
        self.port = port

        self.I = []
        self.U_led = []
        self.error_I_mean_list = []
        self.error_U_led_list = []

    # def list(self, search):
    #     """[summary]
    #     Args:
    #         search ([type]): [description]
    #     Returns:
    #         [type]: [description]
    #     """
    #     if str(search) in str(list_devices()):
    #         for item in list_devices():
    #             if str(search) in str(item):
    #                 return f"The following devices match your search string: {item}"

    #     else:
    #         return (
    #             f"The following devices are connected to your computer:{list_devices()}"
    #         )

    # def info(self, search):
    #     """[summary]
    #     Args:
    #         search ([type]): [description]
    #     Returns:
    #         [type]: [description]
    #     """
    #     if str(search) in str(list_devices()):
    #         for item in list_devices():
    #             if str(search) in str(item):
    #                 return f"The following devices match your search string:{self.device.get_identification()}"

    #     else:
    #         return "There are no devices"

    # def current(self, voltage):
    #     """[summary]
    #     Args:
    #         voltage ([type]): [description]
    #     Returns:
    #         [type]: [description]
    #     """
    #     I = []
    #     self.device.set_output_voltage(channel=0, value=voltage)
    #     volt_ch2 = self.device.get_input_voltage(channel=2)
    #     I.append(float(volt_ch2) / 220)
    #     self.device.set_output_value(channel=0, value=0)
    #     return I

    def close(self):
        """Closes the window
        """
        self.device.closes()

    def start_scan(self, start, stop, steps):
        """Start a new thread to execute a scan."""
        self._scan_thread = threading.Thread(
            target=self.scan, args=(start, stop, steps)
        )
        self._scan_thread.start()

    def scan(self, begin_range, end_range, counts):

        """excecutes measurments
        Args:
            begin_range (float): the start of range of measurements
            end_range (float): the end of range of measurements
            counts (int): number of times one value in the range is measured
        Returns:
            int: voltages, currents and their errors
        """
        self.U_led = []
        self.I = []
        self.error_I_mean_list = []
        self.error_U_led_list = []
        # loops over the range of voltages
        for value in np.arange(begin_range, end_range, 0.03):
            mean_U_led = 0
            mean_I = 0
            # stores data with a loop over input voltage
            voltages = []
            currents = []
            # loops a number of times over one voltage
            for i in range(0, counts):
                # measurements
                self.device.set_output_voltage(channel=0, value=value)
                volt_ch1 = self.device.get_input_voltage(channel=1)
                volt_ch2 = self.device.get_input_voltage(channel=2)

                # calculates voltage and current over LED
                mean_U_led += (float(volt_ch1) - float(volt_ch2)) / counts
                mean_I += (float(volt_ch2) / 220) / counts

                voltages.append(float(volt_ch1) - float(volt_ch2))
                currents.append(float(vot_ch2) / 220)
                i += 1

            self.U_led.append(mean_U_led)
            self.I.append(mean_I)
            # calculate error
            err_mean_U = stdev(voltages) / np.sqrt(counts)
            err_mean_I = stdev(currents) / np.sqrt(counts)

            self.error_U_led_list.append(err_mean_U)
            self.error_I_mean_list.append(err_mean_I)
        # stops measurements
        self.device.set_output_value(channel=0, value=0)
        return self.U_led, self.I, self.error_U_led_list, self.error_I_mean_list

    def save(self, output):
        """Saves the data from the measurements

        Args:
            output (str): name of the csv file
        """
        if output != "":
            with open(f"{output}", "w") as f:
                writer = csv.writer(f)
                writer.writerow(["U_LED", "I", "err_u", "err_I"])
                for u, i, err_u, err_i in zip(
                    self.U_led, self.I, self.error_U_led_list, self.error_I_mean_list
                ):
                    writer.writerow([u, i, err_u, err_i])
