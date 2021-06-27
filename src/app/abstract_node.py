from abc import ABC, abstractmethod
from typing import Callable
from .server import Server
from .CONFIG import ADDRESS_SPACE_SIZE
from .utility import mod_in_range


class AbstractNode(Server, ABC):
    def __init__(self, name: str, id_method: Callable[[str], int]) -> None:
        super().__init__(name)
        self._digest_id = id_method(name)
        self.predecessor: AbstractNode
        self.finger_to_fix = 0

    @property
    def id(self) -> int:
        return self._digest_id

    @staticmethod
    def address_in_range(target: int, lower_bound: int, upper_bound: int, inclusive_upper: bool = False) -> bool:
        # >= 0 check to handle null-object nodes (which have their ID set to -1)
        return all([val >= 0 for val in [target, lower_bound, upper_bound]]) and\
            mod_in_range(target, lower_bound, upper_bound,
                         ADDRESS_SPACE_SIZE, inclusive_upper)

    @abstractmethod
    def set_successor(self, value: 'AbstractNode') -> None:
        pass

    @property
    @abstractmethod
    def finger_table(self) -> list['AbstractNode']:
        pass

    @abstractmethod
    def find_chord_successor(self, digest: int, hops: int = 0) -> tuple['AbstractNode', int]:
        pass

    @property
    @abstractmethod
    def successor(self) -> 'AbstractNode':
        pass

    @abstractmethod
    def build_finger_table(self) -> None:
        pass

    @staticmethod
    def getNullObject() -> 'AbstractNode':
        return AbstractNode('null', lambda _: -1)

    def _isNil(self) -> bool:
        return self.id == -1
