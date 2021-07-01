import click
import traceback
from app.network.networked_node import NetworkedNode


@click.command()
@click.option('-k', '--key-server-ip', type=str, help='IP address of the key-server')
@click.option('-i', '--ip-address', type=str, help='IP address of this node')
@click.option('-w', '--well-known-ip', type=str, help='IP address of the well-known node')
@click.option('-j', '--join', is_flag=True)
def __main__(key_server_ip: str, ip_address: str, well_known_ip: str, join: bool) -> None:
    print('running node')
    print(f'\tkey server ip: {key_server_ip}')
    print(f'\tip: {ip_address}')
    print(f'\twell known ip: {well_known_ip}')
    print(f'\tjoin: {join}')
    try:
        node = NetworkedNode(ip_address, key_server_ip)
        if join:
            node.join_ring(well_known_ip)
        else:
            node.create_new_ring()
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
    __main__()
