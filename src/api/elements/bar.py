from math import sqrt
from api.elements.elem_node import FElemNode, xi, eta, phi
from api.elements.element import FElement
from api.ips.ip import IP


class Bar(FElement):
    def __init__(self):
        super().__init__(
            1,
            # FElemNode
            [
                FElemNode((0), 1 - xi),
                FElemNode((1), xi),
            ], 
            # IPs
            [
                IP([0.5], 1),
            ]
        )

