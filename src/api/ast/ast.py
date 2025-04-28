from sympy import *

from api.ast.utils import stringify

class FAst:
    def __init__(self, expr : Expr) -> None:
        self.expr = expr

    def __str__(self):
        return stringify(self.expr)
