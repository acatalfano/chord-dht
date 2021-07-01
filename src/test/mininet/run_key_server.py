import click
from app.network.key_server import KeyServer


@click.command()
@click.option('-i', '--ip-address', type=str, help="IP address of the key-server")
def __main__(ip_address: str) -> None:
    KeyServer(ip_address)


if __name__ == '__main__':
    __main__()
