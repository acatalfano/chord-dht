from typing import Callable
from .node import Node


class VirtualNodeManager:
    def __init__(self, name: str, id_method: Callable[[str], int]) -> None:
        self.__id_method = id_method
        self.__base_name = name
        self.__nodes: list[Node] = []

    @staticmethod
    def create_new_ring(name: str, id_method: Callable[[str], int]) -> 'VirtualNodeManager':
        manager = VirtualNodeManager(name, id_method)
        node = Node.create_new_ring(name, id_method)
        manager.nodes.append(node)
        return manager

    @staticmethod
    def create_and_join_ring(name: str, id_method: Callable[[str], int], target_node: Node) -> 'VirtualNodeManager':
        manager = VirtualNodeManager(name, id_method)
        node = Node(name, id_method)
        node.join_ring(target_node)
        manager.nodes.append(node)
        return manager

    def add_virtual_node(self, count: int = 1) -> None:
        assert(len(self.nodes) >= 1)
        for _ in range(count):
            node = Node(f'{self.__base_name}_{len(self.__nodes)}',
                        self.__id_method)
            node.join_ring(self.__nodes[0])
            self.__nodes.append(node)

    @property
    def nodes(self) -> list[Node]:
        return self.__nodes
