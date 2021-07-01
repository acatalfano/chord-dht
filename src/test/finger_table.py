from test_helper.build_ring import build_ring
from random import seed, choice
from app.node.naive_node import NaiveNode


def __main__():
    nodes = build_ring(10, lambda x, y: NaiveNode(x, y))
    print('--------------------------------')
    print('node configuration (name: id)')
    print('--------------------------------')
    node_config = [f'{n.name}: {n.id}' for n in nodes]
    print('\n'.join(node_config))

    seed(0)
    target_node = choice(nodes)
    target_node.build_finger_table()

    print('--------------------------------')
    print(f'node (id)\n    {target_node.name}: {target_node.id}\n')
    print('finger table (k-value -- id)')
    finger_list = [f'{k} -- {node.id}' for k,
                   node in enumerate(target_node.finger_table, start=1)]
    print('\n'.join(finger_list))
    print('--------------------------------')


if __name__ == '__main__':
    __main__()
