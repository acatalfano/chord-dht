from abc import ABC, abstractmethod
from typing import Callable, TypeVar

from .node import Node
from ..node_data.node_data import NodeData
from .chord_node import ChordNode
from ..utility.logger import Logger
from ..CONFIG import BITS_IN_ADDRESS

T = TypeVar('T', bound=NodeData)


class StabilizingNode(ChordNode[T], ABC):
    def build_finger_table(self) -> None:
        # don't want this functionality in this class
        pass

    def join_ring(self, other_node: Node) -> None:
        self.predecessor = self._get_null_object()
        successor, _ = other_node.find_successor(self.id)
        self.set_successor(successor)
        Logger.logger().info('Node %d join ring with successor node %d',
                             self.id, self.successor.id)
        self._deploy_stabilizing_tasks()

    @abstractmethod
    def _deploy_stabilizing_tasks(self) -> None:
        pass

    @abstractmethod
    def _notify_successor(self, potential_predecessor: T) -> None:
        pass

    def _notify(self, other_node: T) -> None:
        if self.predecessor.is_nil() or Node.address_in_range(other_node.id, self.predecessor.id, self.id):
            self.predecessor = other_node
            Logger.logger().info('set predecessor of %d to %d',
                                 self.id, other_node.id)

    def _stabilize(self) -> None:
        successor_predecessor = self._get_successor_predecessor()
        if Node.address_in_range(successor_predecessor.id, self.id, self.successor.id):
            self.successor = successor_predecessor
            Logger.logger().info('set successor of %d to %d',
                                 self.id, successor_predecessor.id)
        self._notify_successor(self.as_node_data())

    def _fix_fingers(self) -> None:
        update = self.find_successor(
            self.id + (2 ** self.finger_to_fix))[0]
        if self.finger_table_at(self.finger_to_fix).id != update.id:
            Logger.logger().verbose('node %d fix finger[%d] = %d',
                                    self.id, self.finger_to_fix, update.id)
        self.set_finger_table_at(self.finger_to_fix, update)

        self.finger_to_fix = (
            self.finger_to_fix + 1) % BITS_IN_ADDRESS

    def _check_predecessor(self) -> None:
        # nothing to do in the local scenario. override for the network scenario
        # only here for good book-keeping
        pass

    @abstractmethod
    def _get_successor_predecessor(self) -> T:
        pass
