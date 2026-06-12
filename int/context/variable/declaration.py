from typing import Any, TYPE_CHECKING

from int.exception.direct_quantum_access import DirectQuantumAccessException

from ...script_errors import ScriptErrors
from ...consts import *
import copy

from ...expression import Expression, TYPE_INT, TYPE_LIST, TYPE_OBS, TYPE_NUM, TYPE_STATE, TYPE_TEXT, TYPE_ANY
from ...logger import log, VARIABLE, FATAL
from ...operations.operators import do_operation_int_to_bits

from ...exception.size_error import SizeErrorException
from ...exception.variable_redefinition import VariableRedefiniotionException
from ...exception.cant_find_variable import CantFindVariableException
from ...exception.operation_not_supported import OperationNotSupportedException
from ...exception.shape_mismatch import ShapeMismatchException
from ...variable import Variable

if TYPE_CHECKING:
    from place import Place

def _list_shape(values: Any) -> list | None:
    """
    Returns list of shapes of given list
    Returns [] if not list
    Returns None if not able to determine
    """
    if not isinstance(values, list):
        return []

    if len(values) == 0:
        return [0]

    next_shape = _list_shape(values[0])
    if next_shape is None:
        return None

    for element in values[1:]:
        element_shape = _list_shape(element)
        if element_shape != next_shape:
            return None

    return [len(values)] + next_shape


def _normalize_list_values(values: Any) -> Any:
    """
    Unwraps unnecessary Expression nesting in list
    """
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


def handle_variable_sizevar(self: Place, block: any, parent: any):
    """
    Handles size declaration
    When size is a number -> returns the number
    When size is '?' -> returns '?', which is later treated as dynamic size
    """
    if block.expr():
        expr = self.handle_block(block.expr(), block)
        if expr.type != TYPE_INT:
            # code SE-1
            raise SizeErrorException(ScriptErrors.Position.extract(block), code="1")
        
        if expr.value <= 0:
            # code SE-2
            raise SizeErrorException(ScriptErrors.Position.extract(block), code="2")

        return expr.value
    elif block.getText().find('?') != -1:
        # Dynamic size
        return '?'



def _handle_variable_subdeclaration(self: Place, block: any, parent: Any, type: str, is_const: bool = False):
    """
    Handles declaration of a single variable in varDecl or constDecl
    ||| varAssign: ID sizeVar* ('=' expr)?;
    """

    var_name = block.ID().getText()

    if var_name in self.scopes.current.vars:
        # code: VR-1
        raise VariableRedefiniotionException(ScriptErrors.Position.extract(block), code="1")

    if is_const and block.expr() is None:
        # code: CFV-10
        raise CantFindVariableException(
            pos=ScriptErrors.Position.extract(block.ID()),
            var_name=var_name,
            code="10"
        )

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
        # code: ONS-1
        raise OperationNotSupportedException(
            pos=ScriptErrors.Position.extract(block),
            msg="Const state variables are not supported.",
            code="1"
        )

    if len(dimensions) == 0:
        dimensions = [0]


    if type == TYPE_STATE and initial_value is not None:
        # code: DQA-7
        raise DirectQuantumAccessException(
            pos=ScriptErrors.Position.extract(block.expr()),
            code="7"
        )

    var = Variable(var_name, type, dimensions, quantum_client=self.quantum_client, is_const=is_const)
    if initial_value is not None:
        if type == TYPE_OBS and not isinstance(initial_value, list) and not (
            isinstance(initial_value, Expression) and initial_value.type == TYPE_LIST
        ) and dimensions != [0]:
            size = dimensions[0] if isinstance(dimensions, list) else dimensions
            if isinstance(initial_value, Expression) and initial_value.type in [TYPE_INT, TYPE_NUM]:
                initial_value = do_operation_int_to_bits(initial_value, size)
            elif isinstance(initial_value, (int, float)):
                initial_value = do_operation_int_to_bits(Expression(TYPE_INT, initial_value), size)
            else:
                initial_value = Expression(TYPE_LIST, [initial_value], shape=1)

        if isinstance(initial_value, list):
            initial_value = _normalize_list_values(initial_value)
            value_shape = _list_shape(initial_value)

            expected_shapes = [dimensions]

            is_valid_shape = False
            for expected in expected_shapes:
                if isinstance(value_shape, list) and value_shape == expected:
                    is_valid_shape = True
                    break
                if isinstance(value_shape, int) and len(expected) == 1 and value_shape == expected[0]:
                    is_valid_shape = True
                    break

            if value_shape is None or not is_valid_shape:
                # code: SM-1
                raise ShapeMismatchException(
                    pos=ScriptErrors.Position.extract(block),
                    left_shape=dimensions,
                    right_shape=value_shape,
                    code="1"
                )

            initial_value = Expression(TYPE_LIST, initial_value, shape=value_shape)
        elif isinstance(initial_value, Expression) and initial_value.type == TYPE_LIST:
            if(is_dynamic):
                dimensions = initial_value.shape
                var.dimensions = dimensions
            value_shape = initial_value.shape
            initial_value = Expression(TYPE_LIST, initial_value.value, shape=value_shape)
            
            if is_dynamic:
                var_dims = value_shape if isinstance(value_shape, list) else [value_shape]
            else:
                var_dims = dimensions
            var = Variable(var_name, type, var_dims, quantum_client=self.quantum_client, is_const=is_const)
            
            if isinstance(dimensions, int):
                dimensions = [dimensions]

            expected_shapes = [dimensions]

            is_valid_shape = False
            for expected in expected_shapes:
                if isinstance(value_shape, list) and value_shape == expected:
                    is_valid_shape = True
                    break
                if isinstance(value_shape, int) and len(expected) == 1 and value_shape == expected[0]:
                    is_valid_shape = True
                    break

            if value_shape is None or not is_valid_shape:
                # code: SM-1
                raise ShapeMismatchException(
                    pos=ScriptErrors.Position.extract(block),
                    left_shape=dimensions,
                    right_shape=value_shape,
                    code="1"
                )

        var.set(initial_value, allow_const_init=is_const)
        var.initial_value = copy.deepcopy(initial_value)

    self.scopes.create(var_name, var)

    


def handle_variable_declaration(self: Place, block: any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles multiple variable declaration in varDecl
    ||| varDecl: varType varAssign (',' varAssign)*
    """
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
        # code: ONS-2
        raise OperationNotSupportedException(
            pos=ScriptErrors.Position.extract(block.varType()),
            msg=f"Unsupported variable type: {var_type}",
            code="2"
        )
    
    for var_assign in block.varAssign():
        _handle_variable_subdeclaration(self, var_assign, block, var_type)


def handle_const_variable_declaration(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles multiple const variable declaration in constDecl
    ||| constDecl: CONST varType constAssign (',' constAssign)*;
    """
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
        # code: ONS-3
        raise OperationNotSupportedException(
            pos=ScriptErrors.Position.extract(block.varType()),
            msg=f"Unsupported variable type: {var_type}",
            code="3"
        )

    if var_type == TYPE_STATE:
        # code: ONS-1
        raise OperationNotSupportedException(
            pos=ScriptErrors.Position.extract(block.varType()),
            msg="Const state variables are not supported.",
            code="1"
        )

    for const_assign in block.constAssign():
        _handle_variable_subdeclaration(self, const_assign, block, var_type, is_const=True)


def handle_const_existing_variable(self: Place, block: any, parent: Any, pos: ScriptErrors.Position):
    """
    Applies const modifier to already existing variable
    ||| constExisting: CONST ID;
    """
    # constDecl: CONST ID;
    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        # code: CFV-10
        raise CantFindVariableException(
            pos=ScriptErrors.Position.extract(block.ID()),
            var_name=var_name,
            code="10"
        )

    variable = self.scopes.get(var_name)

    if isinstance(variable, Variable) and variable.type == TYPE_STATE:
        # code: ONS-1
        raise OperationNotSupportedException(
            pos=ScriptErrors.Position.extract(block),
            msg="Const state variables are not supported.",
            code="1"
        )

    if isinstance(variable, Variable):
        variable.is_const = True




