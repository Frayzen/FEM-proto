from typing import List
from sympy import *

from api.ast.fns import FFunction
from api.mesh.mesh import Mesh

def assemble(mesh : Mesh, expr : Expr, functions : List[FFunction]):
    for elem, conn in mesh.elems.items():
        for node_ids in conn:
            nodes = mesh.nodes[node_ids]
            # print(nodes)
         
