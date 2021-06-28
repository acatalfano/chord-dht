from hashlib import md5
from .CONFIG import HEX_DIGITS_IN_ADDRESS, ADDRESS_SPACE_SIZE


class HashFunction:
    def __init__(self) -> None:
        self.__previous_hashes: list[int] = []

    def hash_function(self, val: str) -> int:
        current_hash = self.__hash_function(val)

        index = 1
        while current_hash in self.__previous_hashes:
            current_hash = (current_hash + (index ** 2)) % ADDRESS_SPACE_SIZE

        self.__previous_hashes.append(current_hash)
        return current_hash

    def __hash_function(self, val: str) -> int:
        '''1-byte hash function
        a function that computes a 1-byte hash of a string
        by grabbing the least significant byte as an int
        from the MD5 algorithm
        '''
        hash_val = md5(bytes(val, 'ascii')
                       ).hexdigest()[-HEX_DIGITS_IN_ADDRESS:]
        return int(hash_val, 16)
