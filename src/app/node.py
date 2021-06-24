from typing import Callable
from .server import Server


class Node(Server):
    def __init__(self, name: str, id_method: Callable[[str], int]) -> None:
        super().__init__(name)
        self.__digest_id = id_method(name)
        self.__address_precision = 8
        self.__address_space_size = 2 ** self.__address_precision
        self.__finger_table: list[Node] = []

    def set_successor(self, successor: 'Node') -> None:
        self.__successor = successor

    def build_finger_table(self) -> None:
        self.__finger_table = [
            self.find_successor((self.__digest_id + 2 ** k) % 2 ** 8)[0]
            for k in range(self.__address_precision)
        ]

    def find_successor(self, digest: int, hops: int = 0) -> tuple['Node', int]:
        if (digest - self.id) % self.__address_space_size <= (self.__successor.id - self.id) % self.__address_space_size:
            return (self.__successor, hops)
        else:
            return self.__successor.find_successor(digest, hops + 1)

    @property
    def finger_table(self) -> list['Node']:
        return self.__finger_table

    @property
    def id(self) -> int:
        return self.__digest_id
