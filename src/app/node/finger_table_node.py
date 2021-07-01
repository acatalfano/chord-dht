from typing import TypeVar
from .node import Node
from ..node_data.node_data import NodeData
from ..CONFIG import ADDRESS_SPACE_SIZE, BITS_IN_ADDRESS

T = TypeVar('T', bound=NodeData, covariant=True)


class FingerTableNode(Node[T]):
    def build_finger_table(self) -> None:
        self._finger_table: list[T] = [
            self.find_successor(
                (self.id + (2 ** k)) % ADDRESS_SPACE_SIZE,
                0
            )[0]
            for k in range(BITS_IN_ADDRESS)
        ]
