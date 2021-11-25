import csv

import matplotlib.pyplot as plt

from pythondaq.controllers.arduino_device import list_devices, ArduinoVISADevice


# help(ArduinoVISADevice)

print("List of connected devices:")
print(list_devices())
print()

# This port is specific to my setup. Please change.
port = "ASRL/dev/cu.usbmodem14501::INSTR"

# Open device and print identification
device = ArduinoVISADevice(port)
print(device.get_identification())
print()

# Perform measurement
U_led = []
I = []
for value in range(1024):
    device.set_output_value(channel=0, value=value)
    volt_ch1 = device.get_input_voltage(channel=1)
    value_ch2 = device.get_input_value(channel=2)
    volt_ch2 = device.get_input_voltage(channel=2)
    print(value, volt_ch1, value_ch2, volt_ch2)

    U_led.append(float(volt_ch1) - float(volt_ch2))
    I.append(float(volt_ch2) / 220)

# Turn off LED
device.set_output_value(channel=0, value=0)

# Create plot
plt.figure()
plt.plot(U_led, [i * 1000 for i in I], ".")
plt.xlabel(r"$U_\mathrm{LED}$ [V]")
plt.ylabel("$I$ [mA]")
plt.show()

# Save data to CSV (overwrites old files)
with open("testdata.txt", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["U_LED", "I"])
    for u, i in zip(U_led, I):
        writer.writerow([u, i])
