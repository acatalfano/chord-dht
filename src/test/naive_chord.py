from app.hash_function import hash_function
from random import seed, sample
from itertools import product

from test_helper.build_ring import build_ring


def __main__() -> None:
    seed(0)
    __measure_routing_for_network_size_of(50)
    __measure_routing_for_network_size_of(100)


def __measure_routing_for_network_size_of(size: int) -> None:
    ring = build_ring(size)
    keys_and_digests = [(k, hash_function(k)) for k in [
        f'data_{i}' for i in sample(range(100_000), 100)
    ]]

    results = [node.find_successor(digest)[1] for node, (_, digest) in list(
        product(ring, keys_and_digests))]

    average = sum(results) / len(results)

    print(f'for {size} nodes, the average hop size is: {average}')


if __name__ == '__main__':
    __main__()
