from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister

from ...expression import Expression, TYPE_INT, TYPE_LIST, TYPE_OBS, TYPE_NUM, TYPE_OBS_REGISTER, TYPE_TEXT
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



def _handle_variable_subdeclaration(self: Place, block: any, parent: Any, type: str):
    # varAssign: ID sizeVar* ('=' expr)?;

    var_name = block.ID().getText()

    if var_name in self.scopes.current.vars:
        raise VariableRedefiniotionException(ScriptErrors.Position.extract(block))

    dimensions = []
    for size in block.sizeVar():
        dim = handle_variable_sizevar(self, size, block)
        dimensions.append(dim if dim != '?' else -100)

    # Remember if it was dynamic
    is_dynamic = -100 in [d for d in dimensions if isinstance(d, int)] or len(dimensions) == 0
    
    initial_value = None

    if block.expr():
        initial_value = self.handle_block(block.expr(), block)

    print(f"Variable declaration: name: {var_name}, dimensions: {dimensions}, initial_value: {initial_value}, type: {type}")

    if type == TYPE_OBS and len(dimensions) >= 1:
        type = TYPE_OBS_REGISTER
    
    if len(dimensions) == 0:
        dimensions = [0]


    var = Variable(var_name, type, dimensions)
    print(dimensions, initial_value)
    if initial_value is not None:
        if isinstance(initial_value, list):
            initial_value = _normalize_list_values(initial_value)
            value_shape = _list_shape(initial_value)

            if value_shape is None or (isinstance(value_shape, int) and value_shape != dimensions[0]) or (isinstance(value_shape, list) and value_shape != dimensions):
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
            print("Initial value is a list expression with shape:", initial_value.shape)
            print("Size dynamic: ", is_dynamic)
            if(is_dynamic):
                dimensions = initial_value.shape
                var.dimensions = dimensions
            value_shape = initial_value.shape
            initial_value = Expression(TYPE_LIST, initial_value.value, shape=value_shape)
            var = Variable(var_name, type, value_shape)
            print("Dimesions: ", dimensions)
            print("Initial value shape: ", value_shape)
            print("Initial value: ", initial_value)
            
            if isinstance(dimensions, int):
                dimensions = [dimensions]

            if initial_value.shape is None or (isinstance(initial_value.shape, int) and initial_value.shape != dimensions[0]) or (isinstance(initial_value.shape, list) and initial_value.shape != dimensions):
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
        var.set(initial_value)
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
    else:
        log(VARIABLE, FATAL, "Unsupported variable type: " + str(var_type))
        exit()
    
    for var_assign in block.varAssign():
        _handle_variable_subdeclaration(self, var_assign, block, var_type)




