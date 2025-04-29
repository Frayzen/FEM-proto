from typing import List, Tuple

from numpy.typing import NDArray
from sympy import Expr

from api.elements.elem_node import FElemNode, xi_eta_phi, xi, eta, phi
import numpy as np

class IP:
    def __init__(self, pos : List[float], weight : float):
        self.pos = np.array(pos) # coordinates of the current IP
        self.weight = weight

        # Will be set during evaluate
        self.vals = None
        self.evaluated = None

    def evaluate(self, dim : int, ref_pts : List[FElemNode]):
        nbrefpts = len(ref_pts)

        def eval(v : Expr):
            for d in range(dim):
                v = v.subs(xi_eta_phi[d], self.pos[d])
            return v

        vals = [p.shape_fn for p in ref_pts ]
        vals = np.array(list(map(eval, vals))).reshape((nbrefpts, 1))
        self.xep = np.array(vals, dtype=float)

        vals = np.array([p.shape_fn.diff(xi_eta_phi[d]) for d in range(dim) for p in ref_pts])
        vals = np.array(list(map(eval, vals))).reshape((dim, nbrefpts))
        self.dxep = np.array(vals, dtype=float)

    def get_shapefn(self, nb : int):
        assert(nb <= 1)
        if nb == 0:
            return self.xep
        return self.dxep
