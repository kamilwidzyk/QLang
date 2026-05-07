from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...function import Function
from ...scope import Scope
from ...QLang.QLangParser import QLangParser
from ...expression import (
    Expression,
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_BOOL,
    TYPE_NUM,
    TYPE_OBS,
    TYPE_OBS_REGISTER,
)

class FunctionReturn(Exception):
    """Control flow exception raised when a function returns a value."""
    def __init__(self, value: Any):
        super().__init__("Function return")
        self.value = value

if TYPE_CHECKING:
    from place import Place


def _is_arg_type_compatible(expected_type: str, value: Any) -> bool:
    value_type = value.type if isinstance(value, Expression) else getattr(value, "type", None)

    if expected_type == "num":
        # Accept scalar numeric expressions and runtime numeric variables.
        if value_type in [TYPE_INT, TYPE_FLOAT, "Num", TYPE_NUM]:
            return True
        if isinstance(value, (int, float)):
            return True
        return False
    if expected_type == "obs":
        # Accept bool expressions, obs variables/registers and obs arrays.
        if value_type in [TYPE_BOOL, "Obs", "ObsRegister", TYPE_OBS, TYPE_OBS_REGISTER]:
            return True
        if isinstance(value, list):
            return True
        return False
    if expected_type == "state":
        return False
    return True


def _collect_call_args(self: Place, block: Any):
    arg_list = block.argList()
    if arg_list is None:
        return []

    named = arg_list.namedArgList()
    if named is not None:
        arg_names = [token.getText() for token in named.ID()]
        arg_values = [self.handle_block(expr, block) for expr in named.expr()]
        return dict(zip(arg_names, arg_values))

    standard = arg_list.standardArgList()
    if standard is None:
        return []

    return [self.handle_block(expr, block) for expr in standard.expr()]


def _resolve_parent_scope(current_scope: Scope, depth: int = 1):
    scope = current_scope
    for _ in range(depth):
        if scope.parent is None:
            return None
        scope = scope.parent
    return scope


def _resolve_parent_value(self: Place, block: Any, args: Any, current_scope: Scope):
    if not isinstance(args, list) or len(args) != 1:
        return None, "parent() expects exactly one variable name argument."

    arg_block = block.argList().standardArgList().expr(0)

    if isinstance(arg_block, QLangParser.VarExprContext):
        var_name = arg_block.ID().getText()
        target_scope = _resolve_parent_scope(current_scope, 1)
        if target_scope is None:
            return None, f"No parent scope to read '{var_name}' from."
        if var_name not in target_scope.vars:
            return None, f"I can't find '{var_name}' in parent scope."
        variable = target_scope.vars[var_name]
        if hasattr(variable, 'get'):
            return variable.get(), None
        if hasattr(variable, 'values'):
            return variable.values, None
        return variable, None

    if isinstance(arg_block, QLangParser.FuncCallExprContext) and arg_block.ID().getText() == "parent":
        inner_value, error_message = _resolve_parent_value(self, arg_block, [self.handle_block(arg_block, block)], _resolve_parent_scope(current_scope, 1) or current_scope)
        if error_message is not None:
            return None, error_message
        return inner_value, None

    return None, "parent() argument must be a variable name like parent(x)."


def _normalize_call_args(function_def: Function, call_args: Any, func_name: str):
    params = function_def.params or []

    if isinstance(call_args, dict):
        ordered_values = []
        used_names = set()

        for param in params:
            if param.name in call_args:
                ordered_values.append(call_args[param.name])
                used_names.add(param.name)
            elif param.initial_value is not None:
                ordered_values.append(param.initial_value)
            else:
                raise ValueError(f"'{func_name}' takes exactly {len(params)} arguments. {len(call_args)} given.")

        unknown_args = [name for name in call_args.keys() if name not in used_names]
        if unknown_args:
            raise ValueError(f"'{func_name}' got unexpected argument(s): {', '.join(unknown_args)}.")

        return ordered_values

    if call_args is None:
        call_args = []

    if len(call_args) > len(params):
        raise ValueError(f"'{func_name}' takes exactly {len(params)} arguments. {len(call_args)} given.")

    ordered_values = []
    for index, param in enumerate(params):
        if index < len(call_args):
            ordered_values.append(call_args[index])
        elif param.initial_value is not None:
            ordered_values.append(param.initial_value)
        else:
            raise ValueError(f"'{func_name}' takes exactly {len(params)} arguments. {len(call_args)} given.")

    return ordered_values


def _parse_num_cast_value(value: Any):
    if isinstance(value, Expression):
        if value.type in [TYPE_INT, TYPE_FLOAT]:
            return value
        if value.type == TYPE_NUM:
            return value.get()
        if value.type == TYPE_STRING:
            return _parse_num_cast_value(value.value)

    if isinstance(value, (int, float)):
        if isinstance(value, int):
            return Expression(TYPE_INT, value)
        return Expression(TYPE_FLOAT, value)

    if isinstance(value, str):
        text = value.strip()

        try:
            if text.startswith("0x") or text.startswith("0X"):
                return Expression(TYPE_INT, int(text, 16))
            if text.startswith("0b") or text.startswith("0B"):
                return Expression(TYPE_INT, int(text, 2))
            if "." in text or "e" in text or "E" in text:
                parsed_value = float(text)
                if parsed_value.is_integer():
                    return Expression(TYPE_INT, int(parsed_value))
                return Expression(TYPE_FLOAT, parsed_value)

            return Expression(TYPE_INT, int(text))
        except ValueError:
            return None

    return None

def handle_function_call(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # functionCallStmt: ID '(' argList? ')';

    if getattr(block, "NUM", None) is not None:
        args = _collect_call_args(self, block)
        block_pos = ScriptErrors.Position.extract(block)

        if isinstance(args, dict):
            args = list(args.values())

        if not isinstance(args, list) or len(args) != 1:
            self.script_errors.showError(
                pos=block_pos,
                error_type="RUNTIME ERROR",
                title="ExecutionError",
                msg="num() expects exactly one argument.",
            )
            exit()

        cast_value = _parse_num_cast_value(args[0])
        if cast_value is None:
            self.script_errors.showError(
                pos=block_pos,
                error_type="RUNTIME ERROR",
                title="Type Error",
                msg="num() expects a number or a numeric string.",
            )
            exit()

        return cast_value

    func_name = block.ID().getText()
    args = _collect_call_args(self, block)
    
    block_pos = ScriptErrors.Position.extract(block) 
    
    if func_name == "parent":
        value, error_message = _resolve_parent_value(self, block, args, self.scopes.current)
        if error_message is not None:
            self.script_errors.showError(
                pos=block_pos,
                error_type="RUNTIME ERROR",
                title="ExecutionError",
                msg=error_message,
            )
            exit()

        return value

    # Check if the function exists
    if not self.scopes.exists(func_name):
        self.script_errors.showError(
            pos=block_pos, 
            error_type="RUNTIME ERROR", 
            title="ExecutionError", 
            msg="Tried calling that function: No one picked up.")
        exit()

    # Get the function
    function_def: Function = self.scopes.get(func_name)

    # Check if it's a function(variable call is possible but not legal)
    if not function_def.type == "Function":
        self.script_errors.showError(
            pos=block_pos, 
            error_type="RUNTIME ERROR", 
            title="ExecutionError", 
            msg=f"I tried to call '{func_name}' but a variable picked up.")
        exit()

    try:
        ordered_args = _normalize_call_args(function_def, args, func_name)
    except ValueError as error:
        self.script_errors.showError(
            pos=block_pos,
            error_type="RUNTIME ERROR",
            title="ExecutionError",
            msg=str(error),
        )
        exit()

    for param, arg_value in zip(function_def.params or [], ordered_args):
        if not _is_arg_type_compatible(param.type, arg_value):
            self.script_errors.showError(
                pos=block_pos,
                error_type="RUNTIME ERROR",
                title="Type Error",
                msg=f"Argument '{param.name}' in '{func_name}' expects '{param.type}'.",
            )
            exit()



    # Create new scope for function
    new_scope = Scope(
        pos=pos,
        parent=function_def.closure_scope
    )

    # Add names functions args to it
    for param, param_value in zip(function_def.params or [], ordered_args):
        new_scope.vars[param.name] = param_value
    
    # Switch execution context
    old_scope = self.scopes.current
    self.scopes.current = new_scope

    return_val = None
    try:
        for func_block in function_def.body:
            self.handle_block(func_block, parent=function_def.body)
    except FunctionReturn as ret:
        return_val = ret.value
    finally:
        self.scopes.current = old_scope

    return return_val