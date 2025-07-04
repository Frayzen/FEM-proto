from typing import Dict, List, Type
from numpy import *
from numpy.typing import NDArray

from api.elements.element import FElement


class Mesh():

    def __init__(self, dim : int):
        self.dim = dim
        self.nodes : NDArray[floating] = None
        self.elems : Dict[Type[FElement], NDArray[integer]] = {}

    def set_nodes(self, nodes : NDArray[floating]):
        assert nodes.shape[1] == self.dim
        self.nodes = nodes

    def add_elems(self, elem_type : Type[FElement], connectivity : NDArray[integer]):
        ref_elem = elem_type()
        assert connectivity.shape[1] == len(ref_elem.ref_pts)
        assert ref_elem.dim == self.dim
        if elem_type not in self.elems:
            self.elems[elem_type] = connectivity 
        else:
            self.elems[elem_type] = hstack((self.elems[elem_type], connectivity))

    def check_valid(self):
        for elem_type, connectivity in self.elems:
            assert connectivity.shape[1] == len(elem_type.ref_pts)
            assert elem_type().dim == self.dim
        assert self.nodes.shape[1] == self.dim
