from hashlib import md5
from .CONFIG import HEX_DIGITS_IN_ADDRESS


def hash_function(val: str) -> int:
    '''1-byte hash function
    a function that computes a 1-byte hash of a string
    by grabbing the least significant byte as an int
    from the MD5 algorithm
    '''
    hash_val = md5(bytes(val, 'ascii')).hexdigest()[-HEX_DIGITS_IN_ADDRESS:]
    return int(hash_val, 16)
