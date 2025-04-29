from sympy import *

from api.ast.fns import FFnType, create_test_fn, create_unknown_fn
from api.fem import create_system
from api.mesh.utils import discretize_1d

# Example Poisson Equation

u = create_unknown_fn()
v = create_test_fn()

f = 2

expr = diff(u) * diff(v) - f * v

mesh = discretize_1d(0, 1, 2)

create_system(mesh, expr, [u, v])
# K, f = create_system(mesh, ast, [u, v])
