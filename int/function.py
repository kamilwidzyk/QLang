from typing import List
from .script_errors import ScriptErrors

class Function:
    def __init__(self, name: str, params: List[FunctionParam], body, 
                 closure_scope, pos: ScriptErrors.Position):
        self.name = name
        self.params = params
        self.body = body
        self.closure_scope = closure_scope
        self.pos = pos
        self.type = "Function"

class FunctionParam:
    def __init__(self, name: str, type: str, size: int):
        self.name = name # param name
        self.type = type # param type 'state' or 'obs'
        self.size = size # param size or None if not specified