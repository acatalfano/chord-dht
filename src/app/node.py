import verboselogs
from typing import Callable
from .abstract_node import AbstractNode
from .CONFIG import ADDRESS_SPACE_SIZE, BITS_IN_ADDRESS
from .stabilizing_node import StabilizingNode
from .utility.logger import Logger

# TODO: try something (perhaps decorator pattern for example)
# to separate out the functionality used exclusively for different tasks


class Node(AbstractNode):
    def __init__(self, name: str, id_method: Callable[[str], int], skip_finger_table: bool = False) -> None:
        super().__init__(name, id_method)
        if not skip_finger_table:
            self.__finger_table = [Node.getNullObject()
                                   for _ in range(BITS_IN_ADDRESS)]

    # NAIVE TASK
    def find_successor(self, digest: int, hops: int = 0) -> tuple['Node', int]:
        '''this method is used for naïve chord routing
        '''
        if self._successor_owns_digest(digest):
            return self.successor, hops
        else:
            return self.successor.find_successor(digest, hops + 1)

    # CHORD ROUTING TASK
    def find_chord_successor(self, digest: int, hops: int = 0) -> tuple['Node', int]:
        '''this method is used for "real" chord routing
        '''
        # edge case (results from the key's digest being the same as a node's digest)
        if self.id == digest or self.id == self.successor.id:
            return self, hops

        if self._successor_owns_digest(digest):
            return self.successor, hops
        else:
            next_node = self.closest_preceding_node(digest)

            # edge case (results from nodes being directly next to each other)
            if next_node.id == self.id:
                next_node = next_node.successor

            return next_node.find_chord_successor(digest, hops + 1)

    def closest_preceding_node(self, digest: int) -> 'Node':
        for finger in reversed(self.finger_table):
            if Node.address_in_range(finger.id, self.id, digest):
                return finger
        return self

    def _successor_owns_digest(self, digest: int) -> bool:
        return Node.address_in_range(digest, self.id, self.successor.id, inclusive_upper=True)

    def set_successor(self, value: 'Node') -> None:
        self.__finger_table[0] = value

    def build_finger_table(self) -> None:
        self.__finger_table: list[Node] = [
            self.find_successor(
                (self.id + (2 ** k)) % ADDRESS_SPACE_SIZE,
                0
            )[0]
            for k in range(BITS_IN_ADDRESS)
        ]

    def join_ring(self, other_node: 'Node') -> None:
        self.predecessor: Node = Node.getNullObject()
        successor, _ = other_node.find_chord_successor(self.id)
        self.set_successor(successor)
        Logger.logger().info('Node %d join ring with successor node %d',
                             self.id, self.successor.id)
        StabilizingNode.deploy_threads(self)

    @staticmethod
    def create_new_ring(name: str, id_method: Callable[[str], int]) -> 'Node':
        node = Node(name, id_method)
        node.__finger_table[0] = node
        node.predecessor = Node.getNullObject()
        Logger.logger().info('Start a ring with node %d', node.id)
        StabilizingNode.deploy_threads(node)
        return node

    @property
    def finger_table(self) -> list['Node']:
        return self.__finger_table

    @property
    def successor(self) -> 'Node':
        return self.finger_table[0]

    @staticmethod
    def getNullObject() -> 'Node':
        node = Node('null', lambda _: -1, skip_finger_table=True)
        node.__finger_table = [node]
        node.predecessor = node
        return node
