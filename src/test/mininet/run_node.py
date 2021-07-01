import click
from app.network.networked_node import NetworkedNode


@click.command()
@click.option('-k', '--key-server-ip', type=str, help='IP address of the key-server')
@click.option('-i', '--ip-address', type=str, help='IP address of this node')
@click.option('-w', '--well-known-ip', type=str, help='IP address of the well-known node')
@click.option('-j', '--join', is_flag=True)
def __main__(key_server_ip: str, ip_address: str, well_known_ip: str, join: bool) -> None:
    node = NetworkedNode(ip_address, key_server_ip)
    if join:
        node.join_ring(well_known_ip)
    else:
        node.create_new_ring()


if __name__ == '__main__':
    __main__()
