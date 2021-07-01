from abc import ABC, abstractmethod, abstractproperty
from typing import Union


class NodeData(ABC):
    def __init__(
        self,
        id_value: int,
        predecessor: Union['NodeData', None] = None,
        successor: Union['NodeData', None] = None,
        recurse: bool = True
    ) -> None:
        self.id = id_value
        if recurse:
            self._predecessor: NodeData = predecessor if predecessor is not None else self.null_object
            self._successor: NodeData = successor if successor is not None else self.null_object

    def update(self, id_value: int) -> None:
        self.id = id_value

    def is_nil(self) -> bool:
        return self.id == -1

    @property
    def successor(self) -> 'NodeData':
        return self._successor

    @successor.setter
    def successor(self, value: 'NodeData') -> None:
        self._successor = value

    @property
    def predecessor(self) -> 'NodeData':
        return self._predecessor

    @predecessor.setter
    def predecessor(self, value: 'NodeData') -> None:
        self._predecessor = value

    @property
    @abstractmethod
    def null_object(self) -> 'NodeData':
        pass
