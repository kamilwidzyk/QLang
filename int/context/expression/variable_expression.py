from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...expression import Expression

from ...exception.cant_find_variable import CantFindVariableException

if TYPE_CHECKING:
    from place import Place

def handle_variable_expression(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position, return_variable=False):
    # ID ('[' expr ']')*

    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        raise CantFindVariableException(ScriptErrors.Position.extract(block), var_name)

    variable = self.scopes.get(var_name)

    index = []
    
    for expr in block.expr():
        index.append(
            self.handle_block(expr, block).value
        )

    print("index: ", index)


    variable.index = index

    if return_variable:
        return variable

    if isinstance(variable, Expression):
        return variable

    if hasattr(variable, "get"):
        return variable.get()

    return variable



    if type(variable) == int:
        return variable

    # Check if it can be read
    if variable.type in ["StateRegister", "State"]:
        self.script_errors.showError(
            pos=parent_pos,
            error_type="RUNTIME ERROR",
            title="Access Denied",
            msg="You can't access a quantum state like that. Try measuring it first.")
        exit()

    if index is not None:
        # Check if variable supports index (Dodano NumArray)
        if variable.type not in ["ObsRegister", "NumArray"]:
            self.script_errors.showError(
                pos=parent_pos,
                error_type="RUNTIME ERROR",
                title="Access denied",
                msg="There is nothing more, just a single value. You cannot index this variable.")
            exit()

        # Check if index is int (Zabezpieczenie przed floatami jako index)
        if int(index) != index:
            self.script_errors.showError(
                pos=parent_pos,
                error_type="RUNTIME ERROR",
                title="QuantizationError",
                msg="Try looking at the items, not between them. Index must be an integer.")
            exit()

        # Check if index is >= 0
        if index < 0:
            self.script_errors.showError(
                pos=parent_pos,
                error_type="RUNTIME ERROR",
                title="BoundaryBreach",
                msg=f"You attempted to access index {index}. Aren't you scared of going into the unknown.")
            exit()

        if variable.type == "NumArray":
            try:
                return variable.get(int(index))
            except IndexError as e:
                self.script_errors.showError(
                    pos=parent_pos,
                    error_type="RUNTIME ERROR",
                    title="BoundaryBreach",
                    msg=str(e))
                exit()

        # Return the value from ObsRegister as 0/1 (not bool)
        return 1 if variable[int(index)] else 0


    if variable.type == "Obs":
        return 1 if variable.get() else 0

    if variable.type == "ObsRegister":
        return variable.get()

    if variable.type == "Num":
        return variable.get()

    if variable.type == "NumArray":
        return variable.values

    self.script_errors.showError(
        pos=parent_pos,
        error_type="RUNTIME ERROR",
        title="Type Error",
        msg=f"What is this variable of type '{variable.type}' doing here?")
    exit()