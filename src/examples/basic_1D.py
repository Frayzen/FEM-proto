from sympy import *

from api.ast.fns import create_test_fn, create_unkown_fn
from api.fem import create_system
from api.mesh.utils import discretize_1d

# Example Poisson Equation

u = create_unkown_fn()
v = create_test_fn()

f = 2

ast = diff(u) * diff(v) - f * v

mesh = discretize_1d(0, 1, 8)

create_system(mesh, ast, [u, v])
# K, f = create_system(mesh, ast, [u, v])
