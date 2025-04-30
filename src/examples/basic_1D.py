from sympy import *
import numpy as np

from api.ast.fns import FFnType, create_test_fn, create_unknown_fn
from api.fem import create_system
from api.mesh.utils import discretize_1d

# Example Poisson Equation

u = create_unknown_fn()
v = create_test_fn()

f = 1

expr = diff(u) * diff(v) - f * v

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
