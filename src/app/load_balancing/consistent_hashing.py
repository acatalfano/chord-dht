from sortedcontainers import SortedDict
from ..server import Server
from ..hash_function import hash_function
from .load_balancer import LoadBalancer


class ConsistentHashing(LoadBalancer):
    '''a class that implements consistent-hashing lookups

    its underlying storage mechanism is a SortedDict,
    where hashes and Servers are stored.
    collisions are handled by a variation of double-hashing

    the responsible server is located with a binary search of the map's keys
    '''

    def _init_server_storage(self, server_list: list[Server] = None) -> None:
        self.__address_space_map: dict[int, Server] = SortedDict()
        self.__map_capacity = 2 ** 8
        for server in server_list or []:
            self.add_server(server.name)

    def add_server(self, name: str) -> None:
        '''create and add a Server to the location that its name hashes to

        recursively hashes if there is a collision
        refuses to hash if there is no room in the address space
        '''
        if len(self.__address_space_map.keys()) < self.__map_capacity:
            server_hash = hash_function(name)
            while server_hash in self.__address_space_map:
                server_hash = hash_function(f'{server_hash}')

            self.__address_space_map.setdefault(server_hash, Server(name))

    def responsible_server(self, key: str) -> Server:
        server_hash = self.__find_responsible_server_hash(
            hash_function(key)
        )
        server = self.__address_space_map.get(server_hash)
        if server is not None:
            return server
        else:
            raise KeyError(
                f'could not find the responsible server for key: {key}'
            )

    def __find_responsible_server_hash(self, target_hash: int) -> int:
        '''
        find the server responsible for the target hash
        (the server whose hash is the smallest value that's still greater than the target hash)

        this method employs a binary search
        '''

        if target_hash < 0:
            raise ValueError(
                f'target_hash is {target_hash}, must be non-negative')

        address_space = list(self.__address_space_map.keys())

        upper_bound_index = len(address_space)
        lower_bound_index = 0
        candidate = address_space[-1] if len(address_space) > 0 else -1

        while lower_bound_index < upper_bound_index:
            # pick the halfway-point index
            test_index = lower_bound_index + \
                ((upper_bound_index - lower_bound_index) // 2)
            if target_hash % (address_space[-1] + 1) <= address_space[test_index]:
                # subdivide search space towards the lower half
                # and set the next candidate to just past the new search-space
                upper_bound_index = test_index
                candidate = address_space[test_index]
            else:
                # subdivide search space towards the upper half
                # and leave the candidate as it is
                lower_bound_index = test_index + 1

        return candidate
