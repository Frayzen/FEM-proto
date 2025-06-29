from sympy import *
import numpy as np

from api.ast.fns import FFnType, create_test_fn, create_unknown_fn
from api.fem import create_system
from api.mesh.utils import discretize_1d

# Example Poisson Equation
def test_poisson():
    u = create_unknown_fn()
    v = create_test_fn()

    f = 2

    expr = diff(u) * diff(v) - f * v

    # u''(x) = 2
    # u(0) = u(8) = 0
    # x*(x-8)

    mesh = discretize_1d(0, 8, 8)

    K, f = create_system(mesh, expr, [u, v])

    # Set DOF 0 and DOF -1 to 0
    dofs_to_constrain = [0, -1]
    for dof in dofs_to_constrain:
        # Set the row and column to identity
        K[dof, :] = 0
        K[:, dof] = 0
        K[dof, dof] = 1
        
        # Set the corresponding force to 0
        f[dof] = 0

    u = np.linalg.solve(K, f)

    print("RES\n",u)
    np.testing.assert_almost_equal(u, [0., -7., -12., -15., -16., -15., -12., -7., 0.])

# Example 2 Poisson Equation
def test_2unknowns():
    u1 = create_unknown_fn("u1")
    v1 = create_test_fn("v1")
    u2 = create_unknown_fn("u2")
    v2 = create_test_fn("v2")

    f = 1

    expr = diff(u1) * diff(v1) + diff(u2) * diff(v2) + diff(v1) * diff(u2) - diff(u1) * diff(v2) - f * v2

    nbnode = 8
    mesh = discretize_1d(0, nbnode, nbnode)

    K, f = create_system(mesh, expr, [u1, v1, u2, v2])

    # Set DOF 0 and DOF -1 to 0
    dofs_to_constrain = [0, -1]
    for dof in dofs_to_constrain:
        # Set the row and column to identity
        K[dof, :] = 0
        K[:, dof] = 0
        K[dof, dof] = 1
        
        # Set the corresponding force to 0
        f[dof] = 0

    u= np.linalg.solve(K, f)
    print("RES\n",u)

test_poisson()
# test_2unknowns()
