from typing import List, Tuple

from api.elements.elem_node import FElemNode, xi_eta_phi
import numpy as np

class IP:
    def __init__(self, pos : List[float], weight : float):
        self.pos = pos
        self.weight = weight
        self.vals = None
        self.evaluated = None

    def evaluate(self, dim : int, ref_pts : List[FElemNode]):
        vals = [p.shape_fn for p in ref_pts ]
        for d in range(dim):
            vals = [v.subs(xi_eta_phi[d], self.pos[d]) for v in vals]
        self.evaluated = np.array(vals)
