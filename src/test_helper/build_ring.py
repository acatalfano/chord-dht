from app.hash_function import HashFunction
from app.node import Node
from random import seed, sample
from app.CONFIG import ADDRESS_SPACE_SIZE, BITS_IN_ADDRESS

SERVER_NAME_PREFIX = 'server_'


def __build_finger_table(node: Node) -> None:
    node.__finger_table = [
        node.find_successor(
            (node.id + (2 ** k)) % ADDRESS_SPACE_SIZE,
            0
        )[0]
        for k in range(BITS_IN_ADDRESS)
    ]


def build_ring(size: int) -> list[Node]:
    seed(0)
    nodes_hash = HashFunction()
    node_names = [f'{SERVER_NAME_PREFIX}{i}' for i in sample(range(100), size)]
    nodes = [Node(name, nodes_hash.hash_function) for name in node_names]
    nodes.sort(key=lambda x: x.id)
    for current_node, next_node in zip(nodes, nodes[1:] + nodes[:1]):
        current_node.set_successor(next_node)

    for n in nodes:
        __build_finger_table(n)

    return nodes
