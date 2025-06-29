from typing import List
import numpy as np
from numpy.testing import assert_equal
from numpy.typing import NDArray
from sympy import Tuple

from api.elements.bar import Bar
from api.elements.quad import Quad
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
    m.add_elems(Bar, elems)
    return m


def create_connectivity(amount_nodes: List[int], dim: int) -> np.ndarray:
    """
    Generates element connectivity for 1D/2D/3D structured grids.
    """
    if dim == 1:
        # 1D elements (bars)
        n_elements = amount_nodes[0] - 1
        return np.array([[i, i+1] for i in range(n_elements)])
    elif dim == 2:
        # 2D elements (quads)
        nx, ny = amount_nodes
        quads = []
        for j in range(ny - 1):
            for i in range(nx - 1):
                n0 = i + j * nx
                quads.append([n0, n0 + 1, n0 + nx + 1, n0 + nx])
        return np.array(quads)
    elif dim == 3:
        # 3D elements (hexahedrons)
        nx, ny, nz = amount_nodes
        hexes = []
        for k in range(nz - 1):
            for j in range(ny - 1):
                for i in range(nx - 1):
                    n0 = i + j * nx + k * nx * ny
                    hexes.append([
                        n0, n0 + 1, n0 + nx + 1, n0 + nx,
                        n0 + nx * ny, n0 + 1 + nx * ny,
                        n0 + nx + 1 + nx * ny, n0 + nx + nx * ny
                    ])
        return np.array(hexes)



def discretize(min : float | List | Tuple, max : float | List | Tuple, amount_nodes : int | List | Tuple) -> Mesh:
    """
    Discretizes a 1D/2D/3D domain into nodes and elements.
    
    Args:
        min_coord: Minimum coordinates (float for 1D, list/tuple for 2D/3D).
        max_coord: Maximum coordinates (float for 1D, list/tuple for 2D/3D).
        amount_nodes: Number of nodes per dimension (int for 1D, list/tuple for 2D/3D).
    
    Returns:
        Mesh object with nodes and connectivity.
    """
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
    elem_type = [None, Bar, Quad][dim]
    # create elems, the connectivtiy matrix of size (2 ** dim) * nbelem
    elems = create_connectivity(amount_nodes, dim)
    m.add_elems(elem_type, elems)
    return m
    
