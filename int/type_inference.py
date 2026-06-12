from .expression import TYPE_NUM, TYPE_TEXT, TYPE_OBS, TYPE_STATE, TYPE_ANY, Expression
from .obs import Obs, ObsRegister
from .state import State
from .text import Text

def infer_type_from_value(value):
    """
    Infers internal QLang type from provided python value or Expression. 
    """
    def unwrap_value(v):
        if isinstance(v, Expression):
            return unwrap_value(v.extract_raw_value())
        return v

    def infer_single_type(v):
        v = unwrap_value(v)
        if isinstance(v, list):
            if len(v) == 0:
                return TYPE_NUM
            return infer_single_type(v[0])
        if isinstance(v, (str, Text)):
            return TYPE_TEXT
        if isinstance(v, (bool, Obs, ObsRegister)):
            return TYPE_OBS
        if isinstance(v, State):
            return TYPE_STATE
        from .function import Function
        if isinstance(v, Function):
            return "Function"
        return TYPE_NUM

    inner_val = unwrap_value(value)
    if isinstance(inner_val, list):
        element_types = set()
        for element in inner_val:
            element_types.add(infer_single_type(element))
            if len(element_types) > 1:
                return TYPE_ANY
        return element_types.pop() if element_types else TYPE_NUM

    return infer_single_type(inner_val)
