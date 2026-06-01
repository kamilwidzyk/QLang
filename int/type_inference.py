from .expression import TYPE_NUM, TYPE_TEXT, TYPE_OBS, TYPE_STATE, Expression
from .obs import Obs, ObsRegister
from .state import State
from .text import Text

def infer_type_from_value(value):
    """
    Infers internal QLang type from provided python value or Expression. 
    """
    inner_val = value.extract_raw_value() if isinstance(value, Expression) else value
    
    while isinstance(inner_val, list) and len(inner_val) > 0:
        inner_val = inner_val[0]
        if isinstance(inner_val, Expression):
            inner_val = inner_val.extract_raw_value()

    if isinstance(inner_val, (str, Text)):
        return TYPE_TEXT
    elif isinstance(inner_val, (bool, Obs, ObsRegister)):
        return TYPE_OBS
    elif isinstance(inner_val, State):
        return TYPE_STATE
    from .function import Function
    if isinstance(inner_val, Function):
        return "Function"
    else:
        # Default to NUM for int, float, Num, or empty list
        return TYPE_NUM
