# Code from Canvas "uitwerkingen hoofdstuk 5"
"""Classes handling communication with Arduino devices.
Typical usage::

    >>> port = list_devices()[0]
    >>> device = ArduinoVISADevice(port)
    >>> print(device.get_identification())
    >>> device.set_output_value(channel=0, value=512)
    >>> value = device.get_input_value(channel=2)
"""

import pyvisa


class ArduinoVISADevice:
    """An Arduino device compatible with the VISA standard."""

    def __init__(self, port):
        """Instantiate the device.

        Args:
            port (str): the name of the VISA port the device is connected to.

        """
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n", timeout=1000
        )

    def get_identification(self):
        """Returns the device identification string."""
        return self.device.query("*IDN?")

    def set_output_value(self, channel, value):
        """Set the value for a DAC output channel.

        Args:
            channel (int): The output channel. Channel numbering starts at 0.
            value (int): The raw DAC value (range 0 - 1023), where 0 is the
                device's GND and 1023 is the device's operating voltage (3.3 V).

        Returns:
            The devices' response. Typically the device echoes back the value.
        """
        return self.device.query(f"OUT:CH{channel} {value}")

    def get_output_value(self, channel):
        """Get the value previously set for a DAC output channel.

        Args:
            channel (int): The output channel. Channel numbering starts at 0.

        Returns:
            The integer value previously set for the channel (range 0 - 1023),
            where 0 is the device's GND and 1023 is the device's operating
            voltage (3.3 V).
        """
        return self.device.query(f"OUT:CH{channel}?")

    def set_output_voltage(self, channel, value):
        """Set the voltage for a DAC output channel.

        This differs from :meth:`set_output_value` in that this method sets the
        voltage, not a raw DAC value.

        Args:
            channel (int): The output channel. Channel numbering starts at 0.
            value (float): The DAC voltage (range 0 - 3.3 V).

        Returns:
            The devices' response. Typically the device echoes back the value.
        """
        return self.device.query(f"OUT:CH{channel}:VOLT {value}")

    def get_output_voltage(self, channel):
        """Get the voltage previously set for a DAC output channel.

        This differs from :meth:`get_output_value` in that this method gets the
        voltage, not a raw DAC value.

        Args:
            channel (int): The output channel. Channel numbering starts at 0.

        Returns:
            The float value previously set for the channel voltage (range 0 - 3.3 V).
        """
        return self.device.query(f"OUT:CH{channel}:VOLT?")

    def get_input_value(self, channel):
        """Get the value measured on an ADC input channel.

        Args:
            channel (int): The input channel. Channel numbering starts at 0.

        Returns:
            The integer value measured for the channel (range 0 - 1023),
            where 0 is the device's GND and 1023 is the device's operating
            voltage (3.3 V).
        """
        return self.device.query(f"MEAS:CH{channel}?")

    def get_input_voltage(self, channel):
        """Get the voltage measured on an ADC input channel.

        This differs from :meth:`get_input_value` in that this method gets the
        voltage, not a raw ADC value.

        Args:
            channel (int): The input channel. Channel numbering starts at 0.

        Returns:
            The float value measured for the channel voltage (range 0 - 3.3 V).
        """
        return self.device.query(f"MEAS:CH{channel}:VOLT?")


def list_devices():
    """List VISA devices connected to the system.

    Returns:
         A list of VISA port names.
    """
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()
