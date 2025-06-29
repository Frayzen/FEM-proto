from typing import List

from numpy.typing import NDArray

from api.elements.elem_node import FElemNode
from api.ips.ip import IP

class FElement:
    def __init__(self, dim : int, ref_pts : List[FElemNode], ips : List[IP]):
        self.dim = dim
        self.ref_pts = ref_pts
        self.ips = ips
        for ip in ips:
            ip.evaluate(dim, ref_pts)

    def get_jacobian(self, ip : IP, nodes : NDArray):
        # nodes (dim * nbnode)
        # dxep (nbnode * dim)
        return ip.dxep @ nodes

