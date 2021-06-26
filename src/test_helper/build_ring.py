from app.hash_function import hash_function
from app.node import Node
from random import seed, sample

SERVER_NAME_PREFIX = 'server_'


def build_ring(size: int) -> list[Node]:
    seed(0)
    node_names = [f'{SERVER_NAME_PREFIX}{i}' for i in sample(range(100), size)]
    nodes = [Node(name, hash_function) for name in node_names]
    nodes.sort(key=lambda x: x.id)
    for current_node, next_node in zip(nodes, nodes[1:] + nodes[:1]):
        current_node.set_successor(next_node)

    for n in nodes:
        n.build_finger_table()

    return nodes
