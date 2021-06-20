from collections import defaultdict
from random import sample, randrange
from typing import Callable
from app.load_balancing import LoadBalancer
from app import Server


def lb_test(lb_factory: Callable[[list[Server]], LoadBalancer]) -> None:
    server_names = [f'server_{i}' for i in sample(range(100), 31)]
    initial_list = [Server(i) for i in server_names[:-1]]
    load_balancer = lb_factory(initial_list)

    keys = [f'cached_data_{i}' for i in sample(range(100), 10)]
    print('\n--------------------------------')
    print('initial configuration')
    print('--------------------------------\n')
    __print_key_assignments(load_balancer, keys)
    print('\n--------------------------------')
    print('after adding 1 new server')
    print('--------------------------------\n')
    load_balancer.add_server(server_names[-1])
    __print_key_assignments(load_balancer, keys)


def __print_key_assignments(load_balancer: LoadBalancer, keys: list[str]) -> None:
    server_key_map: dict[Server, list[str]] = defaultdict(list)
    for k in keys:
        server_key_map[load_balancer.responsible_server(k)].append(k)

    for server, keys in server_key_map.items():
        key_list = '\n\t' + '\n\t'.join(keys)
        print(f'keys in server {server.name}:{key_list}')
