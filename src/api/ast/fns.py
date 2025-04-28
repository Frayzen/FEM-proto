from enum import Enum
import string
from sympy import Symbol, symbols

class FFnType(Enum):
    UNKNOWN = 0
    TEST = 1

class FFunction(Symbol):
    def __new__(cls, type: FFnType, f: Symbol, **assumptions):
        # Create a new Symbol instance with the same name and assumptions
        obj = super(FFunction, cls).__new__(cls, f.name, **f._assumptions)
        
        # Store the original symbol and type
        obj._original_symbol = f
        obj.type = type
        
        return obj
    
    def __init__(self, type: FFnType, f: Symbol, **kwargs):
        # Additional initialization if needed
        super(FFunction, self).__init__()
        # Note: The Symbol.__init__() is typically empty in SymPy,
        # but we call it for completeness
        
    def __str__(self):
        return f"FFunction(type={self.type.name}, name='{self.name}')"
    
    def __repr__(self):
        return f"FFunction(type={self.type}, {self._original_symbol!r})"
    
    # Add any custom methods you need
    def describe(self):
        return f"Function of type {self.type.name} representing {self.name}"
def create_test_fn(name : string = "v"):
    return FFunction(FFnType.TEST, symbols(name))

def create_unkown_fn(name : string = "v"):
    return FFunction(FFnType.UNKNOWN, symbols(name))
