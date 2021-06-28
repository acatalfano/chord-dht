import sys
from app.hash_function import HashFunction


def __main__() -> None:
    if len(sys.argv) == 2:
        unhashed = sys.argv[1]
        hash_value = HashFunction().hash_function(unhashed)
        print(f'the hash of {unhashed} is {hash_value}')
    else:
        print('pass 1 argument to hash')


if __name__ == '__main__':
    __main__()
