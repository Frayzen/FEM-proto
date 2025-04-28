from sympy import *
def stringify_expr(expr : Expr):
    def aux(indent : int = 0):
        if expr.is_Atom:
            print(" " * indent + f"Atom: {expr}")
        else:
            print(" " * indent + f"Node: {expr.__class__.__name__}")
            for arg in expr.args:
                return aux(arg, indent + 2)
    return aux()
