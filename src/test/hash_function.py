import sys
from app import hash


def __main__() -> None:
    if len(sys.argv) == 2:
        unhashed = sys.argv[1]
        hash_value = hash(unhashed)
        print(f'the hash of {unhashed} is {hash_value}')
    else:
        print('pass 1 argument to hash')


if __name__ == '__main__':
    __main__()
