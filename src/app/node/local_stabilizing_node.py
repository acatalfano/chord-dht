
from typing import Callable
from threading import Thread, main_thread
from time import sleep

from .stabilizing_node import StabilizingNode
from ..node_data.local_node_data import LocalNodeData
from .node import Node
from ..utility.logger import Logger


class LocalStabilizingNode(StabilizingNode[LocalNodeData[StabilizingNode]]):
    @staticmethod
    def create_new_ring(name: str, id_method: Callable[[str], int]) -> 'LocalStabilizingNode':
        node = LocalStabilizingNode(name, id_method)
        node._finger_table[0] = node.as_node_data()
        node.predecessor = node._get_null_object()
        Logger.logger().info('Start a ring with node %d', node.id)
        node._deploy_stabilizing_tasks()
        return node

    @staticmethod
    def __spin(operation: Callable[[], None]) -> None:
        while main_thread().is_alive():
            operation()
            sleep(1)

    def _deploy_stabilizing_tasks(self) -> None:
        operations: list[Callable[[], None]] = [
            self._stabilize,
            self._fix_fingers,
            self._check_predecessor
        ]
        threads = [Thread(target=LocalStabilizingNode.__spin, args=[operation])
                   for operation in operations]
        for t in threads:
            t.start()

    def _get_successor_predecessor(self) -> LocalNodeData:
        assert(self.successor.reference is not None)
        return self.successor.reference.predecessor

    def _get_next_successor(self, node_data: LocalNodeData, digest: int, hops: int) -> tuple[LocalNodeData, int]:
        assert(node_data.reference is not None)
        return node_data.reference.find_successor(digest, hops)

    def _notify_successor(self, potential_predecessor: LocalNodeData) -> None:
        assert(self.successor.reference is not None)
        self.successor.reference._notify(potential_predecessor)

    def _get_null_object(self) -> LocalNodeData:
        return LocalNodeData(-1, None)

    def as_node_data(self) -> LocalNodeData:
        return LocalNodeData(self.id, self, self.predecessor, self.successor)
