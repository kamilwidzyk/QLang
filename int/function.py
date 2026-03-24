from __future__ import annotations
from typing import List
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

class FunctionParam:
    """
    Represents one function parameter
    """
    def __init__(self, name: str, type: str, size: int):
        self.name = name # param name
        self.type = type # param type 'state' or 'obs'
        self.size = size # param size or None if not specified