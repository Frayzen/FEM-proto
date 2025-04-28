from typing import Tuple
from sympy import Expr, symbols

xi, eta, phi = symbols("xi eta phi")

xi_eta_phi = (xi, eta, phi)

class FElemNode:
    def __init__(self, coord : Tuple[float], shape_fn : Expr):
        self.coord = coord
        self.shape_fn = shape_fn
