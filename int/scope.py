from dataclasses import dataclass
from typing import Any

from .script_errors import ScriptErrors

@dataclass
class Scope:
    def __init__(self, pos: ScriptErrors.Position, scope_type="block", parent=None):
        self.vars = {}
        self.pos = pos
        self.parent = parent
        self.type = scope_type


class ScopeManager:
    def __init__(self):
        # initialize with global scope that begins at 0, 0
        self.current = Scope(ScriptErrors.Position(0, 0))

    def push(self, pos: ScriptErrors.Position, scope_type: str):
        # go one scope down, pos = position of element that started the scope
        self.current = Scope(pos, scope_type, parent=self.current)

    def pop(self):
        # exit from scope
        if self.current.parent is not None:
            self.current = self.current.parent
        else:
            raise Exception("Cannot pop global scope")
        
    def get(self, name):
        # get var/func from current scope or higher
        scope = self.current
        while scope:
            print(scope.vars)
            if name in scope.vars:
                return scope.vars[name]
            scope = scope.parent
        raise Exception(f"Variable {name} not defined")
    
    def set(self, name, value):
        # assign a variable:
        # if found: assign value
        # if not found: create variable at current scope and assign (this will propably change)
        # there will be most likely a create method added to prevent assigment of non-existing variables
        scope = self.current
        while scope:
            if name in scope.vars:
                scope.vars[name] = value
                return
            scope = scope.parent
        self.current.vars[name] = value

    def exists(self, name) -> bool:
        # check if variable with a given name exists at the current scope
        scope = self.current
        while scope:
            if name in scope.vars:
                return True
            scope = scope.parent
        return False

    def create(self, name: str, value: Any):
        # create variable with given name at current scope
        # value will be a class instance which will specify type and size
        self.current.vars[name] = value

    def assign(self, name: str, value: Any):
        # assign an existing variable
        # search all the scopes 
        scope = self.current
        while scope:
            if name in scope.vars:
                scope.vars[name] = value
                return
            scope = scope.parent