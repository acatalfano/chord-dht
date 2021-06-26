from typing import Callable
from .server import Server
from .utility import mod_in_range
from .CONFIG import ADDRESS_SPACE_SIZE, BITS_IN_ADDRESS


class Node(Server):
    def __init__(self, name: str, id_method: Callable[[str], int]) -> None:
        super().__init__(name)
        self._digest_id = id_method(name)

    def set_successor(self, successor: 'Node') -> None:
        self._successor = successor

    def find_successor(self, digest: int, hops: int = 0) -> tuple['Node', int]:
        '''this method is used for naïve chord routing
        '''
        if self._successor_owns_digest(digest):
            return (self._successor, hops)
        else:
            return self._successor.find_successor(digest, hops + 1)

    def find_chord_successor(self, digest: int, hops: int = 0) -> tuple['Node', int]:
        '''this method is used for "real" chord routing
        '''

        # edge case (results from the key's digest being the same as a node's digest)
        if self.id == digest:
            return self, hops

        if self._successor_owns_digest(digest):
            return self._successor, hops
        else:
            next_node = self.closest_preceding_node(digest)

            # edge case (results from nodes being directly next to each other)
            if next_node.id == self.id:
                next_node = next_node._successor

            return next_node.find_chord_successor(digest, hops + 1)

    def closest_preceding_node(self, digest: int) -> 'Node':
        for finger in reversed(self.__finger_table):
            if mod_in_range(finger.id, self.id, digest, ADDRESS_SPACE_SIZE):
                return finger
        return self

    def _successor_owns_digest(self, digest: int) -> bool:
        return mod_in_range(digest, self.id, self._successor.id, ADDRESS_SPACE_SIZE, inclusive_upper=True)

    def build_finger_table(self) -> None:
        self.__finger_table: list[Node] = [
            self.find_successor(
                (self.id + (2 ** k)) % ADDRESS_SPACE_SIZE,
                0
            )[0]
            for k in range(BITS_IN_ADDRESS)
        ]

    @property
    def finger_table(self) -> list['Node']:
        return self.__finger_table

    @property
    def id(self) -> int:
        return self._digest_id
