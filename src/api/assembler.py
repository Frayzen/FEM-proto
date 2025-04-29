from typing import List, Tuple
import sympy as sp

from api.ast.fns import FFnType
from api.mesh.mesh import Mesh

from api.integrator import integrate

def assemble(mesh : Mesh, expr : sp.Expr, functions : List[Tuple[sp.Function, FFnType]]):
    for elem, conn in mesh.elems.items():
        for i in range(conn.shape[0]):
            nodes = mesh.nodes[conn[i]]
            local_K, local_F = integrate(nodes, elem, expr, functions)
            print("K IS \n", local_K)
            print("F IS \n", local_F)
         
