from typing import List
import numpy as np
from numpy.testing import assert_equal
from numpy.typing import NDArray
from sympy import Tuple

from api.elements.bar import Bar
from api.mesh.mesh import Mesh

def discretize_domain(min : float, max : float, amount_bar : int):
    assert(amount_bar > 0)
    assert(min < max)
    offset = (max - min) / amount_bar
    nodes = min + np.arange(amount_bar + 1).reshape((amount_bar + 1, 1)) * offset
    elems = np.array([
        [i, i + 1] for i in range(amount_bar)
    ])
    return nodes, elems

def discretize_1d(min : float, max : float, amount_bar : int):
    nodes, elems = discretize_domain(min, max, amount_bar)
    m : Mesh = Mesh(1)
    m.set_nodes(nodes)
    m.add_elems(Bar(), elems)
    return m



def discretize(min : float | List | Tuple, max : float | List | Tuple, amount_nodes : int | List | Tuple):
    assert(len(min) == len(max) == len(amount_nodes))
    dim = len(min)
    assert(dim > 0 and dim < 4)
    dim_vals = []
    nb_node = np.prod(amount_nodes)
    for i in range(dim):
        dim_vals.append(np.linspace(min[i], max[i], amount_nodes[i]))
    print(dim_vals)
    vals = np.meshgrid(*dim_vals)
    nodes = np.stack(vals, axis=-1)
    nodes = nodes.reshape(nb_node, dim)
    m : Mesh = Mesh(dim)
    m.set_nodes(nodes)
    elem_type=[Bar]
    
