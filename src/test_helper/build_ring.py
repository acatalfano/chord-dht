from typing import Callable
from app.hash_function import HashFunction
from app.node.finger_table_node import FingerTableNode
from random import seed, sample

SERVER_NAME_PREFIX = 'server_'
NodeFactory = Callable[[str, Callable[[str], int]], FingerTableNode]


def build_ring(size: int, node_factory: NodeFactory) -> list[FingerTableNode]:
    seed(0)
    nodes_hash = HashFunction()
    node_names = [f'{SERVER_NAME_PREFIX}{i}' for i in sample(range(100), size)]
    nodes = [node_factory(name, nodes_hash.hash_function)
             for name in node_names]
    nodes.sort(key=lambda x: x.id)
    for current_node, next_node in zip(nodes, nodes[1:] + nodes[:1]):
        current_node.set_successor(next_node.as_node_data())

    for n in nodes:
        n.build_finger_table()

    return nodes
