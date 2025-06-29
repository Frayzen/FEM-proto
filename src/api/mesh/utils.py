from typing import List
import numpy as np
from numpy.testing import assert_equal
from numpy.typing import NDArray
from sympy import Tuple

from api.elements.bar import Bar
from api.mesh.mesh import Mesh

def discretize_1d(min : float, max : float, amount_bar : int):
    assert(amount_bar > 0)
    assert(min < max)
    offset = (max - min) / amount_bar
    nodes = min + np.arange(amount_bar + 1).reshape((amount_bar + 1, 1)) * offset
    elems = np.array([
        [i, i + 1] for i in range(amount_bar)
    ])
    m : Mesh = Mesh(1)
    m.set_nodes(nodes)
    m.add_elems(Bar(), elems)
    return m



def discretize(min : float | List | Tuple, max : float | List | Tuple, amount_bar : int | List | Tuple):
    amount_bar = np.array(amount_bar, dtype=int)
    min = np.array(min, dtype=float)
    max = np.array(max, dtype=float)
    assert(len(min) == len(max) == len(amount_bar))
    np.testing.assert_equal(min < max, True)
    np.testing.assert_equal(amount_bar != 0)
    offset = (max - min) / amount_bar
    nodes = np.arange((amount_bar + 1).prod()).reshape(amount_bar + 1) * offset
    elems = np.array([
        [i, i + 1] for i in range(amount_bar)
    ])
    m : Mesh = Mesh(1)
    m.set_nodes(nodes)
    m.add_elems(Bar(), elems)
    return m


