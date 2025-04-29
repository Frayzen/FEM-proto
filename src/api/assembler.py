from typing import List, Tuple
import sympy as sp
import numpy as np

from api.ast.fns import FFnType
from api.mesh.mesh import Mesh

from api.integrator import integrate

def assemble(mesh : Mesh, expr : sp.Expr, functions : List[Tuple[sp.Function, FFnType]]):
    nbnode = len(mesh.nodes)

    nbtest = len([fn for fn in functions if fn.type == FFnType.TEST])
    nbunknown = len([fn for fn in functions if fn.type == FFnType.UNKNOWN])

    K = np.zeros((nbunknown*nbnode, nbtest*nbnode), dtype=float)
    f = np.zeros(nbunknown * nbnode, dtype=float)

    for elem, conn in mesh.elems.items():
        nbnode = conn.shape[1]
        for cur in range(conn.shape[0]):
            node_ids = conn[cur]
            nodes = mesh.nodes[node_ids]
            local_K, local_F = integrate(nodes, elem, expr, functions)
            assert local_F.shape[0] == local_K.shape[0]
            assert local_K.shape[0] == nbunknown * nbnode

            # Assume DOFs are same as node IDs
            for i in range(nbnode):
                row = node_ids[i]
                for u in range(nbunknown):
                    f[row * nbunknown + u] += local_F[i]
                    for j in range(nbnode):
                        col = node_ids[j]
                        K[row * nbunknown + u, col] += local_K[i, j]
    return K, f
