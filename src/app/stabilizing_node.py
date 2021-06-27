from typing import Callable
from time import sleep
from threading import Thread, main_thread
from .abstract_node import AbstractNode
from .CONFIG import BITS_IN_ADDRESS
from .utility.logger import Logger


class StabilizingNode:
    @staticmethod
    def __spin(this_node: AbstractNode, operation: Callable[[AbstractNode], None]) -> None:
        while main_thread().is_alive():
            operation(this_node)
            sleep(1)

    @staticmethod
    def __notify(this_node: AbstractNode, other_node: AbstractNode) -> None:
        if this_node.predecessor._isNil() or AbstractNode.address_in_range(other_node.id, this_node.predecessor.id, this_node.id):
            this_node.predecessor = other_node
            Logger.logger().info('set predecessor of %d to %d',
                                 this_node.id, other_node.id)

    @staticmethod
    def deploy_threads(this_node: AbstractNode) -> None:
        operations: list[Callable[[AbstractNode], None]] = [
            StabilizingNode.stabilize,
            StabilizingNode.fix_fingers,
            StabilizingNode.check_predecessor
        ]
        threads = [Thread(target=StabilizingNode.__spin, args=[
                          this_node, operation]) for operation in operations]
        for t in threads:
            t.start()

    @staticmethod
    def stabilize(this_node: AbstractNode) -> None:
        successor_predecessor = this_node.successor.predecessor
        if AbstractNode.address_in_range(successor_predecessor.id, this_node.id, this_node.successor.id):
            this_node.set_successor(successor_predecessor)
            Logger.logger().info('set successor of %d to %d',
                                 this_node.id, successor_predecessor.id)
        StabilizingNode.__notify(this_node.successor, this_node)

    @staticmethod
    def fix_fingers(this_node: AbstractNode) -> None:
        update = this_node.find_chord_successor(
            this_node.id + (2 ** this_node.finger_to_fix))[0]
        if this_node.finger_table[this_node.finger_to_fix] != update:
            Logger.logger().verbose('node %d fix finger[%d] = %d',
                                    this_node.id, this_node.finger_to_fix, update.id)
        this_node.finger_table[this_node.finger_to_fix] = update

        this_node.finger_to_fix = (
            this_node.finger_to_fix + 1) % BITS_IN_ADDRESS

    @staticmethod
    def check_predecessor(this_node: AbstractNode) -> None:
        # TODO: change this to actually check if the predecessor is there once it's up on mininet
        # i.e. use latency
        if not this_node.predecessor._isNil() and this_node.predecessor.id is None:
            Logger.logger().info('clear predecessor of %d', this_node.predecessor.id)
            this_node.predecessor = type(this_node).getNullObject()

    # TODO: later add in the successor list logic if there's time
