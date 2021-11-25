import click
import pyvisa


@click.group()
def cmd_group():
    pass


@cmd_group.command()
@click.option(
    "-s",
    "--search",
    default=1,
    help="print connected device",
    show_default=True,  # show default in help
)
def list_devices():
    """List VISA devices connected to the system.

    Returns:
         A list of VISA port names.
    """
    rm = pyvisa.ResourceManager("@py")
    print(rm.list_resources())


if __name__ == "__main__":
    cmd_group()
