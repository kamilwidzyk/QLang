from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
import copy

from ...obs import Obs, ObsRegister

from ...expression import Expression, TYPE_INT, TYPE_LIST, TYPE_OBS, TYPE_NUM, TYPE_OBS_REGISTER, TYPE_STATE, TYPE_TEXT, TYPE_ANY
from ...logger import log, VARIABLE, FATAL

from ...exception.size_error import SizeErrorException
from ...exception.variable_redefinition import VariableRedefiniotionException
from ...variable import Variable


def _list_shape(values: Any) -> list | None:
    if not isinstance(values, list):
        return []

    if len(values) == 0:
        return [0]

    first_shape = _list_shape(values[0])
    if first_shape is None:
        return None

    for element in values[1:]:
        element_shape = _list_shape(element)
        if element_shape != first_shape:
            return None

    return [len(values)] + first_shape


def _normalize_list_values(values: Any) -> Any:
    if isinstance(values, list):
        return [_normalize_list_values(v) for v in values]

    if isinstance(values, Expression):
        return values

    if hasattr(values, 'get') and not isinstance(values, Expression):
        try:
            return values.get()
        except Exception:
            pass

    return values


if TYPE_CHECKING:
    from place import Place


def handle_variable_sizevar(self: Place, block: any, parent: any):
    # sizeVar: '[' (expr | '?') ']'; 
    # Only int allowed as size, or '?' for dynamic size
    if block.expr():
        expr = self.handle_block(block.expr(), block)
        if expr.type != TYPE_INT:
            raise SizeErrorException(ScriptErrors.Position.extract(block))
        
        if expr.value <= 0:
            raise SizeErrorException(ScriptErrors.Position.extract(block))

        return expr.value
    elif block.getText().find('?') != -1:
        # Dynamic size
        return '?'



def _handle_variable_subdeclaration(self: Place, block: any, parent: Any, type: str, is_const: bool = False):
    # varAssign: ID sizeVar* ('=' expr)?;

    var_name = block.ID().getText()

    if var_name in self.scopes.current.vars:
        raise VariableRedefiniotionException(ScriptErrors.Position.extract(block))

    if is_const and block.expr() is None:
        self.script_errors.showError(
            pos=ScriptErrors.Position.extract(block),
            error_type="RUNTIME ERROR",
            title="DeclarationError",
            msg=f"Const variable '{var_name}' must be initialized.",
        )
        exit()

    dimensions = []
    for size in block.sizeVar():
        dim = handle_variable_sizevar(self, size, block)
        dimensions.append(dim if dim != '?' else -100)

    # Remember if it was dynamic
    is_dynamic = -100 in [d for d in dimensions if isinstance(d, int)] or len(dimensions) == 0
    
    initial_value = None

    if block.expr():
        initial_value = self.handle_block(block.expr(), block)

    if is_const and type == TYPE_STATE:
        self.script_errors.showError(
            pos=ScriptErrors.Position.extract(block),
            error_type="RUNTIME ERROR",
            title="DeclarationError",
            msg="Const state variables are not supported.",
        )
        exit()

    if type == TYPE_OBS and len(dimensions) >= 1:
        type = TYPE_OBS_REGISTER
    
    if len(dimensions) == 0:
        dimensions = [0]


    if type == TYPE_STATE and initial_value is not None:
        self.script_errors.showError(
            pos=ScriptErrors.Position.extract(block),
            error_type="RUNTIME ERROR",
            title="Access Denied",
            msg="Quantum states cannot be assigned directly.",
        )
        exit()

    var = Variable(var_name, type, dimensions, quantum_client=self.quantum_client, is_const=is_const)
    if initial_value is not None:
        if isinstance(initial_value, list):
            initial_value = _normalize_list_values(initial_value)
            value_shape = _list_shape(initial_value)

            expected_shapes = [dimensions]
            if type == TYPE_OBS_REGISTER:
                expected_shapes.append(dimensions[:-1])

            is_valid_shape = False
            for expected in expected_shapes:
                if isinstance(value_shape, list) and value_shape == expected:
                    is_valid_shape = True
                    break
                if isinstance(value_shape, int) and len(expected) == 1 and value_shape == expected[0]:
                    is_valid_shape = True
                    break

            if value_shape is None or not is_valid_shape:
                self.script_errors.showError(
                    pos=ScriptErrors.Position.extract(block),
                    error_type="RUNTIME ERROR",
                    title="Array Shape Mismatch",
                    msg=(
                        f"Cannot initialize array '{var_name}' with shape {value_shape} "
                        f"when declared size is {dimensions}."
                    )
                )
                exit()

            initial_value = Expression(TYPE_LIST, initial_value, shape=value_shape)
        elif isinstance(initial_value, Expression) and initial_value.type == TYPE_LIST:
            if(is_dynamic):
                dimensions = initial_value.shape
                var.dimensions = dimensions
            value_shape = initial_value.shape
            initial_value = Expression(TYPE_LIST, initial_value.value, shape=value_shape)
            
            var_dims = dimensions if not is_dynamic else value_shape
            var = Variable(var_name, type, var_dims, quantum_client=self.quantum_client, is_const=is_const)
            
            if isinstance(dimensions, int):
                dimensions = [dimensions]

            expected_shapes = [dimensions]
            if type == TYPE_OBS_REGISTER:
                expected_shapes.append(dimensions[:-1])

            is_valid_shape = False
            for expected in expected_shapes:
                if isinstance(value_shape, list) and value_shape == expected:
                    is_valid_shape = True
                    break
                if isinstance(value_shape, int) and len(expected) == 1 and value_shape == expected[0]:
                    is_valid_shape = True
                    break

            if value_shape is None or not is_valid_shape:
                self.script_errors.showError(
                    pos=ScriptErrors.Position.extract(block),
                    error_type="RUNTIME ERROR",
                    title="Array Shape Mismatch",
                    msg=(
                        f"Cannot initialize array '{var_name}' with shape {initial_value.shape} "
                        f"when declared size is {dimensions}."
                    )
                )
                exit()

        #try:
        var.set(initial_value, allow_const_init=is_const)
        var.initial_value = copy.deepcopy(initial_value)
        #except (AttributeError, TypeError, ValueError):
        #    self.script_errors.showError(
        #        pos=ScriptErrors.Position.extract(block),
        #        error_type="RUNTIME ERROR",
        #        title="Type Mismatch",
        #        msg=f"The variable '{var_name}' is defined as '{type}' (numeric)."
        #    )
        #    exit()

    self.scopes.create(var_name, var)

    


def handle_variable_declaration(self: Place, block: any, parent: Any, pos: ScriptErrors.Position):
    # varDecl: varType varAssign (',' varAssign)*

    var_type = block.varType().getText()

    if var_type == "obs":
        var_type = TYPE_OBS
    elif var_type == "num":
        var_type = TYPE_NUM
    elif var_type == "text":
        var_type = TYPE_TEXT
    elif var_type == "state":
        var_type = TYPE_STATE
    elif var_type == "any":
        var_type = TYPE_ANY
    else:
        log(VARIABLE, FATAL, "Unsupported variable type: " + str(var_type))
        exit()
    
    for var_assign in block.varAssign():
        _handle_variable_subdeclaration(self, var_assign, block, var_type)


def handle_const_variable_declaration(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # constDecl: CONST varType constAssign (',' constAssign)*;
    var_type = block.varType().getText()

    if var_type == "obs":
        var_type = TYPE_OBS
    elif var_type == "num":
        var_type = TYPE_NUM
    elif var_type == "text":
        var_type = TYPE_TEXT
    elif var_type == "state":
        var_type = TYPE_STATE
    elif var_type == "any":
        var_type = TYPE_ANY
    else:
        log(VARIABLE, FATAL, "Unsupported variable type: " + str(var_type))
        exit()

    if var_type == TYPE_STATE:
        self.script_errors.showError(
            pos=pos,
            error_type="RUNTIME ERROR",
            title="DeclarationError",
            msg="Const state variables are not supported.",
        )
        exit()

    for const_assign in block.constAssign():
        _handle_variable_subdeclaration(self, const_assign, block, var_type, is_const=True)


def handle_const_existing_variable(self: Place, block: any, parent: Any, pos: ScriptErrors.Position):
    # constDecl: CONST ID;
    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        self.script_errors.showError(
            pos=ScriptErrors.Position.extract(block),
            error_type="RUNTIME ERROR",
            title="ReferenceError",
            msg=f"Cannot declare const for undefined variable '{var_name}'.",
        )
        exit()

    variable = self.scopes.get(var_name)

    if isinstance(variable, Variable) and variable.type == TYPE_STATE:
        self.script_errors.showError(
            pos=ScriptErrors.Position.extract(block),
            error_type="RUNTIME ERROR",
            title="DeclarationError",
            msg="Const state variables are not supported.",
        )
        exit()

    if isinstance(variable, Variable):
        variable.is_const = True




