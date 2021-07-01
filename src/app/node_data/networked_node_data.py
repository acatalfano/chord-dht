from enum import Enum
from typing import NewType, Union
import zmq
from .node_data import NodeData
from ..network.CONFIG import HOP_DESTINATION_PORT, SUCCESSOR_PREDECESSOR_PORT, NOTIFY_PORT, TIMEOUT


class NodeType(Enum):
    SuccessorNode = 1
    CurrentNode = 2
    PredecessorNode = 3
    OtherFingerNode = 4


class NetworkedNodeData(NodeData):
    def __init__(
        self,
        id_value: int,
        ip_address: str,
        predecessor: Union['NetworkedNodeData', None] = None,
        successor: Union['NetworkedNodeData', None] = None,
        node_type: NodeType = NodeType.OtherFingerNode,
        recurse: bool = True
    ) -> None:
        super().__init__(id_value, predecessor=predecessor,
                         successor=successor, recurse=recurse)
        self.__node_type = node_type
        self.__ip_address = ip_address
        self.__context = zmq.Context.instance()
        self.__try_connect_finger_socket()
        self.__try_connect_predecessor_socket()
        self.__try_connect_notify_socket()

    def __del__(self) -> None:
        self.finger_socket.close()

    def __try_connect_predecessor_socket(self, close: bool = False) -> None:
        if self.__node_type in [NodeType.CurrentNode, NodeType.SuccessorNode]:
            if close:
                self.__predecessor_socket.close()
            self.__predecessor_socket = self.__context.socket(zmq.REQ)
            self.__predecessor_socket.setsockopt(zmq.RCVTIMEO, TIMEOUT)
            self.__predecessor_socket.connect(
                f'tcp://{self.__ip_address}:{SUCCESSOR_PREDECESSOR_PORT}')

    def __try_connect_notify_socket(self, close: bool = False) -> None:
        if self.__node_type == NodeType.CurrentNode:
            if close:
                self.__notify_socket.close()
            self.__notify_socket = self.__context.socket(zmq.REQ)
            self.__notify_socket.setsockopt(zmq.RCVTIMEO, TIMEOUT)
            self.__notify_socket.connect(
                f'tcp://{self.__ip_address}:{NOTIFY_PORT}')

    def __try_connect_finger_socket(self, close: bool = False) -> None:
        if self.__node_type != NodeType.PredecessorNode:
            if close:
                self.__finger_socket.close()
            self.__finger_socket = self.__context.socket(zmq.REQ)
            self.__finger_socket.setsockopt(zmq.RCVTIMEO, TIMEOUT)
            self.__finger_socket.connect(
                f'tcp://{self.__ip_address}:{HOP_DESTINATION_PORT}')

    @property
    def finger_socket(self) -> zmq.Socket:
        if self.__node_type == NewType.PredecessorNode:
            raise TypeError('Finger Socket is not for the predecessor!')
        return self.__finger_socket

    @property
    def predecessor_socket(self) -> zmq.Socket:
        if self.__node_type == NodeType.OtherFingerNode:
            raise TypeError(
                'Predecessor socket is only for self or the successor!')
        return self.__predecessor_socket

    @property
    def notify_socket(self) -> zmq.Socket:
        if self.__node_type != NodeType.SuccessorNode:
            raise TypeError('Notify socket is only for the successor!')
        return self.__notify_socket

    def update(self, id_value: int, ip_address: str = None) -> None:
        if ip_address is not None:
            self.id = id_value
            self.__ip_address = ip_address
            self.__try_connect_finger_socket(close=True)
            self.__try_connect_notify_socket(close=True)
            self.__try_connect_predecessor_socket(close=True)

    def clear(self) -> None:
        self.id = -1
        self.__ip_address = ''
        self.__finger_socket.close()
        self.__notify_socket.close()
        self.__predecessor_socket.close()

    @property
    def ip_address(self) -> str:
        return self.__ip_address

    @NodeData.null_object.getter
    def null_object(self) -> 'NetworkedNodeData':
        return NetworkedNodeData(-1, '')
