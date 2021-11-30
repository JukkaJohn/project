from pythondaq.controllers.arduino_device import list_devices, ArduinoVISADevice
import numpy as np
import csv
from statistics import stdev


# Open device and print identification

port = "ASRL/dev/cu.usbmodem14101::INSTR"
device = ArduinoVISADevice(port)


class DiodeExperiment:
    def __init__(self):
        pass

    def list(self, search):
        """[summary]

        Args:
            search ([type]): [description]

        Returns:
            [type]: [description]
        """
        if str(search) in str(list_devices()):
            for item in list_devices():
                if str(search) in str(item):
                    return f"The following devices match your search string: {item}"

        else:
            return (
                f"The following devices are connected to your computer:{list_devices()}"
            )

    def info(self, search):
        """[summary]

        Args:
            search ([type]): [description]

        Returns:
            [type]: [description]
        """
        if str(search) in str(list_devices()):
            for item in list_devices():
                if str(search) in str(item):
                    return f"The following devices match your search string:{device.get_identification()}"

        else:
            return "There are no devices"

    def current(self, voltage):
        """[summary]

        Args:
            voltage ([type]): [description]

        Returns:
            [type]: [description]
        """
        I = []
        device.set_output_voltage(channel=0, value=voltage)
        volt_ch2 = device.get_input_voltage(channel=2)
        I.append(float(volt_ch2) / 220)
        device.set_output_value(channel=0, value=0)
        return I

    def scan(self, begin_range, end_range, output, counts):
        """[summary]

        Args:
            begin_range ([type]): [description]
            end_range ([type]): [description]
            output ([type]): [description]
            counts ([type]): [description]

        Returns:
            [type]: [description]
        """
        U_led = []
        I = []
        error_I_mean_list = []
        error_U_led_list = []
        for value in np.arange(begin_range, end_range, 0.03):
            mean_U_led = 0
            mean_I = 0
            voltages = []
            currents = []

            for i in range(0, counts):
                device.set_output_voltage(channel=0, value=value)
                volt_ch1 = device.get_input_voltage(channel=1)
                volt_ch2 = device.get_input_voltage(channel=2)

                mean_U_led += (float(volt_ch1) - float(volt_ch2)) / counts
                mean_I += (float(volt_ch2) / 220) / counts

                voltages.append(float(volt_ch1) - float(volt_ch2))
                currents.append(float(volt_ch2) / 220)
                i += 1
                # print(value, volt_ch1, volt_ch2)

            U_led.append(mean_U_led)
            I.append(mean_I)
            print(stdev(voltages), value)
            err_mean_U = stdev(voltages) / np.sqrt(counts)
            err_mean_I = stdev(currents) / np.sqrt(counts)

            error_U_led_list.append(err_mean_U)
            error_I_mean_list.append(err_mean_I)

        device.set_output_value(channel=0, value=0)

        if output != "":
            with open(f"{output}.csv", "w") as f:
                writer = csv.writer(f)
                writer.writerow(["U_LED", "I", "err_u", "err_I"])
                for u, i, err_u, err_i in zip(
                    U_led, I, error_U_led_list, error_I_mean_list
                ):
                    writer.writerow([u, i, err_u, err_i])

        return U_led, I, error_I_mean_list, error_U_led_list
