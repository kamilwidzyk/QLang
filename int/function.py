from __future__ import annotations
from typing import List
from .script_errors import ScriptErrors

class Function:
    """
    Represents a defined function
    """
    def __init__(self, name: str, params: List[FunctionParam], body,
                 closure_scope, pos: ScriptErrors.Position, return_type: str = "void"):
        self.name = name                    # function name
        self.params = params                # list of function params
        self.body = body                    # code inside the function
        self.closure_scope = closure_scope  # scope where the function was declared
        self.pos = pos                      # position in the code
        self.return_type = return_type      # declared return type: 'void', 'num', 'state', 'obs'
        self.type = "Function"

class FunctionParam:
    """
    Represents one function parameter
    """
    def __init__(self, name: str, type: str, size: int):
        self.name = name # param name
        self.type = type # param type: 'STATE', 'OBS', or 'NUM'
        self.size = size # param size or None if not specified