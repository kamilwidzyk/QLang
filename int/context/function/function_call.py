from __future__ import annotations
from typing import Any, TYPE_CHECKING

import os
import random
import math

from ...script_errors import ScriptErrors
from ...consts import *
from ...function import Function
from ...scope import Scope
from ...QLang.QLangParser import QLangParser
from ...imports import parse_ql_text, preprocess_text
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
from ...exception.repeated_keyword_arg import RepeatedKeywordArgException
from ...exception.missing_arg import MissingArgException
from ...exception.too_much_args import TooMuchArgumentsException
from ...exception.unknown_args import UnknownArgException
from ...exception.kwargs_not_supported import KeywordArgumentsNotSupportedException
from ...exception.builtin_expects_value import BuiltinExpectsValueException
from ...exception.cant_find_variable import CantFindVariableException
from ...exception.no_parent_scope import NoParentScopeException
from ...exception.no_function_to_call import NoFunctionToCallException
from ...exception.variable_call import VariableCallException
from ...exception.incompatible_type import IncompatibleTypeException
from ...exception.place_decl_not_allowed import PlaceDeclarationNotAllowedException

class FunctionReturn(Exception):
    """Control flow exception raised when a function returns a value."""
    def __init__(self, value: Any):
        super().__init__("Function return")
        self.value = value

_current_seed = random.SystemRandom().randrange(2**64)
random.seed(_current_seed)


def _parse_seed_value(value: Any):
    if isinstance(value, Expression):
        if value.type in [TYPE_INT, TYPE_FLOAT, TYPE_NUM]:
            return int(value.value)
        if value.type == TYPE_STRING:
            parsed_value = _parse_num_cast_value(value.value)
            if parsed_value is not None:
                return int(parsed_value.value)
            return None
        return None

    if isinstance(value, (int, float)):
        return int(value)

    if isinstance(value, str):
        parsed_value = _parse_num_cast_value(value)
        if parsed_value is not None:
            return int(parsed_value.value)
        return None

    return None


def _get_seed_expression():
    return Expression(TYPE_INT, _current_seed)


def _set_seed(value: Any):
    global _current_seed
    seed_value = _parse_seed_value(value)
    if seed_value is None:
        return None
    _current_seed = seed_value
    random.seed(_current_seed)
    return Expression(TYPE_INT, _current_seed)


def _coerce_import_path(value: Any, func_name: str, pos) -> str:
    if isinstance(value, Expression):
        value = value.extract_raw_value()

    if not isinstance(value, str):
        # code BEV-4
        raise BuiltinExpectsValueException(
            pos=pos,
            func_name=func_name,
            expects="a file path string",
            code="4"
        )

    return value


def  _import_source_functions(self: Place, file_path: str, pos):
    with open(file_path, 'r', encoding='utf-8') as handle:
        source_text = handle.read()

    processed_text = preprocess_text(source_text, os.path.dirname(file_path))
    tree = parse_ql_text(processed_text)

    for top_level_item in tree.topLevelItem():
        if top_level_item.placeDecl() is not None:
            # code PDNA-1
            raise PlaceDeclarationNotAllowedException(
                pos=ScriptErrors.Position.extract(top_level_item.placeDecl()),
                file_name=file_path,
                code="1"
            )

        if top_level_item.functionDecl() is not None:
            self.handle_block(top_level_item.functionDecl(), top_level_item.functionDecl())


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
        # code TMA-3
        raise TooMuchArgumentsException(
            pos=ScriptErrors.Position.extract(block),
            func_name="parent",
            taken_args=len(args) if isinstance(args, list) else 0,
            expected_args=1,
            code="3"
        )

    arg = block.argList().arg(0)
    if arg.namedArg() is not None:
        # code KANS-3
        raise KeywordArgumentsNotSupportedException(
            pos=ScriptErrors.Position.extract(arg.namedArg()),
            func_name="parent",
            code="3"
        )
    
    arg_block = arg.expr()

    if isinstance(arg_block, VarExprCtx):
        var_name = arg_block.ID().getText()
        target_scope = _resolve_parent_scope(current_scope, 1)
        if target_scope is None:
            # code NPS-1
            raise NoParentScopeException(
                pos=ScriptErrors.Position.extract(arg_block),
                code="1"
            )
        if var_name not in target_scope.vars:
            # code CFV-4
            raise CantFindVariableException(
                pos=ScriptErrors.Position.extract(arg_block.ID()),
                var_name=var_name + " (parent scope)",
                code="4"
            )
        variable = target_scope.vars[var_name]
        if hasattr(variable, 'get'):
            return variable.get()
        if hasattr(variable, 'values'):
            return variable.values
        return variable

    if isinstance(arg_block, QLangParser.FuncCallExprContext) and arg_block.ID().getText() == "parent":
        return _resolve_parent_value(self, arg_block, [self.handle_block(arg_block, block)], _resolve_parent_scope(current_scope, 1) or current_scope)

    # code BEV-2
    raise BuiltinExpectsValueException(
        pos=ScriptErrors.Position.extract(arg_block),
        func_name="parent",
        expects="a variable name or a nested parent call",
        code="2"
    )



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
        # code RKA-1
        raise RepeatedKeywordArgException(
            pos = ScriptErrors.Position.extract(function_def.definition_block),
            func_name=func_name,
            code="1"
        )
    
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
            # code MA-1
            raise MissingArgException(
                pos = ScriptErrors.Position.extract(function_def.definition_block),
                func_name=func_name,
                missing_arg=param.name,
                code="1"
            )
    
    # Check for extra positional args if no *args
    if used_positional < len(positional_args) and varargs_param is None:
        # code TMA-1
        raise TooMuchArgumentsException(
            pos = ScriptErrors.Position.extract(function_def.definition_block),
            func_name=func_name,
            taken_args=len(positional_args) + len(keyword_args),
            expected_args=len(regular_params),
            code="1"
        )
    
    # Handle *args
    if varargs_param is not None:
        remaining_positional = positional_args[used_positional:]
        ordered_values.append(remaining_positional)
    
    # Check for unexpected keyword args
    expected_names = {param.name for param in regular_params}
    unexpected_kwargs = set(keyword_args.keys()) - expected_names
    if unexpected_kwargs:
        for unknown_arg in unexpected_kwargs:
            # code UA-1
            raise UnknownArgException(
                pos = ScriptErrors.Position.extract(function_def.definition_block),
                func_name=func_name,
                unknown_arg=unknown_arg,
                code="1"
            )
    
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
            # code KANS-1
            raise KeywordArgumentsNotSupportedException(
                pos=block_pos,
                func_name="num",
                code="1"
            )

        if len(positional_args) != 1:
            # code TMA-2
            raise TooMuchArgumentsException(
                pos=block_pos,
                func_name="num",
                taken_args=len(positional_args),
                expected_args=1,
                code="2"
            )

        cast_value = _parse_num_cast_value(positional_args[0])
        if cast_value is None:
            # code BEV-1
            raise BuiltinExpectsValueException(
                pos=block_pos,
                func_name="num",
                expects="a number or a numeric string",
                code="1"
            )

        return cast_value

    func_name = block.ID().getText()
    positional_args, keyword_args = _collect_call_args(self, block)
    
    block_pos = ScriptErrors.Position.extract(block) 
    
    if func_name == "parent":
        # parent() doesn't support keyword args
        if keyword_args:
            # code KANS-2
            raise KeywordArgumentsNotSupportedException(
                pos=block_pos,
                func_name="parent",
                code="2"
            )
        
        return _resolve_parent_value(self, block, positional_args, self.scopes.current)
    if func_name == "seed":
        if keyword_args:
            # code KANS-4
            raise KeywordArgumentsNotSupportedException(
                pos=block_pos,
                func_name="seed",
                code="4"
            )

        if len(positional_args) == 0:
            return _get_seed_expression()

        if len(positional_args) != 1:
            # code TMA-4
            raise TooMuchArgumentsException(
                pos=block_pos,
                func_name="seed",
                taken_args=len(positional_args),
                expected_args=1,
                code="4"
            )

        seed_value = _set_seed(positional_args[0])
        if seed_value is None:
            # code BEV-3
            raise BuiltinExpectsValueException(
                pos=block_pos,
                func_name="seed",
                expects="a number",
                code="3"
            )

        if getattr(self, "quantum_client", None) is not None:
            self.quantum_client.seed(seed_value.value)

        return seed_value

    if func_name == "random":
        # random() doesn't support keyword args
        if keyword_args:
            # code KANS-5
            raise KeywordArgumentsNotSupportedException(
                pos=block_pos,
                func_name="random",
                code="5"
            )

        # random() expects no positional args
        if len(positional_args) != 0:
            # code TMA-5
            raise TooMuchArgumentsException(
                pos=block_pos,
                func_name="random",
                taken_args=len(positional_args),
                expected_args=0,
                code="5"
            )

        # Return a float expression in range [0, 1)
        return Expression(TYPE_FLOAT, random.random())

    if func_name == "packet_log":
        # packet_log() doesn't support keyword args
        if keyword_args:
            # code KANS-7
            raise KeywordArgumentsNotSupportedException(
                pos=block_pos,
                func_name="packet_log",
                code="7"
            )

        if len(positional_args) != 1:
            # code TMA-7
            raise TooMuchArgumentsException(
                pos=block_pos,
                func_name="packet_log",
                taken_args=len(positional_args),
                expected_args=1,
                code="7"
            )

        enable_value = _parse_num_cast_value(positional_args[0])
        if enable_value is None:
            # code BEV-5
            raise BuiltinExpectsValueException(
                pos=block_pos,
                func_name="packet_log",
                expects="0 or 1",
                code="5"
            )

        if int(enable_value.value) not in [0, 1]:
            # code BEV-5
            raise BuiltinExpectsValueException(
                pos=block_pos,
                func_name="packet_log",
                expects="0 or 1",
                code="5"
            )

        self.packet_log_enabled = bool(int(enable_value.value))
        return Expression(TYPE_INT, int(enable_value.value))

    if func_name == "show_console":
        # show_console() doesn't support keyword args
        if keyword_args:
            # code KANS-8
            raise KeywordArgumentsNotSupportedException(
                pos=block_pos,
                func_name="show_console",
                code="8"
            )

        if len(positional_args) != 1:
            # code TMA-8
            raise TooMuchArgumentsException(
                pos=block_pos,
                func_name="show_console",
                taken_args=len(positional_args),
                expected_args=1,
                code="8"
            )

        enable_value = _parse_num_cast_value(positional_args[0])
        if enable_value is None:
            # code BEV-6
            raise BuiltinExpectsValueException(
                pos=block_pos,
                func_name="show_console",
                expects="0 or 1",
                code="6"
            )

        if int(enable_value.value) not in [0, 1]:
            # code BEV-6
            raise BuiltinExpectsValueException(
                pos=block_pos,
                func_name="show_console",
                expects="0 or 1",
                code="6"
            )

        if getattr(self, "console", None) is not None:
            if int(enable_value.value) == 1:
                self.console.show()
            else:
                self.console.hide()

        return Expression(TYPE_INT, int(enable_value.value))

    if func_name in ["cut", "round", "floor", "ceil"]:
        if keyword_args:
            # code KANS-9
            raise KeywordArgumentsNotSupportedException(
                pos=block_pos,
                func_name=func_name,
                code="9"
            )

        if len(positional_args) == 0 or len(positional_args) > 2:
            # code TMA-9
            raise TooMuchArgumentsException(
                pos=block_pos,
                func_name=func_name,
                taken_args=len(positional_args),
                expected_args=2,
                code="9"
            )

        try:
            val_raw = positional_args[0].extract_raw_value()
            if not isinstance(val_raw, (int, float)):
                raise ValueError()
            val = float(val_raw)
        except (AttributeError, ValueError, TypeError):
            # code BEV-7
            raise BuiltinExpectsValueException(
                pos=block_pos,
                func_name=func_name,
                expects="a number",
                code="7"
            )

        if len(positional_args) == 2:
            try:
                decimals_raw = positional_args[1].extract_raw_value()
                if not isinstance(decimals_raw, (int, float)):
                    raise ValueError()
                decimals = int(decimals_raw)
            except (AttributeError, ValueError, TypeError):
                # code BEV-8
                raise BuiltinExpectsValueException(
                    pos=block_pos,
                    func_name=func_name,
                    expects="a number for decimal places",
                    code="8"
                )
        else:
            decimals = 0

        factor = 10.0 ** decimals
        val_scaled = val * factor

        if func_name == "cut":
            res = math.trunc(val_scaled) / factor
        elif func_name == "round":
            if val_scaled > 0:
                res = math.floor(val_scaled + 0.5) / factor
            else:
                res = math.ceil(val_scaled - 0.5) / factor
        elif func_name == "floor":
            res = math.floor(val_scaled) / factor
        elif func_name == "ceil":
            res = math.ceil(val_scaled) / factor

        if decimals <= 0:
            return Expression(TYPE_INT, int(res))
        else:
            return Expression(TYPE_FLOAT, float(res))

    if func_name == "__ql_import_source__":
        if keyword_args:
            # code KANS-6
            raise KeywordArgumentsNotSupportedException(
                pos=block_pos,
                func_name=func_name,
                code="6"
            )

        if len(positional_args) != 1:
            # code TMA-6
            raise TooMuchArgumentsException(
                pos=block_pos,
                func_name=func_name,
                taken_args=len(positional_args),
                expected_args=1,
                code="6"
            )

        file_path = _coerce_import_path(positional_args[0], func_name, block_pos)
        _import_source_functions(self, file_path, block_pos)
        return None

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

    # Check if it's a function(variable call is possible but not legal)
    if not function_def.type == "Function":
        # code VC-1
        raise VariableCallException(
            pos=block_pos, 
            func_name=func_name,
            code="1"
        )

    ordered_args = _normalize_call_args(function_def, positional_args, keyword_args, func_name)

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
