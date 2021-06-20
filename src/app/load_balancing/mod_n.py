from ..server import Server
from ..hash_function import hash
from .load_balancer import LoadBalancer


class ModN(LoadBalancer):
    '''a class that implements a mod-n hashing lookup.

    it maintains a list of servers
    and will lookup the server responsible for a given key value
    '''

    def _init_server_storage(self, server_list: list[Server] = None) -> None:
        self.__server_list = server_list if server_list is not None else []

    def add_server(self, name: str) -> None:
        self.__server_list.append(Server(name))

    def responsible_server(self, key_name: str) -> Server:
        return self.__server_list[hash(key_name) % len(self.__server_list)]
