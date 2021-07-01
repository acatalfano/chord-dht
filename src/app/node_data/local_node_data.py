from typing import Generic, TypeVar, Union
from .node_data import NodeData
from ..node.node import Node

T = TypeVar('T', bound=Node, contravariant=True)


class LocalNodeData(NodeData, Generic[T]):
    def __init__(
        self,
        id_value: int,
        reference: Union[T, None],
        predecessor: Union['LocalNodeData', None] = None,
        successor: Union['LocalNodeData', None] = None,
        recurse: bool = True
    ) -> None:
        self._successor: LocalNodeData
        self._predecessor: LocalNodeData
        super().__init__(id_value, predecessor=predecessor,
                         successor=successor, recurse=recurse)
        self.__reference = reference

    @property
    def reference(self) -> Union[T, None]:
        return self.__reference

    @NodeData.null_object.getter
    def null_object(self) -> 'LocalNodeData':
        return LocalNodeData(-1, None, recurse=False)

    @NodeData.successor.getter
    def successor(self) -> 'LocalNodeData':
        return self._successor

    @NodeData.successor.setter
    def successor(self, value: 'LocalNodeData') -> None:
        self._successor = value

    @NodeData.predecessor.getter
    def predecessor(self) -> 'LocalNodeData':
        return self._predecessor

    @NodeData.predecessor.setter
    def predecessor(self, value: 'LocalNodeData') -> None:
        self._predecessor = value

    def is_nil(self) -> bool:
        return not (hasattr(self, 'reference') and self.reference is not None) or super().is_nil()
