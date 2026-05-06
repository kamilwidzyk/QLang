from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..function import Function

if TYPE_CHECKING:
    from place import Place

def handle_function_declaration(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # functionDecl: FUNCTION returnType? ID '(' paramList? ')' block;

    return_type = "void"
    return_type_ctx = block.returnType()
    if return_type_ctx is not None:
        if return_type_ctx.VOID():
            return_type = "void"
        elif return_type_ctx.NUM():
            return_type = "num"
        elif return_type_ctx.STATE():
            return_type = "state"
        elif return_type_ctx.OBS():
            return_type = "obs"

    func_name = block.ID().getText()
    param_list = None
    if block.paramList():
        param_list = self.handle_block(block.paramList(), block)

    func_block = self.handle_block(block.block(), block)

    parent_pos = ScriptErrors.Position.extract(parent) if parent else pos

    # check if function does not exist
    if self.scopes.exists(func_name):
        self.script_errors.showError(
            pos=parent_pos,
            error_type="RUNTIME ERROR",
            title="You Error",
            msg="The function already exists, whether you remember it or not."
        )
        exit()

    # add function to current scope
    func = Function(func_name, param_list, func_block, self.scopes.current, pos, return_type)
    self.scopes.create(func_name, func)
