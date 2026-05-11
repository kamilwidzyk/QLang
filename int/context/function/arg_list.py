from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors

if TYPE_CHECKING:
    from place import Place

def handle_arg_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # argList: arg (',' arg)*;
    # arg: expr | namedArg;
    # namedArg: ID '=' expr;

    args = []
    for arg in block.arg():
        if arg.expr() is not None:
            args.append(self.handle_block(arg.expr(), block))
        elif arg.namedArg() is not None:
            named_arg = arg.namedArg()
            arg_name = named_arg.ID().getText()
            arg_value = self.handle_block(named_arg.expr(), block)
            args.append({arg_name: arg_value})
    
    return args
