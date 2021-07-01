import json
from threading import Thread
import zmq
from .CONFIG import KEY_SERVER_PORT, HOP_DESTINATION_PORT, SUCCESSOR_PREDECESSOR_PORT, NOTIFY_PORT, TIMEOUT
from typing import Callable, TypedDict
from ..node.stabilizing_node import StabilizingNode
from ..node_data.networked_node_data import NetworkedNodeData, NodeType


class RoutingDto(TypedDict):
    id: int
    ip: str
    hops: int


class NodeLocationDto(TypedDict):
    id: int
    ip: str


class NetworkedNode(StabilizingNode[NetworkedNodeData]):
    def __init__(self, ip_address: str, keyserver_ip: str) -> None:
        self.__keyserver_ip = keyserver_ip
        self.__context = zmq.Context.instance()
        self.__build_sockets()
        self.__predecessor_successor_socket: zmq.Socket\
            = self.__context.socket(zmq.REQ)
        id_value = self.__register_with_keyserver(ip_address)
        self.__node_data = NetworkedNodeData(id_value, ip_address)
        super().__init__(ip_address, lambda _: id_value,
                         skip_finger_table=True)

    def create_new_ring(self) -> None:
        self._finger_table[0] = self.as_node_data()
        self.predecessor = self._get_null_object()
        print('Start a ring with node %d', self.id)
        self._deploy_stabilizing_tasks()
        self.__poll()

    def join_ring(self, other_ip: str) -> None:
        self.predecessor = self._get_null_object()
        successor = self.__find_successor_for_join(other_ip)
        self.set_successor(successor)
        print('Node %d join ring with successor node %d',
              self.id, self.successor.id)
        self._deploy_stabilizing_tasks()
        self.__poll()

    def __find_successor_for_join(self, other_ip: str) -> NetworkedNodeData:
        dummy_successor: NetworkedNodeData = NetworkedNodeData(-1, other_ip)
        dummy_target: NetworkedNodeData = NetworkedNodeData(
            -1, '', successor=dummy_successor, node_type=NodeType.SuccessorNode)
        return self._get_next_successor(dummy_target, self.id, 0)[0]

    def __build_sockets(self) -> None:
        self.__receive_hop_socket = self.__context.socket(zmq.REP)
        self.__receive_hop_socket.setsockopt(zmq.RCVTIMEO, TIMEOUT)
        self.__receive_hop_socket.bind(f'tcp://*:{HOP_DESTINATION_PORT}')
        self.__provide_predecessor_socket = self.__context.socket(zmq.REP)
        self.__provide_predecessor_socket.setsockopt(zmq.RCVTIMEO, TIMEOUT)
        self.__provide_predecessor_socket.bind(
            f'tcp://*:{SUCCESSOR_PREDECESSOR_PORT}')
        self.__receive_notification_socket = self.__context.socket(zmq.REP)
        self.__receive_notification_socket.setsockopt(zmq.RCVTIMEO, TIMEOUT)
        self.__receive_notification_socket.bind(f'tcp://*:{NOTIFY_PORT}')

    def __poll(self) -> None:
        poller = zmq.Poller()
        poller.register(self.__receive_hop_socket)
        poller.register(self.__provide_predecessor_socket)
        poller.register(self.__receive_notification_socket)
        while True:
            socks = dict(poller.poll())
            if self.__receive_hop_socket in socks:
                req: RoutingDto = json.loads(
                    self.__receive_hop_socket.recv_string(zmq.DONTWAIT))
                hops = req['hops']
                target = req['id']
                result_node, result_hops = self.find_successor(
                    target, hops + 1)
                response: RoutingDto = {
                    'id': result_node.id, 'ip': result_node.ip_address, 'hops': result_hops}
                self.__receive_hop_socket.send_string(json.dumps(response))
            if self.__provide_predecessor_socket in socks:
                self.__provide_predecessor_socket.recv(zmq.DONTWAIT)
                resp: NodeLocationDto = {'id': self.id,
                                         'ip': self.__node_data.ip_address}
                self.__provide_predecessor_socket.send_string(json.dumps(resp))
            if self.__receive_notification_socket in socks:
                notification: NodeLocationDto = json.loads(
                    self.__receive_notification_socket.recv_string(zmq.DONTWAIT))
                candidate_predecessor = NetworkedNodeData(
                    notification['id'], notification['ip'])
                self._notify(candidate_predecessor)
                self.__receive_notification_socket.send(b'')

    def __register_with_keyserver(self, ip_address: str) -> int:
        register_socket = self.__context.socket(zmq.REQ)
        register_socket.connect(
            f'tcp://{self.__keyserver_ip}:{KEY_SERVER_PORT}')
        register_socket.send_string(ip_address)
        return int(register_socket.recv_string())

    @property
    def predecessor(self) -> NetworkedNodeData:
        return super().predecessor

    @predecessor.setter
    def predecessor(self, value: NetworkedNodeData) -> None:
        self.__predecessor_successor_socket.close()
        self.__predecessor_successor_socket = self.__context.socket(zmq.REQ)
        self.__predecessor_successor_socket.connect(
            f'tcp://{value.ip_address}:{SUCCESSOR_PREDECESSOR_PORT}')
        super().predecessor = value

    def _check_predecessor(self) -> None:
        if self.__predecessor_has_failed():
            self.predecessor.clear()

    def __predecessor_has_failed(self) -> bool:
        self.__node_data.predecessor_socket.send(b'')
        try:
            # don't care about the message
            # just need to know if anything is received before the timeout
            self.__node_data.predecessor_socket.recv()
            return True
        except zmq.error.Again:
            return False

    def _deploy_stabilizing_tasks(self) -> None:
        operations: list[Callable[[], None]] = [
            self._stabilize,
            self._fix_fingers,
            self._check_predecessor
        ]
        threads = [Thread(target=NetworkedNode.__spin, args=[operation])
                   for operation in operations]
        for t in threads:
            t.start()

    def _notify_successor(self, potential_predecessor: NetworkedNodeData) -> None:
        if not self.successor.is_nil():
            req: NodeLocationDto = {
                'id': potential_predecessor.id, 'ip': potential_predecessor.ip_address}
            self.successor.notify_socket.send_string(json.dumps(req))
            try:
                self.successor.notify_socket.recv()
            except zmq.error.Again:
                # this is where a call to the "next successor" in the successor list would be made
                # but that hasn't been implemented yet
                pass

    def _get_successor_predecessor(self) -> NetworkedNodeData:
        if self.successor.is_nil():
            return self._get_null_object()
        else:
            self.successor.predecessor_socket.send(b'')
            try:
                resp: NodeLocationDto = json.loads(
                    self.successor.predecessor_socket.recv_string())
                return NetworkedNodeData(resp['id'], resp['ip'])
            except zmq.error.Again:
                return self._get_null_object()

    def _get_next_successor(self, node_data: NetworkedNodeData, digest: int, hops: int) -> tuple[NetworkedNodeData, int]:
        req: RoutingDto = {'id': digest, 'hops': hops, 'ip': ''}
        node_data.finger_socket.send(json.dumps(req))
        try:
            resp: RoutingDto = json.loads(
                node_data.finger_socket.recv_string())
            return NetworkedNodeData(resp['id'], resp['ip']), resp['hops']
        except zmq.error.Again:
            return self._get_null_object(), hops

    def _get_null_object(self) -> NetworkedNodeData:
        return NetworkedNodeData(-1, '', recurse=False)

    def as_node_data(self) -> NetworkedNodeData:
        return self.__node_data
