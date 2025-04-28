from typing import List, Tuple

import numpy as np

from api.elements.elem_node import FElemNode
from api.ips.ip import IP

class FElement:
    def __init__(self, dim : int, ref_pts : List[FElemNode], ips : List[IP]):
        self.dim = dim
        self.ref_pts = ref_pts
        self.ips = ips
        for ip in ips:
            ip.evaluate(dim, ref_pts)
        local = np.outer(ips[0].evaluated, ips[1].evaluated) * ips[0].weight
        local += np.outer(ips[1].evaluated, ips[0].evaluated) * ips[1].weight
        print(local)

