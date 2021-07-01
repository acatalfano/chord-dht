from typing import Callable
from test_helper.hop_test import hop_test
from app.node.local_chord_node import LocalChordNode


def __main__() -> None:
    build_finger_table: Callable[[LocalChordNode], None] =\
        lambda node: node.build_finger_table()
    hop_test(LocalChordNode, build_finger_table)


if __name__ == '__main__':
    __main__()
