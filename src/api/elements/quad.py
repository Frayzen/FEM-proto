from math import sqrt
from api.elements.elem_node import FElemNode, xi, eta, phi
from api.elements.element import FElement
from api.ips.ip import IP


class Bar(FElement):
    def __init__(self):
        super().__init__(
            2,
            # FElemNode
            [
                FElemNode((0, 0), (1 - xi) * (1 - eta)),
                FElemNode((1, 0), (xi) * (1 - eta)),
                FElemNode((1, 1), (xi) * (eta)),
                FElemNode((0, 1), (1 - xi) * (eta)),
            ], 
            # IPs
            [
                IP([0.5, 0.5], 1)
            ]
        )

