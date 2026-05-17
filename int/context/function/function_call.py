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
    TYPE_LIST,
    TYPE_STATE,
    TYPE_STRING,
    TYPE_TEXT
)
from ...variable import Variable

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
    if expected_type == "text":
        # Accept string expressions and text variables.
        if value_type in [TYPE_STRING, TYPE_TEXT]:
            return True
        if isinstance(value, str):
            return True
        return False
    if expected_type == "state":
        return value_type == TYPE_STATE
    return True


def _collect_call_args(self: Place, block: Any):
    arg_list = block.argList()
    if arg_list is None:
        return [], {}

    positional_args = []
    keyword_args = {}
    
    for arg in arg_list.arg():
        if arg.expr() is not None:
            # Positional argument
            positional_args.append(self.handle_block(arg.expr(), block))
        elif arg.namedArg() is not None:
            # Keyword argument
            named_arg = arg.namedArg()
            arg_name = named_arg.ID().getText()
            arg_value = self.handle_block(named_arg.expr(), block)
            keyword_args[arg_name] = arg_value
    
    return positional_args, keyword_args

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

    arg = block.argList().arg(0)
    if arg.namedArg() is not None:
        return None, "parent() does not accept named arguments."
    
    arg_block = arg.expr()

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


def _normalize_call_args(function_def: Function, positional_args: list, keyword_args: dict, func_name: str):
    params = function_def.params or []
    
    # Separate regular params from *args param
    regular_params = []
    varargs_param = None
    for param in params:
        if param.type == "varargs":
            varargs_param = param
        else:
            regular_params.append(param)
    
    # Check for duplicate keyword args
    if len(keyword_args) != len(set(keyword_args.keys())):
        raise ValueError(f"'{func_name}' got multiple values for keyword argument")
    
    # Build the ordered values for regular params
    ordered_values = []
    used_positional = 0
    
    for i, param in enumerate(regular_params):
        if param.name in keyword_args:
            # Keyword argument provided
            ordered_values.append(keyword_args[param.name])
        elif used_positional < len(positional_args):
            # Positional argument
            ordered_values.append(positional_args[used_positional])
            used_positional += 1
        elif param.initial_value is not None:
            # Default value
            ordered_values.append(param.initial_value)
        else:
            raise ValueError(f"'{func_name}' missing required argument: '{param.name}'")
    
    # Check for extra positional args if no *args
    if used_positional < len(positional_args) and varargs_param is None:
        raise ValueError(f"'{func_name}' takes {len(regular_params)} arguments but {len(positional_args) + len(keyword_args)} were given")
    
    # Handle *args
    if varargs_param is not None:
        remaining_positional = positional_args[used_positional:]
        ordered_values.append(remaining_positional)
    
    # Check for unexpected keyword args
    expected_names = {param.name for param in regular_params}
    unexpected_kwargs = set(keyword_args.keys()) - expected_names
    if unexpected_kwargs:
        raise ValueError(f"'{func_name}' got unexpected keyword argument(s): {', '.join(unexpected_kwargs)}")
    
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
        positional_args, keyword_args = _collect_call_args(self, block)
        block_pos = ScriptErrors.Position.extract(block)

        # num() doesn't support keyword args
        if keyword_args:
            self.script_errors.showError(
                pos=block_pos,
                error_type="RUNTIME ERROR",
                title="ExecutionError",
                msg="num() doesn't accept keyword arguments.",
            )
            exit()

        if len(positional_args) != 1:
            self.script_errors.showError(
                pos=block_pos,
                error_type="RUNTIME ERROR",
                title="ExecutionError",
                msg="num() expects exactly one argument.",
            )
            exit()

        cast_value = _parse_num_cast_value(positional_args[0])
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
    positional_args, keyword_args = _collect_call_args(self, block)
    
    block_pos = ScriptErrors.Position.extract(block) 
    
    if func_name == "parent":
        # parent() doesn't support keyword args
        if keyword_args:
            self.script_errors.showError(
                pos=block_pos,
                error_type="RUNTIME ERROR",
                title="ExecutionError",
                msg="parent() doesn't accept keyword arguments.",
            )
            exit()
        
        value, error_message = _resolve_parent_value(self, block, positional_args, self.scopes.current)
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
        ordered_args = _normalize_call_args(function_def, positional_args, keyword_args, func_name)
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

    # Add function args as variables to the scope
    param_index = 0
    for param in function_def.params or []:
        if param.type == "varargs":
            # Handle *args - store as a list directly in scope
            varargs_values = ordered_args[param_index] if param_index < len(ordered_args) else []
            # Extract values from Expression objects
            cleaned_varargs = []
            for val in varargs_values:
                if isinstance(val, Expression):
                    cleaned_varargs.append(val.value)
                else:
                    cleaned_varargs.append(val)
            var = Variable(param.name, TYPE_NUM, [len(cleaned_varargs)])
            var.data = cleaned_varargs
            new_scope.vars[param.name] = var
            param_index += 1
        else:
            # Regular parameter - create variable of the appropriate type
            param_value = ordered_args[param_index] if param_index < len(ordered_args) else param.initial_value
            param_index += 1
            
            # Convert type string to constant
            type_const = {
                "num": TYPE_NUM,
                "obs": TYPE_OBS,
                "state": TYPE_STATE,
                "text": TYPE_TEXT
            }.get(param.type, TYPE_NUM)
            
            # Handle dimensions
            dimensions = param.size if param.size else [0]
            if len(dimensions) == 1 and dimensions[0] == 0:
                dimensions = [0]
            
            var = Variable(param.name, type_const, dimensions, quantum_client=self.quantum_client)
            if param_value is not None:
                var.set(param_value)
            new_scope.vars[param.name] = var
    
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
