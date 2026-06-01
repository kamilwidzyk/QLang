from __future__ import annotations
from typing import Any, List

from int.expression import TYPE_BOOL, Expression
from .script_errors import ScriptErrors

class Function:
    """
    Represents a defined function
    """
    def __init__(self, name: str, params: List[FunctionParam], body, 
                 closure_scope, pos: ScriptErrors.Position):
        self.name = name                    # function name
        self.params = params                # list of function params
        self.body = body                    # code inside the function
        self.closure_scope = closure_scope  # scope where the function was declared
        self.pos = pos                      # position in the code
        self.type = "Function"    

    def __deepcopy__(self, memo):
        return self

    def __len__(self): # length of function is the number of parameters it takes
        return len(self.params)   

    def __lt__(self, other):
        if not isinstance(other, Function):
            raise TypeError("Cannot compare Function with " + str(type(other).__name__))
        return Expression(TYPE_BOOL, len(self) < len(other))
    
    def __le__(self, other):
        if not isinstance(other, Function):
            raise TypeError("Cannot compare Function with " + str(type(other).__name__))
        return Expression(TYPE_BOOL, len(self) <= len(other))
    
    def __gt__(self, other):
        if not isinstance(other, Function):
            raise TypeError("Cannot compare Function with " + str(type(other).__name__))
        return Expression(TYPE_BOOL, len(self) > len(other))
    
    def __ge__(self, other):
        if not isinstance(other, Function):
            raise TypeError("Cannot compare Function with " + str(type(other).__name__))
        return Expression(TYPE_BOOL, len(self) >= len(other))
    
    def __eq__(self, other):
        if not isinstance(other, Function):
            raise TypeError("Cannot compare Function with " + str(type(other).__name__))
        return Expression(TYPE_BOOL, len(self) == len(other))
    
    def __ne__(self, other):
        if not isinstance(other, Function):
            raise TypeError("Cannot compare Function with " + str(type(other).__name__))
        return Expression(TYPE_BOOL, len(self) != len(other))

class FunctionParam:
    """
    Represents one function parameter
    """
    def __init__(self, name: str, type: str, size: list[int], initial: Any):
        self.name = name # param name
        self.type = type # param type 'state' or 'obs' or 'num'
        self.size = size # param size or None if not specified
        self.initial_value = initial # default value