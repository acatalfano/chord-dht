from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar
from ..CONFIG import ADDRESS_SPACE_SIZE, BITS_IN_ADDRESS
from ..utility import mod_in_range
from ..node_data.node_data import NodeData
from .server import Server

T = TypeVar('T', bound=NodeData)


class Node(Server, ABC, Generic[T]):
    def __init__(self, name: str, id_method: Callable[[str], int], skip_finger_table: bool = False) -> None:
        super().__init__(name)
        self.__predecessor: T = self._get_null_object()
        self.__digest_id = id_method(name)
        self.finger_to_fix = 0
        if not skip_finger_table:
            self._finger_table = [self._get_null_object()
                                  for _ in range(BITS_IN_ADDRESS)]

    @abstractmethod
    def _get_null_object(self) -> T:
        pass

    @abstractmethod
    def find_successor(self, digest: int, hops: int = 0) -> tuple[T, int]:
        pass

    def _successor_owns_digest(self, digest: int) -> bool:
        return Node.address_in_range(digest, self.id, self.successor.id, inclusive_upper=True)

    def set_successor(self, value: T) -> None:
        self._finger_table[0] = value

    def set_finger_table_at(self, index: int, value: T) -> None:
        self._finger_table[index] = value

    def finger_table_at(self, index: int) -> T:
        return self._finger_table[index]

    @abstractmethod
    def as_node_data(self) -> NodeData:
        pass

    @property
    def id(self) -> int:
        return self.__digest_id

    @property
    def predecessor(self) -> T:
        return self.__predecessor

    @predecessor.setter
    def predecessor(self, value: T) -> None:
        self.__predecessor = value

    @staticmethod
    def address_in_range(target: int, lower_bound: int, upper_bound: int, inclusive_upper: bool = False) -> bool:
        # >= 0 check to handle null-object nodes (which have their ID set to -1)
        return all([val >= 0 for val in [target, lower_bound, upper_bound]]) and\
            mod_in_range(target, lower_bound, upper_bound,
                         ADDRESS_SPACE_SIZE, inclusive_upper)

    @property
    def finger_table(self) -> list[T]:
        return self._finger_table

    @property
    def successor(self) -> T:
        return self.finger_table[0]

    @successor.setter
    def successor(self, value: T) -> None:
        self.finger_table[0] = value
