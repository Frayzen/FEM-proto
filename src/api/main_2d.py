from api.ast.fns import create_test_fn, create_unknown_fn
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

from api.elements.quad import Quad
from api.fem import create_system
from api.mesh.utils import discretize


u = create_unknown_fn()
v = create_test_fn()

f = 2

expr = diff(u) * diff(v) - f * v

# u''(x) = 2
# u(0) = u(8) = 0
# x*(x-8)

nb = (20, 20)
minval = (0, 0)
maxval = (8, 8)
mesh = discretize(minval, maxval, nb)

# K, f = create_system(mesh, expr, [u, v])

# # Set DOF 0 and DOF -1 to 0
# dofs_to_constrain = [0, -1]
# constrain_vals = [minval * (minval - 8), maxval * (maxval - 8)]
# for i in range(len(dofs_to_constrain)):
#     dof = dofs_to_constrain[i]
#     # Set the row and column to identity
#     K[dof, :] = 0
#     K[dof, dof] = 1
#     # Set the corresponding force
#     f[dof] = constrain_vals[i]
# # print(K)
# y = np.linalg.solve(K, f)

# print("RES\n",y)
# # np.testing.assert_almost_equal(y, [0., -7., -12., -15., -16., -15., -12., -7., 0.])
# x=mesh.nodes.flatten()
# print(x)

# # 1. Plot the numerical solution (piecewise linear between nodes)
# plt.plot(x, y, 'b-o', label='Numerical solution (FEM)')

# # 2. Plot the exact solution u(x) = x*(x-8) as a continuous curve
# x_fine = np.linspace(minval, maxval, 100)  # Fine grid for smooth exact solution plot
# exact_solution = x_fine * (x_fine - 8)
# plt.plot(x_fine, exact_solution, 'r-', label='Exact solution (x(x-8))')

# # 3. Add plot labels and legend
# plt.xlabel('x')
# plt.ylabel('u(x)')
# plt.title('Comparison of FEM Solution and Exact Solution')
# plt.legend()
# plt.grid(True)

# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

def plot_quad_mesh_3d(nodes: np.ndarray, elems: np.ndarray, z_values: np.ndarray = None):
    """
    Plots a quadrilateral mesh in 3D given nodes and element connectivity.
    
    Args:
        nodes: Array of shape (N, 2) or (N, 3) containing node coordinates.
        elems: Array of shape (M, 4) defining quad connectivity (4 node indices per element).
        z_values: Optional array of shape (N,) containing z-coordinates for each node.
                 If not provided and nodes is (N, 2), z-coordinates will be set to zero.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Prepare 3D coordinates
    if nodes.shape[1] == 2:
        if z_values is None:
            z_values = np.zeros(nodes.shape[0])
        nodes_3d = np.column_stack([nodes, z_values])
    else:
        nodes_3d = nodes
    
    # Plot nodes (optional)
    ax.scatter(nodes_3d[:, 0], nodes_3d[:, 1], nodes_3d[:, 2], 
               color='red', s=10, label='Nodes')
    
    # Plot edges of each quad
    for elem in elems:
        # Close the loop by repeating the first node
        quad_nodes = nodes_3d[elem]
        quad_nodes_closed = np.vstack([quad_nodes, quad_nodes[0]])
        
        # Draw the quad edges
        ax.plot(quad_nodes_closed[:, 0], quad_nodes_closed[:, 1], quad_nodes_closed[:, 2], 
                'b-', lw=1)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Quadrilateral Mesh')
    ax.legend()
    plt.tight_layout()
    plt.show()

plot_quad_mesh_3d(mesh.nodes, mesh.elems[Quad])
