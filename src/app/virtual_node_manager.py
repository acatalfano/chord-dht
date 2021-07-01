from typing import Callable
from .node.local_stabilizing_node import LocalStabilizingNode


class VirtualNodeManager:
    def __init__(self, name: str, id_method: Callable[[str], int]) -> None:
        self.__id_method = id_method
        self.__base_name = name
        self.__nodes: list[LocalStabilizingNode] = []

    @staticmethod
    def create_new_ring(name: str, id_method: Callable[[str], int]) -> 'VirtualNodeManager':
        manager = VirtualNodeManager(name, id_method)
        node = LocalStabilizingNode.create_new_ring(name, id_method)
        manager.nodes.append(node)
        return manager

    @staticmethod
    def create_and_join_ring(name: str, id_method: Callable[[str], int], target_node: LocalStabilizingNode) -> 'VirtualNodeManager':
        manager = VirtualNodeManager(name, id_method)
        node = LocalStabilizingNode(name, id_method)
        node.join_ring(target_node)
        manager.nodes.append(node)
        return manager

    def add_virtual_node(self, count: int = 1) -> None:
        assert(len(self.nodes) >= 1)
        for _ in range(count):
            node = LocalStabilizingNode(f'{self.__base_name}_{len(self.__nodes)}',
                                        self.__id_method)
            node.join_ring(self.__nodes[0])
            self.__nodes.append(node)

    @property
    def nodes(self) -> list[LocalStabilizingNode]:
        return self.__nodes
