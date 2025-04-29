from enum import Enum
import string
from sympy import Function, symbols

class FFnType(Enum):
    UNKNOWN = 0
    TEST = 1

x = symbols('x')

def create_test_fn(name : string = "v"):
    fn = Function(name)(x)
    fn.type = FFnType.TEST
    return fn

def create_unknown_fn(name : string = "u"):
    fn = Function(name)(x)
    fn.type = FFnType.UNKNOWN
    return fn
