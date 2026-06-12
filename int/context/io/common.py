from int.num import Num
from int.text import Text
from int.expression import Expression
from int.variable import Variable
from int.obs import Obs

def convert_value(value):
    result = None
    if isinstance(value, (Num, Text)):
        result = value.get_value()
        if isinstance(result, bool):
            result = int(result)
    if isinstance(value, Expression):
        result = convert_value(value.get())
    if isinstance(value, Variable):
        result = convert_value(value.get())
    if isinstance(value, list):
        result = [convert_value(x) for x in value]
    if isinstance(value, (int, float, str)):
        result = value
    if isinstance(value, bool):
        result = 'T' if value else 'F'
    if isinstance(value, Obs):
        result = 'T' if value.get_value() else 'F'

    while hasattr(result, 'get_value'):
        result = result.get_value()

    return result