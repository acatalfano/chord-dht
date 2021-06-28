from test_helper.hop_test import hop_test


def __main__() -> None:
    hop_test(
        lambda node, digest: node.find_chord_successor(digest),
        build_finger_table=True
    )


if __name__ == '__main__':
    __main__()
