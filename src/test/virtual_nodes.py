from math import sqrt
from app.virtual_node_manager import VirtualNodeManager
from app.node import Node
from app.CONFIG import ADDRESS_SPACE_SIZE
from app.hash_function import HashFunction
from random import seed, sample


def __main__() -> None:
    seed(0)
    node_names = [f'node_{i}' for i in sample(range(100_000), 20)]
    __test_physical_ring(node_names)
    __test_virtual_ring(node_names)


def __test_physical_ring(node_names: list[str]) -> None:
    hasher = HashFunction()
    first_node = Node.create_new_ring(node_names[0], hasher.hash_function)
    other_nodes = [Node(f'node_{i}', hasher.hash_function)
                   for i in node_names[1:]]
    for n in other_nodes:
        n.join_ring(first_node)

    ring = [first_node, *other_nodes]
    responsible_ranges = __responsible_ranges(ring)

    print(
        f'standard deviation for physical 20-ring: {__standard_deviation(responsible_ranges)}')


def __test_virtual_ring(node_names: list[str]) -> None:
    hasher = HashFunction()
    first_manager = VirtualNodeManager.create_new_ring(
        node_names[0], hasher.hash_function)
    first_node = first_manager.nodes[0]
    other_managers = [VirtualNodeManager.create_and_join_ring(
        name, hasher.hash_function, first_node) for name in node_names[1:]]

    for manager in [first_manager, *other_managers]:
        manager.add_virtual_node(9)

    nodes_per_physical = [m.nodes for m in [first_manager, *other_managers]]
    ring = [n for nodes in nodes_per_physical for n in nodes]
    responsible_ranges = __responsible_ranges(ring)
    print(
        f'standard deviation for virtual 200-ring: {__standard_deviation(responsible_ranges)}')


def __responsible_ranges(ring: list[Node]) -> list[int]:
    ring.sort(key=lambda x: x.id)
    node_successor_pairs = list(zip(ring, ring[1:] + ring[:1]))
    return [(successor.id - node.id) % ADDRESS_SPACE_SIZE
            for node, successor in node_successor_pairs]


def __standard_deviation(values: list[int]) -> float:
    average = sum(values) / len(values)
    return sqrt(sum([(x - average) ** 2 for x in values]) / len(values))


if __name__ == '__main__':
    __main__()
