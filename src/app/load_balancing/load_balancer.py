from abc import ABC, abstractmethod
from ..server import Server


class LoadBalancer(ABC):
    def __init__(self, server_list: list[Server] = None) -> None:
        self._init_server_storage(server_list)

    @abstractmethod
    def _init_server_storage(self, server_list: list[Server] = None) -> None:
        pass

    @abstractmethod
    def add_server(self, name: str) -> None:
        pass

    @abstractmethod
    def responsible_server(self, key: str) -> Server:
        pass
