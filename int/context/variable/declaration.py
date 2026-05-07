from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister

from ...expression import TYPE_INT, TYPE_OBS, TYPE_NUM, TYPE_OBS_REGISTER
from ...logger import log, VARIABLE, FATAL

from ...exception.size_error import SizeErrorException
from ...exception.variable_redefinition import VariableRedefiniotionException
from ...variable import Variable

if TYPE_CHECKING:
    from place import Place


def handle_variable_sizevar(self: Place, block: any, parent: any):
    # sizeVar: '[' expr ']'; 
    # Only int allowed as size
    expr = self.handle_block(block.expr(), block)
    if expr.type != TYPE_INT:
        raise SizeErrorException(ScriptErrors.Position.extract(block))
    
    if expr.value <= 0:
        raise SizeErrorException(ScriptErrors.Position.extract(block))

    return expr.value



def _handle_variable_subdeclaration(self: Place, block: any, parent: Any, type: str):
    # varAssign: ID sizeVar* ('=' expr)?;

    var_name = block.ID().getText()

    if var_name in self.scopes.current.vars:
        raise VariableRedefiniotionException(ScriptErrors.Position.extract(block))

    dimensions = []
    for size in block.sizeVar():
        dimensions.append(
            handle_variable_sizevar(self, size, block)
        )
    
    initial_value = None

    if block.expr():
        initial_value = self.handle_block(block.expr(), block)

    print(f"Variable declaration: name: {var_name}, dimensions: {dimensions}, initial_value: {initial_value}, type: {type}")

    if type == TYPE_OBS and len(dimensions) >= 1:
        type = TYPE_OBS_REGISTER
    
    if len(dimensions) == 0:
        dimensions = [0]


    var = Variable(var_name, type, dimensions)
    if initial_value is not None:
        try:
            var.set(initial_value)
        except (AttributeError, TypeError, ValueError):
            self.script_errors.showError(
                pos=ScriptErrors.Position.extract(block),
                error_type="RUNTIME ERROR",
                title="Type Mismatch",
                msg=f"The variable '{var_name}' is defined as '{type}' (numeric)."
            )
            exit()

    self.scopes.create(var_name, var)

    


def handle_variable_declaration(self: Place, block: any, parent: Any, pos: ScriptErrors.Position):
    # varDecl: varType varAssign (',' varAssign)*

    var_type = block.varType().getText()

    if var_type == "obs":
        var_type = TYPE_OBS
    elif var_type == "num":
        var_type = TYPE_NUM
    else:
        log(VARIABLE, FATAL, "Unsupported variable type: " + str(var_type))
        exit()
    
    for var_assign in block.varAssign():
        _handle_variable_subdeclaration(self, var_assign, block, var_type)




