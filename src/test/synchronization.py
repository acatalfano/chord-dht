import logging
from time import sleep
from random import seed, sample, choice
from app.node import Node
from app.hash_function import hash_function
from app.utility.logger import Logger
import argparse
import verboselogs


def __main__():
    print('press ENTER to start\nthen let the activity settle down\n'
          'then press ENTER to see the effects on one node joining the network\n'
          'then press ENTER to end\n\n\n'
          )
    input('')
    seed(0)
    node_names = [f'serve_{i}' for i in sample(
        range(100), 12)]
    ring: list[Node] = [Node.create_new_ring(node_names.pop(), hash_function)]
    next_nodes = [Node(name, hash_function) for name in node_names[:-1]]
    nxt = next_nodes[0]
    initial = ring[0]

    ring.append(nxt)

    sleep(1)
    nxt.join_ring(initial)
    for n in next_nodes:
        ring.append(n)
        n.join_ring(ring[0])

    target_node = choice(ring)
    new_node = Node(node_names[-1], hash_function)

    input('')
    print('\n\n\n\n')

    new_node.join_ring(target_node)

    ring.append(new_node)

    input('')

    for n in ring:
        print(f'{n.predecessor.id} <-- {n.id} --> {n.successor.id}')

    for n in ring:
        print(f'{n.id} finger table')
        for i, f in enumerate(n.finger_table):
            print(f'\t{i} -- {f.id}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    Logger.logger().setLevel(verboselogs.VERBOSE if args.verbose else logging.INFO)
    __main__()
