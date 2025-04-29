import numpy as np

from api.elements.bar import Bar
from api.mesh.mesh import Mesh

def discretize_1d(min : float, max : float, amount_bar : int):
    assert(amount_bar > 0)
    assert(min < max)
    offset = (max - min) / amount_bar
    nodes = np.arange(amount_bar + 1).reshape((amount_bar + 1, 1)) * offset
    elems = np.array([
        [i, i + 1] for i in range(amount_bar)
    ])
    m : Mesh = Mesh(1)
    m.set_nodes(nodes)
    m.add_elems(Bar(), elems)
    return m


