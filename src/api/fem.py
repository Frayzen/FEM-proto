from typing import List, Tuple
from sympy import Expr, Function

from api.assembler import assemble
from api.ast.fns import FFnType
from api.mesh.mesh import Mesh


def create_system(mesh : Mesh, expr : Expr, functions : List[Tuple[Function, FFnType]]):
    atoms = expr.atoms(Function)
    assert(fn in functions for fn in atoms)
    assert(len(atoms) == len(functions))
    return assemble(mesh, expr, functions)

