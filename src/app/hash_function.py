from hashlib import md5


def hash_function(val: str) -> int:
    '''
        a function that computes a 1-byte hash of a string
        by grabbing the least significant byte as an int
        from the MD5 algorithm
        '''
    hash_val = md5(bytes(val, 'ascii')).hexdigest()[-2:]
    return int(hash_val, 16)
