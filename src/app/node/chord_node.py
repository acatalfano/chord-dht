from abc import abstractmethod
from typing import TypeVar

from ..node_data.node_data import NodeData
from .finger_table_node import FingerTableNode
from .node import Node

T = TypeVar('T', bound=NodeData)


class ChordNode(FingerTableNode[T]):
    def find_successor(self, digest: int, hops: int = 0) -> tuple[T, int]:
        # edge case (results from the key's digest being the same as a node's digest)
        if self.id == digest or self.id == self.successor.id:
            return self.as_node_data(), hops

        if self._successor_owns_digest(digest):
            return self.successor, hops
        else:
            next_node = self.__closest_preceding_node(digest)

            # edge case (results from nodes being directly next to each other)
            if next_node.id == self.id:
                next_node = next_node.successor

            return self._get_next_successor(next_node, digest, hops)

    def __closest_preceding_node(self, digest: int) -> T:
        for finger in reversed(self.finger_table):
            if Node.address_in_range(finger.id, self.id, digest):
                return finger
        return self.as_node_data()

    @abstractmethod
    def _get_next_successor(self, node_data: NodeData, digest: int, hops: int) -> tuple[T, int]:
        pass

    @abstractmethod
    def _get_null_object(self) -> T:
        pass

    @abstractmethod
    def as_node_data(self) -> T:
        pass
