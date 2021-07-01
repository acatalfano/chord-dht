from ..hash_function import HashFunction
from .CONFIG import KEY_SERVER_PORT
import zmq


class KeyServer:
    def __init__(self, ip_address: str) -> None:
        print('keyserver')
        self.__hasher = HashFunction()
        self.__context = zmq.Context.instance()
        self.__build_sockets(ip_address)
        self.__dns_map: dict[int, str] = {}
        self.__spin()

    def __build_sockets(self, ip_address: str) -> None:
        self.__key_socket = self.__context.socket(zmq.REP)
        self.__key_socket.bind(f'tcp://{ip_address}:{KEY_SERVER_PORT}')

    def __spin(self) -> None:
        while True:
            self.__handle_key_request()

    def __handle_key_request(self) -> None:
        client_ip_address = self.__key_socket.recv_string()
        hash_value = self.__hasher.hash_function(client_ip_address)
        self.__dns_map.setdefault(hash_value, client_ip_address)
        self.__key_socket.send_string(hash_value)
