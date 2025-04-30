from typing import List, Tuple

import numpy as np
from numpy import floating, integer, linalg, outer
from numpy.typing import NDArray
from sympy import Expr, Function, det
from api.ast.fns import FFnType
from api.elements.element import FElement
from api.mesh.mesh import Mesh

def get_nbderivative(expr : Expr):
    cur = 0
    while expr.is_Derivative:
        expr = expr.args[0]
        cur += 1
    assert expr.is_Function
    return expr, cur

def integrate(nodes : NDArray[floating], elem : FElement, expr : Expr, functions : List[Tuple[Function, FFnType]]):
    unknowns = [ fn for fn in functions if fn.type == FFnType.UNKNOWN ]
    nb_ref_pts = len(elem.ref_pts)
    nb_dof = nb_ref_pts * len(unknowns)
    nb_test = nb_ref_pts * len([ fn for fn in functions if fn.type == FFnType.TEST ])
    K = np.zeros((nb_dof, nb_test), dtype=float)
    f = np.zeros(nb_dof, dtype=float)
    i = 0
    for i in range(len(elem.ips)):

        ip = elem.ips[i]
        J = elem.get_jacobian(ip, nodes)
        
        # return WEIGHT, updates cur_unkown and cur_test
        def eval_expr(expr : Expr) -> float:
            global cur_test, cur_unknown

            if expr.is_Atom:
                return expr
            if expr.is_Function or expr.is_Derivative:
                fn, nb = get_nbderivative(expr)
                if fn.type == FFnType.UNKNOWN:
                    cur_unknown = (ip.get_shapefn(nb), fn)
                    return 1
                else:
                    cur_test = (ip.get_shapefn(nb), fn)
                    return 1
            else:
                evaluated_args = [eval_expr(arg) for arg in expr.args]
                return expr.func(*evaluated_args)

        def evaluate(expr : Expr, K : NDArray, f : NDArray):
            global cur_test, cur_unknown

            cur_test = None
            cur_unknown = None

            weight = eval_expr(expr) * ip.weight
            assert cur_test is not None
            if cur_unknown is None:
                f = f + weight * cur_test[0].flatten()
            else:
                toadd = weight * outer(cur_unknown[0], cur_test[0])
                toadd = toadd.astype(float)
                id = unknowns.index(cur_unknown[1])
                sub = K[id*nb_ref_pts:(id + 1)*nb_ref_pts]
                sub += toadd
            return K, f


        if expr.is_Add:
            for e in expr.args:
                K, f = evaluate(e, K, f)
        else:
            K, f = evaluate(expr, K, f)
        detJ = linalg.det(J)
        K *= detJ 
        f *= detJ 
    return K, f.flatten()

