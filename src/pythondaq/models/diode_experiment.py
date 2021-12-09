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

        self.U_led = []
        self.I = []
        self.powers = []
        self.R = []
        self.error_I_mean_list = []
        self.error_U_led_list = []
        self.error_power = []
        self.error_R = []
        self.vch0 = []
        self.err_ch0 = []

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
        self.powers = []
        self.R = []
        self.error_I_mean_list = []
        self.error_U_led_list = []
        self.error_power = []
        self.error_R = []
        self.vch0 = []
        self.err_ch0 = []

        # loops over the range of voltages
        for value in np.arange(begin_range, end_range, 0.03):
            mean_U_led = 0
            mean_I = 0
            mean_vch0 = 0
            # stores data with a loop over input voltage
            voltages = []
            currents = []
            vch0 = []
            # loops a number of times over one voltage
            for i in range(0, counts):
                # measurements
                volt_ch0 = self.device.set_output_voltage(channel=0, value=value)
                volt_ch1 = self.device.get_input_voltage(channel=1)
                volt_ch2 = self.device.get_input_voltage(channel=2)

                # calculates voltage and current over LED
                mean_U_led += 3 * float(volt_ch1) / counts
                mean_I += mean_U_led / 4.7
                mean_vch0 += float(volt_ch0) / counts

                voltages.append(3 * float(volt_ch1))
                currents.append(float(volt_ch2) / 4.7)
                vch0.append(volt_ch0)
                i += 1

            self.vch0.append(mean_vch0)
            self.U_led.append(mean_U_led)
            self.I.append(mean_I)
            self.powers.append(mean_U_led * mean_I)
            if mean_I == 0:
                self.R.append(10000000)
            else:
                self.R.append(mean_U_led / mean_I)

            # calculate error
            err_mean_U = stdev(voltages) / np.sqrt(counts)
            err_mean_I = stdev(currents) / np.sqrt(counts)
            err_mean_power = np.sqrt(
                (mean_U_led * err_mean_I) ** 2 + (mean_I * err_mean_U) ** 2
            )
            if mean_I == 0:
                err_R = 0
            else:
                err_R = np.sqrt(
                    (err_mean_U / mean_I) ** 2
                    + ((err_mean_I * mean_U_led) / (mean_I ** 2)) ** 2
                )
            self.err_ch0.append(stdev(voltages) / np.sqrt(counts))
            self.error_U_led_list.append(err_mean_U)
            self.error_I_mean_list.append(err_mean_I)
            self.error_power.append(err_mean_power)
            self.error_R.append(err_R)
        # stops measurements
        self.device.set_output_value(channel=0, value=0)
        return (
            self.U_led,
            self.I,
            self.error_U_led_list,
            self.error_I_mean_list,
            self.powers,
            self.R,
            self.error_R,
            self.error_power,
            self.vch0,
            self.err_ch0,
        )

    def save(self, output):
        """Saves the data from the measurements

        Args:
            output (str): name of the csv file
        """

        if output != "":
            with open(f"{output}", "w") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "U_LED",
                        "I",
                        "err_u",
                        "err_I",
                        "Power",
                        "Resistance",
                        "err_Resistance",
                        "err_power",
                        "Voltage_ch0",
                        "error voltagech0",
                    ]
                )
                for u, i, err_u, err_i, powers, r, err_r, err_p, vch0, err_vch0 in zip(
                    self.U_led,
                    self.I,
                    self.error_U_led_list,
                    self.error_I_mean_list,
                    self.powers,
                    self.R,
                    self.error_R,
                    self.error_power,
                    self.vch0,
                    self.err_ch0,
                ):
                    writer.writerow(
                        [u, i, err_u, err_i, powers, r, err_r, err_p, vch0, err_vch0]
                    )
