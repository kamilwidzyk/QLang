from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...exception.cant_find_variable import CantFindVariableException

if TYPE_CHECKING:
    from place import Place

def handle_type_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # $ expr
    expr = block.expr()
    # For now, assume expr is VarExpr
    if hasattr(expr, 'ID') and hasattr(expr, 'expr'):
        # It's a VarExpr with indices
        var_name = expr.ID().getText()
        indices = [self.handle_block(e, block) for e in expr.expr()]
        if var_name not in self.scopes.current.vars:
            # code CFV-2
            raise CantFindVariableException(
                pos=ScriptErrors.Position.extract(expr.ID()), 
                var_name=var_name,
                code="2"
            )
        var = self.scopes.current.vars[var_name]
        if indices:
            # For indexed, return base type
            return var.type
        else:
            # For array, return type with dimensions
            dims = [str(d) for d in var.dimensions if d > 0]
            if dims:
                return f"{var.type}[{']['.join(dims)}]"
            else:
                return var.type
    else:
        # For simple expr, handle normally but get type
        value = self.handle_block(expr, block)
        # TODO: To jest do zrobienia
        return type(value).__name__  # or something, but for variables it's better