import click
from pythondaq.models.diode_experiment import DiodeExperiment


# Open device and print identification

device = DiodeExperiment()


@click.group()
def cmd_group():
    pass


@cmd_group.command("list")
@click.option(
    "-s",
    "--search",
    default="bla",
    help="print connected device",
    show_default=True,  # show default in help
)
def lists(search):
    print(device.list(search))


@cmd_group.command("info")
@click.option(
    "-s",
    "--search",
    default="bla",
    help="print connected device",
    show_default=True,  # show default in help
)
def information(search):
    device.info(search)


@cmd_group.command("measure")
@click.option(
    "-v",
    "--voltage",
    default="1",
    help="determine current",
    show_default=True,  # show default in help
)
def currents(voltage):
    print(device.current(voltage))


@cmd_group.command("scan")
@click.argument("begin_range", type=click.FloatRange(0, 3.3))
@click.argument("end_range", type=click.FloatRange(0, 3.3))
def scan(begin_range, end_range):
    print(f"current = {device.scan(begin_range, end_range)}")


if __name__ == "__main__":
    cmd_group()
