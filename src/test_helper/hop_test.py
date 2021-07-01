from typing import Callable
from app.hash_function import HashFunction
from app.node.finger_table_node import FingerTableNode
from random import seed, sample
from itertools import product

from test_helper.build_ring import build_ring

NodeFactory = Callable[[str, Callable[[str], int]], FingerTableNode]


def hop_test(node_factory: NodeFactory, setup_callback: Callable = None) -> None:
    seed(0)
    __measure_routing_for_network_size_of(50, node_factory)
    __measure_routing_for_network_size_of(100, node_factory)


def __measure_routing_for_network_size_of(size: int, node_factory: NodeFactory) -> None:
    keys_hash = HashFunction()
    ring = build_ring(size, node_factory)
    keys_and_digests = [(k, keys_hash.hash_function(k)) for k in [
        f'data_{i}' for i in sample(range(100_000), 100)
    ]]

    results = [node.find_successor(digest)[1] for node, (_, digest) in list(
        product(ring, keys_and_digests))]

    average = sum(results) / len(results)

    print(f'for {size} nodes, the average hop size is: {average}')
