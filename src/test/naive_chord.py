from typing import Callable
from app.hash_function import hash
from app.node import Node
from random import sample
from itertools import product

# TODO: FAILS W/ EXCEPTION CURRENTLY...

SERVER_NAME_PREFIX = 'server_'


def __main__() -> None:
    __measure_routing_for_network_size_of(50)
    __measure_routing_for_network_size_of(100)


def __measure_routing_for_network_size_of(size: int) -> None:
    names_and_ids = [(name, hash(name)) for name in [
        f'{SERVER_NAME_PREFIX}{i}' for i in sample(range(100), size)]]
    names_and_ids.sort(key=lambda x: x[1])
    nodes = [Node(name, id) for name, id in names_and_ids]
    for current_node, next_node in zip(nodes, nodes[1:] + nodes[:1]):
        current_node.set_successor(next_node)

    keys_and_digests = [(k, hash(k)) for k in [
        f'data_{i}' for i in sample(range(100_000), 100)
    ]]

    results = [node.find_successor(digest)[1] for node, (_, digest) in list(
        product(nodes, keys_and_digests))]

    average = sum(results) / len(results)

    print(f'for {size} nodes, the average hop size is: {average}')


if __name__ == '__main__':
    __main__()
