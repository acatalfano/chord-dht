from itertools import product
from app.utility import mod_in_range


if __name__ == '__main__':
    print('exclusive upper:')
    result = [f'{d} in ({lb}, {ub})' for (
        d, lb, ub) in product(range(3), range(3), range(3)) if mod_in_range(d, lb, ub, 3)]
    print('\n'.join(result))

    print('\ninclusive upper:')

    result = [f'{d} in ({lb}, {ub})' for (
        d, lb, ub) in product(range(3), range(3), range(3)) if mod_in_range(d, lb, ub, 3, inclusive_upper=True)]
    print('\n'.join(result))
