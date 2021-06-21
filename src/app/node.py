from .server import Server


class Node(Server):
    def __init__(self, name: str, id: int) -> None:
        super().__init__(name)
        self.__digest_id = id

    def set_successor(self, successor: 'Node') -> None:
        self.__successor = successor

    @property
    def id(self) -> int:
        return self.__digest_id

    def find_successor(self, digest: int, hops: int = 0) -> tuple['Node', int]:
        successor_id = self.__successor.id
        if (self.id < digest and digest <= successor_id) or (successor_id <= digest and digest < self.id):
            return (self.__successor, hops)
        else:
            return self.__successor.find_successor(digest, hops + 1)
