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
                    FElemNode((0), xi),
                    FElemNode((1), 1 - xi),
                ], 
                # IPs
                [
                    IP([0.5 + 1/(2 * sqrt(3))], 1/2),
                    IP([0.5 - 1/(2 * sqrt(3))], 1/2),
                ]
                )

