from typing import Any, TYPE_CHECKING
from ...script_errors import ScriptErrors
from ...num import Num

if TYPE_CHECKING:
    from place import Place

def handle_num_declaration(self: 'Place', block: Any, parent: Any, pos: ScriptErrors.Position):
    # numDecl: NUM ID ('[' expr ']')? ('=' expr)?
    var_name = block.ID().getText()

    if self.scopes.exists(var_name):
        self.script_errors.showError(
            pos=pos, error_type="RUNTIME ERROR", title="Name Conflict",
            msg=f"Variable '{var_name}' already exists."
        )
        exit()

    expressions = [x for x in block.expr()]
    array_size = None
    initial_val = 0.0

    if len(expressions) == 1:

        has_assignment = '=' in [child.getText() for child in block.getChildren()]

        if has_assignment:
            initial_val = self.handle_block(expressions[0], block)
        else:
            array_size = self.handle_block(expressions[0], block)

    elif len(expressions) == 2:
        array_size = self.handle_block(expressions[0], block)
        initial_val = self.handle_block(expressions[1], block)


    if array_size is not None:
        if not isinstance(array_size, (int, float)) or int(array_size) != array_size or array_size <= 0:
            self.script_errors.showError(
                pos=pos, error_type="RUNTIME ERROR", title="Invalid Array Size",
                msg=f"Array size must be a positive integer. Got: {array_size}"
            )
            exit()

        if initial_val != 0.0:
            self.script_errors.showError(
                pos=pos, error_type="SYNTAX LIMITATION", title="Array Initialization",
                msg="You cannot assign a single value to an entire array at declaration yet."
            )
            exit()

        #array_var = NumArray(int(array_size))
        #array_var.name = var_name
        #self.scopes.create(var_name, array_var)

    else:
        try:
            num_var = Num(initial_val)
            num_var.name = var_name
            self.scopes.create(var_name, num_var)
        except (ValueError, TypeError):
            self.script_errors.showError(
                pos=pos,
                error_type="RUNTIME ERROR",
                title="Type Mismatch",
                msg=f"The variable '{var_name}' is defined as 'num' (numeric), "
            )
            exit()