from typing import List, Tuple
import sympy as sp
import numpy as np

from api.ast.fns import FFnType
from api.mesh.mesh import Mesh

from api.integrator import integrate

def assemble(mesh : Mesh, expr : sp.Expr, functions : List[Tuple[sp.Function, FFnType]]):
    nbnode = len(mesh.nodes)

    uks = [fn for fn in functions if fn.type == FFnType.UNKNOWN]
    tests = [fn for fn in functions if fn.type == FFnType.TEST]
    nbtest = len(tests)
    nbunknown = len(uks)

    K = np.zeros((nbunknown*nbnode, nbtest*nbnode), dtype=float)
    f = np.zeros(nbunknown * nbnode, dtype=float)

    fn_map = dict()
    for i in range(nbtest):
        fn_map[tests[i]] = i

    for i in range(nbunknown):
        fn_map[uks[i]] = i
    
    total_node = len(mesh.nodes)

    for elem, conn in mesh.elems.items():
        nbnode = conn.shape[1]
        for cur in range(conn.shape[0]):
            node_ids = conn[cur]
            nodes = mesh.nodes[node_ids]
            local_K, local_F = integrate(nodes, elem, expr, fn_map)
            # print("K\n",local_K)
            # print("F\n", local_F)

            # Assume DOFs are same as node IDs
            for u in range(nbunknown):
                col = u * total_node
                subf = local_F[u*nbnode:(u+1)*nbnode]
                for i in range(nbnode):
                    f[col + node_ids[i]] += subf[i]
                for t in range(nbtest):
                    row = t * total_node
                    subK = local_K[t*nbnode:(t+1)*nbnode, u*nbnode:(u+1)*nbnode]
                    for i in range(nbnode):
                        for j in range(nbnode):
                            K[row + node_ids[i], col + node_ids[j]] += subK[i,j]
    return K, f
