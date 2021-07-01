import sys
from mininet.topo import Topo
from mininet.node import Host
from mininet.net import Mininet
from mininet.log import setLogLevel
import pathlib


node_names = [f'h{h+1}' for h in range(25)]
key_server_name = 'ks'


class SingleSwitchTopo(Topo):
    def build(self):
        switch: str = self.addSwitch('s1')
        key_server = self.addHost(key_server_name)
        self.addLink(key_server, switch)
        hosts: list[str] = [self.addHost(name) for name in node_names]
        for h in hosts:
            self.addLink(h, switch)


def run_network() -> None:
    topo = SingleSwitchTopo()
    net = Mininet(topo)
    net.start()
    hosts: list[Host] = [net.getNodeByName(n) for n in node_names]
    key_server: Host = net.getNodeByName(key_server_name)
    cwd = str(pathlib.Path(__file__).parent.resolve())
    __run_key_server(key_server, cwd)
    well_known_host: Host = hosts[0]
    __run_well_known_node(well_known_host, key_server.IP(), cwd)
    other_hosts: list[Host] = hosts[1:]
    for h in other_hosts:
        __run_other_node(h, key_server.IP(), well_known_host.IP(), cwd)
    net.stop()


def __run_key_server(key_server: Host, cwd: str) -> None:
    key_server.cmdPrint(
        sys.executable,
        f'{cwd}/nodes/run_key_server.py',
        '-i', key_server.IP(),
        '>', f'{cwd}/key_server.txt',
        '&'
    )


def __run_well_known_node(well_known_host: Host, key_server_ip: str, cwd: str) -> None:
    well_known_host.cmdPrint(
        sys.executable,
        f'{cwd}/nodes/run_node.py',
        '-i', well_known_host.IP(),
        '-k', key_server_ip,
        '>', f'{cwd}/well_known.txt',
        '&'
    )


def __run_other_node(node: Host, key_server_ip: str, well_known_ip: str, cwd: str) -> None:
    node.cmdPrint(
        sys.executable,
        f'{cwd}/nodes/run_node.py',
        '-i', node.IP(),
        '-k', key_server_ip,
        '-w', well_known_ip,
        '--join',
        '>', f'{cwd}/node_{node.IP()}.txt',
        '&'
    )


if __name__ == '__main__':
    setLogLevel('info')
    run_network()
