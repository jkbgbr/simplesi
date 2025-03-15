import functools
from simplesi.dimensions import Dimensions


@functools.lru_cache(maxsize=None)
def _get_unit_components_from_dims(dims: Dimensions):
    """
    Returns a list of tuples to represent the current units based
    on the current dimensions. Dimension ignored if 0.
    e.g. [('kg', 1), ('m', -1), ('s', -2)]
    """
    unit_components = []
    unit_symbols = dims._fields
    for idx, dim in enumerate(dims):
        if dim:  # int
            unit_tuple = (unit_symbols[idx], dim)
            unit_components.append(unit_tuple)
    return unit_components
