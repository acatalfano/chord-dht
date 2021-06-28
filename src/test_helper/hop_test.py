from typing import Callable
from app.hash_function import HashFunction
from app.node import Node
from random import seed, sample
from itertools import product

from test_helper.build_ring import build_ring

FindSuccessorCallable = Callable[[Node, int], tuple[Node, int]]


def hop_test(find_successor: FindSuccessorCallable, build_finger_table: bool = False) -> None:
    seed(0)
    __measure_routing_for_network_size_of(
        50, find_successor, build_finger_table)
    __measure_routing_for_network_size_of(
        100, find_successor, build_finger_table)


def __measure_routing_for_network_size_of(size: int, find_successor: FindSuccessorCallable, build_finger_table: bool) -> None:
    keys_hash = HashFunction()
    ring = build_ring(size)
    if build_finger_table:
        for n in ring:
            n.build_finger_table()
    keys_and_digests = [(k, keys_hash.hash_function(k)) for k in [
        f'data_{i}' for i in sample(range(100_000), 100)
    ]]

    results = [find_successor(node, digest)[1] for node, (_, digest) in list(
        product(ring, keys_and_digests))]

    average = sum(results) / len(results)

    print(f'for {size} nodes, the average hop size is: {average}')
