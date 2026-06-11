from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...exception.cant_find_variable import CantFindVariableException
from ...expression import Expression

if TYPE_CHECKING:
    from place import Place

def _map_type_name(name: str) -> str:
    if name == "Num" or name == "int" or name == "float" or name == "bool":
        return "num"
    if name == "Obs" or name == "TYPE_OBS":
        return "obs"
    if name == "ObsRegister":
        return "obsRegister"
    if name == "State" or name == "TYPE_STATE":
        return "state"
    if name == "StateRegister":
        return "stateRegister"
    if name == "Text" or name == "text" or name == "string" or name == "TYPE_TEXT" or name == "str":
        return "text"
    if name == "Function":
        return "function"
    if name == "list" or name == "Array":
        return "list"
    if name == "any" or name == "TYPE_ANY":
        return "any"
    if name == "TYPE_NUM":
        return "num"
    return name

def _resolve_variable_type(var: Any, num_indices: int) -> str:
    base_type = _map_type_name(var.type)
    if base_type == "obsRegister":
        base_type = "obs"
    elif base_type == "stateRegister":
        base_type = "state"
        
    num_dims = 0
    if hasattr(var, 'dimensions') and var.dimensions:
        num_dims = 0 if var.dimensions == [0] else len(var.dimensions)
        
    remaining_dims = max(0, num_dims - num_indices)
    if remaining_dims == 0:
        return base_type
    elif remaining_dims == 1:
        if base_type == "obs":
            return "obsRegister"
        if base_type == "state":
            return "stateRegister"
        return "list"
    else:
        return "list"

def handle_type_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # $ expr
    expr = block.expr()
    
    # For now, assume expr is VarExpr
    if hasattr(expr, 'ID') and hasattr(expr, 'index'):
        # It's a VarExpr with indices
        var_name = expr.ID().getText()
        if not self.scopes.exists(var_name):
            # code CFV-3
            raise CantFindVariableException(
                pos=ScriptErrors.Position.extract(expr.ID()), 
                var_name=var_name,
                code="3"
            )
        var = self.scopes.get(var_name)
        
        # If the variable type is "any", we resolve its value to get the dynamic type.
        if hasattr(var, 'type') and var.type in ["any", "TYPE_ANY"]:
            try:
                value = self.handle_block(expr, block)
            except Exception:
                value = var.get() if hasattr(var, 'get') else var
            
            try:
                if isinstance(value, list):
                    return "list"
                if isinstance(value, Expression):
                    t = value.type
                elif hasattr(value, 'type'):
                    t = value.type
                else:
                    from ...variable import Variable
                    if isinstance(value, Variable):
                        t = value.type
                    else:
                        t = type(value).__name__
                return _map_type_name(t)
            except Exception:
                return "unknown"
            
        try:
            indices = [self.handle_block(e, block) for e in expr.index()]
            return _resolve_variable_type(var, len(indices))
        except Exception:
            return "unknown"
    else:
        # For simple expr, handle normally but get type
        value = self.handle_block(expr, block)
        if isinstance(value, list):
            return "list"
        if isinstance(value, Expression):
            t = value.type
        elif hasattr(value, 'type'):
            t = value.type
        else:
            from ...variable import Variable
            if isinstance(value, Variable):
                num_indices = len(value.index) if (hasattr(value, 'index') and value.index) else 0
                return _resolve_variable_type(value, num_indices)
            else:
                t = type(value).__name__

        return _map_type_name(t)