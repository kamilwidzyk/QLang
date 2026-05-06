from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..function import Function
from ..scope import Scope
from ..num import NumVar

class FunctionReturn(Exception):
    """Control flow exception raised when a function returns a value."""
    def __init__(self, value: Any):
        super().__init__("Function return")
        self.value = value

if TYPE_CHECKING:
    from place import Place

def handle_function_call(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # functionCallStmt: ID '(' argList? ')';

    func_name = block.ID().getText()
    args = []
    if block.argList():
        args = self.handle_block(block.argList(), block)

    parent_pos = ScriptErrors.Position.extract(parent) if parent else pos

    # Check if the function exists
    if not self.scopes.exists(func_name):
        self.script_errors.showError(
            pos=parent_pos,
            error_type="RUNTIME ERROR",
            title="You Error",
            msg="Tried calling that function: No one picked up.")
        exit()

    # Get the function
    function_def: Function = self.scopes.get(func_name)

    # Check if it's a function (variable is possible but not legal)
    if not function_def.type == "Function":
        self.script_errors.showError(
            pos=parent_pos,
            error_type="RUNTIME ERROR",
            title="ExecutionError",
            msg=f"I tried to call '{func_name}' but a variable picked up.")
        exit()

    # Validate argument count
    param_list = function_def.params or []
    if len(param_list) != len(args):
        self.script_errors.showError(
            pos=parent_pos,
            error_type="RUNTIME ERROR",
            title="ArgumentError",
            msg=f"Function '{func_name}' expects {len(param_list)} argument(s), got {len(args)}."
        )
        exit()

    # Validate argument types and sizes
    for param, arg_value in zip(param_list, args):
        expected = param.type
        actual_type = getattr(arg_value, "type", None)

        if expected == "NUM":
            # Accept NumVar, NumArray, or a raw Python int/float
            if actual_type not in ("Num", "NumArray") and not isinstance(arg_value, (int, float)):
                self.script_errors.showError(
                    pos=parent_pos,
                    error_type="RUNTIME ERROR",
                    title="TypeError",
                    msg=f"Function '{func_name}' expects a NUM argument for '{param.name}', got '{actual_type}'."
                )
                exit()

        elif expected == "OBS":
            if actual_type not in ["Obs", "ObsRegister"]:
                self.script_errors.showError(
                    pos=parent_pos,
                    error_type="RUNTIME ERROR",
                    title="TypeError",
                    msg=f"Function '{func_name}' expects an OBS argument for '{param.name}', got '{actual_type}'."
                )
                exit()
            if param.size is None and actual_type != "Obs":
                self.script_errors.showError(
                    pos=parent_pos,
                    error_type="RUNTIME ERROR",
                    title="TypeError",
                    msg=f"Function '{func_name}' expects a single OBS for '{param.name}', got an observation register."
                )
                exit()
            if param.size is not None:
                if actual_type != "ObsRegister":
                    self.script_errors.showError(
                        pos=parent_pos,
                        error_type="RUNTIME ERROR",
                        title="TypeError",
                        msg=f"Function '{func_name}' expects an OBS register of size {param.size} for '{param.name}'."
                    )
                    exit()
                if arg_value.size() != param.size:
                    self.script_errors.showError(
                        pos=parent_pos,
                        error_type="RUNTIME ERROR",
                        title="SizeError",
                        msg=f"Function '{func_name}' expects OBS register '{param.name}' of size {param.size}, got {arg_value.size}."
                    )
                    exit()

        elif expected == "STATE":
            if actual_type not in ["State", "StateRegister"]:
                self.script_errors.showError(
                    pos=parent_pos,
                    error_type="RUNTIME ERROR",
                    title="TypeError",
                    msg=f"Function '{func_name}' expects a STATE argument for '{param.name}', got '{actual_type}'."
                )
                exit()
            if param.size is None and actual_type != "State":
                self.script_errors.showError(
                    pos=parent_pos,
                    error_type="RUNTIME ERROR",
                    title="TypeError",
                    msg=f"Function '{func_name}' expects a single STATE for '{param.name}', got a quantum register."
                )
                exit()
            if param.size is not None:
                if actual_type != "StateRegister":
                    self.script_errors.showError(
                        pos=parent_pos,
                        error_type="RUNTIME ERROR",
                        title="TypeError",
                        msg=f"Function '{func_name}' expects a STATE register of size {param.size} for '{param.name}'."
                    )
                    exit()
                if arg_value.size != param.size:
                    self.script_errors.showError(
                        pos=parent_pos,
                        error_type="RUNTIME ERROR",
                        title="SizeError",
                        msg=f"Function '{func_name}' expects STATE register '{param.name}' of size {param.size}, got {arg_value.size}."
                    )
                    exit()

    # Create new scope for function
    new_scope = Scope(
        pos=pos,
        parent=function_def.closure_scope
    )

    # Bind arguments to parameter names in the new scope.
    # For NUM params passed as raw int/float, wrap in NumVar so the body
    # can treat them uniformly as named variables.
    for param, arg_value in zip(param_list, args):
        if param.type == "NUM" and isinstance(arg_value, (int, float)):
            wrapped = NumVar(arg_value)
            wrapped.name = param.name
            new_scope.vars[param.name] = wrapped
        else:
            new_scope.vars[param.name] = arg_value

    # Switch execution context
    old_scope = self.scopes.current
    self.scopes.current = new_scope
    self.scopes.set(func_name, function_def)

    return_val = None
    # Execute function body
    try:
        for func_block in function_def.body:
            self.handle_block(func_block)
    except FunctionReturn as ret:
        return_val = ret.value

    # Recover scope
    self.scopes.current = old_scope

    # Enforce return type contract
    declared = getattr(function_def, "return_type", "void")
    if declared == "void" and return_val is not None:
        self.script_errors.showError(
            pos=parent_pos,
            error_type="RUNTIME ERROR",
            title="ReturnTypeError",
            msg=f"Function '{func_name}' is declared void but returned a value."
        )
        exit()
    if declared == "num" and return_val is not None and not isinstance(return_val, (int, float)):
        self.script_errors.showError(
            pos=parent_pos,
            error_type="RUNTIME ERROR",
            title="ReturnTypeError",
            msg=f"Function '{func_name}' is declared num but returned a non-numeric value."
        )
        exit()

    return return_val
