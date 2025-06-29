from api.ast.fns import create_test_fn, create_unknown_fn
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

from api.fem import create_system


u = create_unknown_fn()
v = create_test_fn()

f = 2

expr = diff(u) * diff(v) - f * v

# u''(x) = 2
# u(0) = u(8) = 0
# x*(x-8)

mesh = discretize_2d(0, 8, 8)

K, f = create_system(mesh, expr, [u, v])
print(K)

# Set DOF 0 and DOF -1 to 0
dofs_to_constrain = [0, -1]
for dof in dofs_to_constrain:
    # Set the row and column to identity
    K[dof, :] = 0
    K[:, dof] = 0
    K[dof, dof] = 1
    
    # Set the corresponding force to 0
    f[dof] = 0

y = np.linalg.solve(K, f)

print("RES\n",u)
np.testing.assert_almost_equal(y, [0., -7., -12., -15., -16., -15., -12., -7., 0.])
x=mesh.nodes.flatten()

# 1. Plot the numerical solution (piecewise linear between nodes)
plt.plot(x, y, 'b-o', label='Numerical solution (FEM)')

# 2. Plot the exact solution u(x) = x*(x-8) as a continuous curve
x_fine = np.linspace(0, 8, 100)  # Fine grid for smooth exact solution plot
exact_solution = x_fine * (x_fine - 8)
plt.plot(x_fine, exact_solution, 'r-', label='Exact solution (x(x-8))')

# 3. Add plot labels and legend
plt.xlabel('x')
plt.ylabel('u(x)')
plt.title('Comparison of FEM Solution and Exact Solution')
plt.legend()
plt.grid(True)

plt.show()
