from typing import List
from sympy import Expr

from api.assembler import assemble
from api.ast.fns import FFunction
from api.mesh.mesh import Mesh


def create_system(mesh : Mesh, expr : Expr, functions : List[FFunction]):
    assemble(mesh, expr, functions)
    # K, f = assemble(mesh, expr, functions)
    # return K, f
