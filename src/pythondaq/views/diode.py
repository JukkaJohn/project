import click
from pythondaq.models.diode_experiment import DiodeExperiment


# Open device
device = DiodeExperiment()

# Makes group of commands
@click.group()
def cmd_group():
    pass


# This command gives an option search to type an input string to check if it corresponds with a connected device
@cmd_group.command("list")
@click.option(
    "-s",
    "--search",
    default="hello",
    help="prints connected device",
    show_default=True,  # show default in help
)
# Prints devices connected to your computer
def lists(search):
    print(device.list(search))


# This command gives an option search to type an input string to check if it corresponds with a connected device
@cmd_group.command("info")
@click.option(
    "-s",
    "--search",
    default="bla",
    help="prints type connected device",
    show_default=True,  # show default in help
)
# Prints type of devices connected to your computer
def information(search):
    device.info(search)


# This command gives an option search to type a value to determine the input voltage
@cmd_group.command("measure")
@click.option(
    "-v",
    "--voltage",
    default="1",
    help="input voltage",
    show_default=True,  # show default in help
)
# This function prints the current corresponding to the input voltage
def currents(voltage):
    print(device.current(voltage))


# These commands determine the range of the input voltage.
@cmd_group.command("scan")
@click.argument("begin_range", type=click.FloatRange(0, 3.3))
@click.argument("end_range", type=click.FloatRange(0, 3.3))
# This command determines the name of the csv file.
@click.option(
    "-o",
    "--output",
    default="",
    help="csv file name",
    show_default=True,  # show default in help
)
# This command determines the number of measurements per voltage.
@click.option(
    "-c",
    "--counts",
    default=1,
    help="number of measurements per voltage",
    show_default=True,  # show default in help
    type=int,
)
# This function prints the voltages and currents and their errors
def scan(begin_range, end_range, output, counts):
    print(f"current = {device.scan(begin_range, end_range,output,counts)}")


if __name__ == "__main__":
    cmd_group()
