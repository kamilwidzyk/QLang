from __future__ import annotations
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from place import Place

import os
import random
import math
import time

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
    TYPE_LIST,
    TYPE_STATE,
    TYPE_STRING,
    TYPE_TEXT,
    TYPE_ANY
)
from ...exception.repeated_keyword_arg import RepeatedKeywordArgException
from ...exception.missing_arg import MissingArgException
from ...exception.too_much_args import TooMuchArgumentsException
from ...exception.unknown_args import UnknownArgException
from ...exception.kwargs_not_supported import KeywordArgumentsNotSupportedException
from ...exception.builtin_expects_value import BuiltinExpectsValueException
from ...exception.cant_find_variable import CantFindVariableException
from ...exception.no_parent_scope import NoParentScopeException
from ...exception.place_decl_not_allowed import PlaceDeclarationNotAllowedException
from ...exception.file_not_found import FileNotFoundException

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
    try:
        with open(file_path, 'r', encoding='utf-8') as handle:
            source_text = handle.read()
    except FileNotFoundError:
        # code FNF-1
        raise FileNotFoundException(
            pos=pos,
            file_path=file_path,
            code="1"
        )

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
        if value_type in [TYPE_BOOL, "Obs", "ObsRegister", TYPE_OBS]:
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
    if expected_type == "any":
        return True
    return True


def _collect_call_args(self: Place, block: Any, func_name: str):
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
            if arg_name in keyword_args:
                # code RKA-1
                raise RepeatedKeywordArgException(
                    pos=ScriptErrors.Position.extract(named_arg),
                    func_name=func_name, code="1"
                )
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



def _normalize_call_args(function_def: Function, positional_args: list, keyword_args: dict, func_name: str, block: Any):
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
            pos = ScriptErrors.Position.extract(block),
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
                pos = ScriptErrors.Position.extract(block),
                func_name=func_name,
                missing_arg=param.name,
                code="1"
            )
    
    # Check for extra positional args if no *args
    if used_positional < len(positional_args) and varargs_param is None:
        # code TMA-1
        raise TooMuchArgumentsException(
            pos = ScriptErrors.Position.extract(block),
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
                pos = ScriptErrors.Position.extract(block),
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