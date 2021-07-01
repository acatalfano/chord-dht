import traceback
import click
from app.network.key_server import KeyServer


@click.command()
@click.option('-i', '--ip-address', type=str, help="IP address of the key-server")
def __main__(ip_address: str) -> None:
    try:
        print(f'keyserver: {ip_address}')
        KeyServer(ip_address)
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
    __main__()
