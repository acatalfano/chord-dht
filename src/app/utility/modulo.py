def mod_in_range(
    target: int,
    lower_bound: int,
    upper_bound: int,
    address_space: int,
    inclusive_upper: bool = False
) -> bool:
    '''determine if the target is within the range of the lower-bound and the upper-bound, modulo-adjusted

    by default, the lower_bound is non-inclusive and the upper_bound is inclusive,
    but the upper_bound can be set to be an inclusive range via the optional parameter
    '''
    float_upper_bound = (upper_bound
                         + (0.5 * int(inclusive_upper))
                         ) % address_space

    mod_range_size = (float_upper_bound - lower_bound) % address_space
    return (float_upper_bound - target) % address_space < mod_range_size and\
        (target - lower_bound) % address_space < mod_range_size
