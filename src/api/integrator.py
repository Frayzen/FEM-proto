from typing import Dict, List, Tuple

import numpy as np
from numpy import floating, linalg, outer
from numpy.typing import NDArray
from sympy import Expr, Function
from api.ast.fns import FFnType
from api.elements.element import FElement

def get_nbderivative(expr : Expr):
    cur = 0
    while expr.is_Derivative:
        expr = expr.args[0]
        cur += 1
    assert expr.is_Function, "Could not get the derivative of a non function"
    return expr, cur

def integrate(nodes : NDArray[floating], elem : FElement, expr : Expr, fn_map : Dict[Function, int]):
    unknowns = [ fn for fn in fn_map.keys() if fn.type == FFnType.UNKNOWN ]
    tests = [ fn for fn in fn_map.keys() if fn.type == FFnType.TEST ]
    nb_ref_pts = len(elem.ref_pts)

    nb_unknowns = len(unknowns)
    nb_dof = nb_ref_pts * nb_unknowns 

    resK = np.zeros((nb_dof, nb_ref_pts * len(tests)), dtype=float)
    resf = np.zeros(nb_dof, dtype=float)
    i = 0
    for i in range(len(elem.ips)):
        K = np.zeros((nb_dof, nb_ref_pts * len(tests)), dtype=float)
        f = np.zeros(nb_dof, dtype=float)

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
                    assert cur_unknown is None, "Please do not multiply 2 unkown functions together"
                    cur_unknown = (ip.get_shapefn(nb), fn_map[fn])
                    return 1
                else:
                    assert cur_test is None, "Please do not multiply 2 test functions together"
                    cur_test = (ip.get_shapefn(nb), fn_map[fn])
                    return 1
            else:
                evaluated_args = [eval_expr(arg) for arg in expr.args]
                return expr.func(*evaluated_args)

        def evaluate(expr : Expr, K : NDArray, f : NDArray):
            global cur_test, cur_unknown

            cur_test = None
            cur_unknown = None

            weight = eval_expr(expr) * ip.weight
            assert cur_test is not None, "Please multiply each term of the equation by a test function"

            tst, tst_id = cur_test
            fromtst = tst_id * nb_ref_pts

            if cur_unknown is None:
                f[fromtst:fromtst+nb_ref_pts] = f[fromtst:fromtst+nb_ref_pts] + weight * tst.flatten()
            else:
                uk, uk_id = cur_unknown

                toadd = weight * outer(uk, tst)
                toadd = toadd.astype(float)

                fromuk = uk_id*nb_ref_pts
                sub = K[fromuk:fromuk+nb_ref_pts, fromtst:fromtst+nb_ref_pts]
                sub += toadd
            return K, f


        if expr.is_Add:
            for e in expr.args:
                K, f = evaluate(e, K, f)
        else:
            K, f = evaluate(expr, K, f)
        detJ = linalg.det(J)
        K *= 1 / detJ 
        f *= detJ 
        resK += K
        resf += f
    return resK, resf.flatten()

