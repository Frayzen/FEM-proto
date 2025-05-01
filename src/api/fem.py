from typing import List, Tuple
from sympy import Expr, Function

from api.assembler import assemble
from api.ast.fns import FFnType
from api.mesh.mesh import Mesh


def create_system(mesh : Mesh, expr : Expr, functions : List[Tuple[Function, FFnType]]):
    atoms = expr.atoms(Function)
    assert(fn in functions for fn in atoms), "Please provide all of the function used in the expression"
    for fn in functions:
        assert fn.type is not None, "Please only use function created with create_unkown_fn or create_test_fn"
    assert(len(atoms) == len(functions)), "Please provide all of the function used in the expression"
    return assemble(mesh, expr, functions)

