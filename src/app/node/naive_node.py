from ..node_data.local_node_data import LocalNodeData
from .finger_table_node import FingerTableNode


class NaiveNode(FingerTableNode[LocalNodeData]):
    def find_successor(self, digest: int, hops: int = 0) -> tuple[LocalNodeData, int]:
        if self._successor_owns_digest(digest):
            return self.successor, hops
        else:
            assert(not self.successor.is_nil()
                   and self.successor.reference is not None)
            return self.successor.reference.find_successor(digest, hops + 1)

    def _get_null_object(self) -> LocalNodeData:
        return LocalNodeData(-1, None)

    def as_node_data(self) -> LocalNodeData:
        return LocalNodeData(self.id, self)
