import click
import pyvisa


@click.group()
def cmd_group():
    pass


port = "ASRL/dev/cu.usbmodem14501::INSTR"
rm = pyvisa.ResourceManager("@py")
device = rm.open_resource(
    port, read_termination="\r\n", write_termination="\n", timeout=1000
)


@cmd_group.command("list")
@click.option(
    "-s",
    "--search",
    default="bla",
    help="print connected device",
    show_default=True,  # show default in help
)
def list(search):
    """List VISA devices connected to the system.

    Returns:
         A list of VISA port names.
    """
    if str(search) in str(rm.list_resources()):
        for item in rm.list_resources():
            if str(search) in str(item):
                print("The following devices match your search string:")
                print("ASRL/dev/cu.usbmodem14501::INSTR")
    else:
        print("The following devices are connected to your computer:")
        print(rm.list_resources())


@cmd_group.command("info")
@click.option(
    "-s",
    "--search",
    default="bla",
    help="print connected device",
    show_default=True,  # show default in help
)
def info(search):

    """List VISA devices connected to the system.

    Returns:
         A list of VISA port names.
    """
    if str(search) in str(rm.list_resources()):
        for item in rm.list_resources():
            if str(search) in str(item):
                print("The following devices match your search string:")
                print(device.query("*IDN?"))
    else:
        print("")


if __name__ == "__main__":
    cmd_group()
