from pythondaq.controllers.arduino_device import list_devices, ArduinoVISADevice
import numpy as np

# Open device and print identification

port = "ASRL/dev/cu.usbmodem14101::INSTR"
device = ArduinoVISADevice(port)


class DiodeExperiment:
    def __init__(self):
        pass

    def list(self, search):
        """List VISA devices connected to the system.

                Returns:
                A list of VISA port names.
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
        """List VISA devices connected to the system.

            Returns:
                A list of VISA port names.
            """
        if str(search) in str(list_devices()):
            for item in list_devices():
                if str(search) in str(item):
                    return f"The following devices match your search string:{device.get_identification()}"

        else:
            return "There are no devices"

    def current(self, voltage):
        I = []
        device.set_output_voltage(channel=0, value=voltage)
        volt_ch2 = device.get_input_voltage(channel=2)
        I.append(float(volt_ch2) / 220)
        device.set_output_value(channel=0, value=0)
        return I

    def scan(self, begin_range, end_range):
        U_led = []
        I = []
        for value in np.arange(begin_range, end_range, 0.003):
            device.set_output_voltage(channel=0, value=value)
            volt_ch1 = device.get_input_voltage(channel=1)
            volt_ch2 = device.get_input_voltage(channel=2)
            print(value, volt_ch1, volt_ch2)

            U_led.append(float(volt_ch1) - float(volt_ch2))
            I.append(float(volt_ch2) / 220)
        device.set_output_value(channel=0, value=0)
        return U_led, I
