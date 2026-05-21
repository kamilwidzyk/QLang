from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...function import Function

if TYPE_CHECKING:
    from place import Place

from ...exception.function_redeclaration import FunctionRedeclarationException

def handle_function_declaration(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # functionDecl: FUNCTION ID '(' paramList? ')' block;
    
    func_name = block.ID().getText()
    param_list = None
    if block.paramList():
        param_list = self.handle_block(block.paramList(), block)

    func_block = self.handle_block(block.block(), block)

    parent_pos = ScriptErrors.Position.extract(parent) if parent else pos

    # check if function does not exist
    # code: FR-1
    if self.scopes.exists(func_name):
        raise FunctionRedeclarationException(
            pos=parent_pos, 
            func_name=func_name, 
            code="1"
        )

    # add function to current scope
    func = Function(func_name, param_list, func_block, self.scopes.current, pos)
    self.scopes.create(func_name, func)