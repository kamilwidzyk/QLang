from dataclasses import dataclass
from typing import Any

from .script_errors import ScriptErrors

@dataclass
class Scope:
    """
    Represents one level of scope
    """
    def __init__(self, pos: ScriptErrors.Position, scope_type="block", parent=None):
        self.vars = {} # dict with name -> variable
        self.pos = pos # where is was added
        self.parent = parent # scope one level higher
        self.type = scope_type # type of scope (for, if, ...)


class ScopeManager:
    def __init__(self):
        """
        Initializes a global scope at default position (0, 0)
        """
        self.current = Scope(ScriptErrors.Position(0, 0))

    def push(self, pos: ScriptErrors.Position, scope_type: str):
        """
        Goes one scope deeper

        Parameters:
            pos: Position of the block that created this scope
            scope_type: what block of code caused this scope to be created
        """
        self.current = Scope(pos, scope_type, parent=self.current)

    def pop(self):
        """
        Exits from scope
        """
        if self.current.parent is not None:
            self.current = self.current.parent
        else:
            raise Exception("Cannot pop global scope")
        
    def get(self, name: str):
        """
        Return variable with given name
        If the variable is not found, this will result in an Exception. 
        Make sure to check first if the variable exists

        Parameters:
            name(str): Variable name
        Returns:
            The found variable, can depends on variable
        """
        scope = self.current
        while scope:
            print(scope.vars)
            if name in scope.vars:
                return scope.vars[name]
            scope = scope.parent
        raise Exception(f"Variable {name} not defined")
    
    def set(self, name: str, value):
        """
        Assign or create a variable at current scope

        Parameters:
            name(str): Variable name
            value: Variable content, type depends
        """
        scope = self.current
        while scope:
            if name in scope.vars:
                scope.vars[name] = value
                return
            scope = scope.parent
        self.current.vars[name] = value

    def exists(self, name: str) -> bool:
        """
        Checks if a variable exists

        Parameters:
            name(str): Variable name

        Returns:
            True: variable exists
            False: variable does not exits
        """
        scope = self.current
        while scope:
            if name in scope.vars:
                return True
            scope = scope.parent
        return False

    def create(self, name: str, value: Any):
        """
        Creates a variable at current scope and assign it

        Parameters:
            name(str): Variable name
            value: variable content, type depends
        """
        self.current.vars[name] = value

    def assign(self, name: str, value: Any):
        """
        Assign an already existing variable

        Parameters:
            name(str): Variable name
            value: variable content, type depends
        """
        scope = self.current
        while scope:
            if name in scope.vars:
                scope.vars[name] = value
                return
            scope = scope.parent