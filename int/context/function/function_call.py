from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from place import Place

from ...script_errors import ScriptErrors
from ...consts import *
from ...function import Function
from ...scope import Scope
from ...expression import (
    Expression,
    TYPE_NUM,
    TYPE_OBS,
    TYPE_STATE,
    TYPE_TEXT,
    TYPE_ANY
)
from ...variable import Variable
from ...exception.no_function_to_call import NoFunctionToCallException
from ...exception.variable_call import VariableCallException
from ...exception.incompatible_type import IncompatibleTypeException

from .common import (
    _collect_call_args,
    _normalize_call_args,
    _is_arg_type_compatible,
    FunctionReturn
)

from .builtin.num import builtin_num
from .builtin.parent import builtin_parent
from .builtin.seed import builtin_seed
from .builtin.random import builtin_random
from .builtin.packet_log import builtin_packet_log
from .builtin.show_console import builtin_show_console
from .builtin.cut_round_floor_ceil import builtin_cut_round_floor_ceil
from .builtin.sleep import builtin_sleep
from .builtin.import_source import builtin_import_source


def handle_function_call(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles function calls, first tries to match to built-in functions, then looks for user-defined ones.
    Built-in function calls are routed to handlers in 'builtin' subdirectory.
    ||| functionCallStmt: ID '(' argList? ')'; 
    """
    if getattr(block, "NUM", None) is not None:
        return builtin_num(self, block) 

    func_name = block.ID().getText()
    
    # First check for built-in functions
    if func_name == "parent":
        return builtin_parent(self, block)
    if func_name == "seed":
        return builtin_seed(self, block)
    if func_name == "random":
        return builtin_random(self, block)
    if func_name == "packet_log":
        return builtin_packet_log(self, block)
    if func_name == "show_console":
        return builtin_show_console(self, block)
    if func_name in ["cut", "round", "floor", "ceil"]:
        return builtin_cut_round_floor_ceil(self, block, func_name)
    if func_name == "sleep": # chyba do wywalenia?
        return builtin_sleep(self, block)
    if func_name == "__ql_import_source__":
        return builtin_import_source(self, block, func_name)

    # Extract position in code and arguments
    block_pos = ScriptErrors.Position.extract(block) 
    positional_args, keyword_args = _collect_call_args(self, block)

    # Check if the function exists
    if not self.scopes.exists(func_name):
        # code NFTC-1
        raise NoFunctionToCallException(
            pos=block_pos, 
            func_name=func_name,
            code="1"
        )

    # Get the function
    function_def: Function = self.scopes.get(func_name)

    if hasattr(function_def, "extract_raw_value"):
        function_def = function_def.extract_raw_value()

    # Check if it's a function(variable call is possible but not legal)
    if not hasattr(function_def, "type") or not function_def.type == "Function":
        # code VC-1
        raise VariableCallException(
            pos=block_pos, 
            func_name=func_name,
            code="1"
        )

    ordered_args = _normalize_call_args(function_def, positional_args, keyword_args, func_name)

    # Check if argument types are compatible with parameter types
    for param, arg_value in zip(function_def.params or [], ordered_args):
        if not _is_arg_type_compatible(param.type, arg_value):
            # code IT-1
            raise IncompatibleTypeException(
                pos=block_pos,
                func_name=func_name,
                param_name=param.name,
                param_type=param.type,
                code="1"
            )

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
                "text": TYPE_TEXT,
                "any": TYPE_ANY
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
