from app.node.node import Node
from app.node_data.node_data import NodeData
from .chord_node import ChordNode
from ..node_data.local_node_data import LocalNodeData


class LocalChordNode(ChordNode[LocalNodeData[ChordNode]]):
    def _get_next_successor(self, node_data: LocalNodeData, digest: int, hops: int) -> tuple[LocalNodeData, int]:
        assert(node_data.reference is not None)
        return node_data.reference.find_successor(digest, hops + 1)

    def _get_null_object(self) -> LocalNodeData:
        return LocalNodeData(-1, self)

    def as_node_data(self) -> LocalNodeData:
        return LocalNodeData(self.id, self, self.predecessor, self.successor)
