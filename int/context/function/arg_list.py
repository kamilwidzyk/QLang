from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors

if TYPE_CHECKING:
    from place import Place

def handle_arg_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # argList: expr (',' expr)*;

    named_arg_list = block.namedArgList()
    if named_arg_list:
        arg_names = [token.getText() for token in named_arg_list.ID()]
        arg_values = [self.handle_block(expr, block) for expr in named_arg_list.expr()]
        return dict(zip(arg_names, arg_values))

    return [self.handle_block(expr, block) for expr in block.standardArgList().expr()]
