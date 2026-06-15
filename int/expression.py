

# This class encloses all retured values for most blocks
# with the exception of blocks that have custom handlers(= do not call handle_block)
# 
# 
# [1] Type specified is the internal type(lowercase)
#   - int
#   - float
#   - bool
#   - (some state type, not now)
#   - string (there is no string variable yet) 
#   - list
# [2] Other types that should not get to the output(same as variable class names):
#   - Obs
#   - ObsRegister
#   - Num
#   - State
#   - StateRegister
#   - Array
# When type of [1] is used the value needs to be specified
# When type of [2] is used the variable needs to be specified

TYPE_INT = "int"
TYPE_FLOAT = "float"
TYPE_BOOL = "bool"
TYPE_STRING = "string"
TYPE_TEXT = "text"
TYPE_OBS = "Obs"
TYPE_OBS_REGISTER = "ObsRegister"
TYPE_NUM = "Num"
TYPE_STATE = "State"
TYPE_STATE_REGISTER = "StateRegister"
TYPE_LIST = "list" # [expr, expr, ...]
TYPE_ARRAY = "Array" # instance of multidimensional Variable
TYPE_ANY = "any"

from .text import Text

import traceback


def type_to_rank(value):
    if hasattr(value, 'type'):
        if value.type == TYPE_BOOL:
            return 1
        if value.type == TYPE_INT:
            return 2
        if value.type == TYPE_FLOAT:
            return 3
        if value.type == TYPE_STRING:
            return 4
        if value.type == TYPE_NUM:
            if hasattr(value, 'value') and hasattr(value.value, 'is_float'):
                return 3 if value.value.is_float else 2
            if hasattr(value, 'data') and hasattr(value.data, 'is_float'):
                return 3 if value.data.is_float else 2
            if hasattr(value, 'is_float'):
                return 3 if value.is_float else 2
            return 2
    else:
        if isinstance(value, bool):
            return 1
        if isinstance(value, int):
            return 2
        if isinstance(value, float):
            return 3
        if isinstance(value, str):
            return 4

    
    
def rank_to_type(type: int):
    if type == 1:
        return TYPE_BOOL
    if type == 2:
        return TYPE_INT
    if type == 3:
        return TYPE_FLOAT
    if type == 4:
        return TYPE_STRING

def get_max_type(left, right):
    left_rank = type_to_rank(left)
    right_rank = type_to_rank(right)

    return rank_to_type(max(left_rank, right_rank))





class ValueResolver:
    @staticmethod
    def is_state(value):
        return type(value).__name__ == 'State'

    @staticmethod
    def _resolve_indexed_variable(value):
        if hasattr(value, 'index') and value.index:
            if hasattr(value, 'get'):
                try:
                    return value.get()
                except Exception:
                    pass
        return value

    @staticmethod
    def extract_raw_value(value):
        #print('extract_raw_value: ', value)
        val = ValueResolver._resolve_indexed_variable(value)
        for _ in range(50):
            #print("iteration: ", val)
            if ValueResolver.is_state(val):
                break
            if isinstance(val, list):
                return [ValueResolver.extract_raw_value(item) for item in val]
            if hasattr(val, 'get'):
                #print("get")
                try:
                    val = val.get()
                    continue
                except TypeError:
                    break
            if hasattr(val, 'get_value'):
                #print("get_value")
                try:
                    val = val.get_value()
                    if hasattr(val, 'value'):
                        val = val.value
                    continue
                except TypeError:
                    break
            
            break
        if isinstance(val, list):
            return [ValueResolver.extract_raw_value(item) for item in val]
        return val

    @staticmethod
    def extract_value(value):
        return ValueResolver.extract_raw_value(value)

    @staticmethod
    def to_primitive(value):
        value = ValueResolver._resolve_indexed_variable(value)
        if isinstance(value, Expression):
            return ValueResolver.to_primitive(value.get_value())

        if hasattr(value, 'get_value'):
            try:
                return ValueResolver.to_primitive(value.get_value())
            except TypeError:
                pass

        if hasattr(value, 'get'):
            try:
                return ValueResolver.to_primitive(value.get())
            except TypeError:
                pass

        if hasattr(value, 'value'):
            return ValueResolver.to_primitive(value.value)
        if hasattr(value, 'data'):
            return ValueResolver.to_primitive(value.data)
        return value

    @staticmethod
    def resolve_for_operation(value):
        #print("resolve_for_operation: ", value)
        value = ValueResolver._resolve_indexed_variable(value)
        for _ in range(50):
            #print("resolve iteration: ", value)
            if ValueResolver.is_state(value):
                break
            if isinstance(value, Expression):
                value = value.get_value()
                continue
            if hasattr(value, 'get_value'):
                # Preserve wrapper objects that have custom value semantics.
                # Unwrapping Obs/ObsRegister/Num/Text too early breaks operations like string concatenation.
                if type(value).__name__ in ('Obs', 'Num', 'Text'):
                    break
                try:
                    new_value = value.get_value()
                except TypeError:
                    break
                if new_value is value:
                    break
                value = new_value
                continue

            if hasattr(value, 'get'):
                try:
                    new_value = value.get()
                except TypeError:
                    break
                if new_value is value:
                    break
                value = new_value
                continue

            if hasattr(value, 'value') and not isinstance(value, (int, float, str, bool, list)):
                value = value.value
                continue

            if hasattr(value, 'data') and not isinstance(value, (int, float, str, bool, list)):
                value = value.data
                continue

            break

        return value

    @staticmethod
    def is_list(expr):
        from .expression import TYPE_LIST
        expr = ValueResolver.resolve_for_operation(expr)
        return (
            isinstance(expr, list)
            or (hasattr(expr, 'type') and expr.type == TYPE_LIST)
            or (hasattr(expr, 'data') and isinstance(expr.data, list))
        )
    
    @staticmethod
    def is_bool(expr):
        from .expression import TYPE_BOOL
        expr = ValueResolver.resolve_for_operation(expr)
        return (
            isinstance(expr, bool)
            or (hasattr(expr, 'type') and expr.type == TYPE_BOOL)
            or (hasattr(expr, 'data') and isinstance(expr.data, bool))
        )

    @staticmethod
    def is_string_or_text(expr):
        from .expression import TYPE_STRING, TYPE_TEXT
        expr = ValueResolver.resolve_for_operation(expr)
        if isinstance(expr, str):
            return True
        if hasattr(expr, 'type') and expr.type in [TYPE_STRING, TYPE_TEXT]:
            return True
        from .text import Text
        return isinstance(expr, Text)

    @staticmethod
    def extract_list(expr):
        expr = ValueResolver.resolve_for_operation(expr)
        if hasattr(expr, 'type') and expr.type == TYPE_LIST:
            return expr.value
        if isinstance(expr, list):
            return expr
        if hasattr(expr, 'data') and isinstance(expr.data, list):
            return expr.data
        raise TypeError('Expected a list expression')

    @staticmethod
    def extract_string(expr):
        #print("extract_string:", expr)
        expr = ValueResolver.resolve_for_operation(expr)
        from .text import Text
        if hasattr(expr, 'type') and expr.type == TYPE_STRING:
            return expr.value
        if hasattr(expr, 'type') and expr.type == TYPE_TEXT:
            return expr.value
        if isinstance(expr, Text):
            return expr.get()
        if isinstance(expr, str):
            return expr
        raise TypeError('Expected a string or text expression')

    @staticmethod
    def convert_value(value):
        value = ValueResolver.resolve_for_operation(value)
        from .obs import Obs
        from .num import Num
        from .text import Text
        if isinstance(value, (Num, Obs, Text)):
            return ValueResolver.convert_value(value.get_value())
        if isinstance(value, Expression):
            return ValueResolver.convert_value(value.get_value())
        if hasattr(value, 'data') and isinstance(value.data, list):
            return [ValueResolver.convert_value(x) for x in value.data]
        if isinstance(value, list):
            return [ValueResolver.convert_value(x) for x in value]
        if isinstance(value, (int, float, str)):
            return value
        if isinstance(value, bool):
            return 'T' if value else 'F'
        if isinstance(value, Obs):
            return 'T' if value.get_value() else 'F'
        return value

    @staticmethod
    def list_shape(values):
        if not isinstance(values, list):
            return []
        if len(values) == 0:
            return [0]

        def item_shape(item):
            if isinstance(item, Expression) and item.type == TYPE_LIST:
                if isinstance(item.shape, list):
                    return item.shape
                if isinstance(item.shape, int):
                    return [item.shape]
                return []
            if isinstance(item, list):
                return ValueResolver.list_shape(item)
            return []

        first_shape = item_shape(values[0])
        for element in values[1:]:
            if item_shape(element) != first_shape:
                return None
        return [len(values)] + first_shape

    @staticmethod
    def wrap_value(type_name, value, quantum_client=None):
        from .obs import Obs
        from .num import Num
        from .text import Text
        from .state import State

        if type_name == TYPE_OBS:
            if isinstance(value, Obs):
                return value
            obj = Obs()
            if value is not None:
                obj.set(value)
            return obj
        if type_name == TYPE_NUM:
            if isinstance(value, Num):
                return value
            obj = Num()
            if value is not None:
                obj.set(value)
            return obj
        if type_name == TYPE_TEXT:
            if isinstance(value, Text):
                return value
            obj = Text('')
            if value is not None:
                obj.set(value)
            return obj
        if type_name == TYPE_STATE:
            if value is not None and type(value).__name__ == 'State':
                return value
            return State(client=quantum_client)
        return value

    @staticmethod
    def wrap_list(type_name, values, quantum_client=None):
        if not isinstance(values, list):
            return ValueResolver.wrap_value(type_name, values, quantum_client)
        return [ValueResolver.wrap_list(type_name, v, quantum_client) for v in values]


class Expression:
    def __init__(self, type: str, value=None, variable=None, shape=None):
        self.type = type         # internal type
        self.value = value
        self.variable = variable
        self.shape = shape # when type is list -> this is the shape from outer to inner
        if isinstance(shape, int):
            self.dimensions = [shape]
        elif shape is None:
            self.dimensions = []
        else:
            self.dimensions = shape

    def get(self):
        if self.variable is not None:
            return self.variable.get()
        return self.value
    
    def __len__(self):
        if self.variable is not None:
            return len(self.variable)
        if self.value is not None:
            if isinstance(self.value, bool):
                return 1 if self.value else 0
            return len(self.value)
        return 0

    def __bool__(self):
        if self.variable is not None:
            return bool(self.variable)
        value = self.value
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) != 0
        if isinstance(value, list):
            return len(value) != 0
        return True

    def __getitem__(self, key):
        if self.variable is not None:
            return self.variable[key]
        if self.value is not None:
            return self.value[key]
        raise TypeError("Expression of type " + str(self.type) + " is not subscriptable")
    
    def __setitem__(self, key, value):
        if self.variable is not None:
            self.variable[key] = value
        elif self.value is not None:
            self.value[key] = value
        else:
            raise TypeError("Expression of type " + str(self.type) + " is not subscriptable")

    def get_value(self):
        val = self.get()
        if hasattr(val, 'get_value') and not ValueResolver.is_state(val):
            return val.get_value()
        return val

    @staticmethod
    def _to_primitive(value):
        return ValueResolver.to_primitive(value)

    def _extract_value_from(value):
        return ValueResolver.extract_raw_value(value)

    def extract_value(self):
        return ValueResolver.extract_raw_value(self)

    def extract_raw_value(self):
        return ValueResolver.extract_raw_value(self)

    def __get_other_value(self, other):
        # Deterministic unwrapping loop. Try common accessors in order until
        # we reach a Python primitive (int/float/str/bool/list) or exhaust attempts.
        for _ in range(10):
            if isinstance(other, Expression):
                other = other.get_value()
                continue

            if hasattr(other, 'get_value'):
                try:
                    new = other.get_value()
                    if new is other:
                        break
                    other = new
                    continue
                except TypeError:
                    pass
                except Exception:
                    break

            if hasattr(other, 'get'):
                try:
                    new = other.get()
                    if new is other:
                        break
                    other = new
                    continue
                except TypeError:
                    pass
                except Exception:
                    break

            if hasattr(other, 'value') and not isinstance(other, (int, float, str, bool, list)):
                try:
                    new = other.value
                    if new is other:
                        break
                    other = new
                    continue
                except Exception:
                    break

            if hasattr(other, 'data') and not isinstance(other, (int, float, str, bool, list)):
                try:
                    new = other.data
                    if new is other:
                        break
                    other = new
                    continue
                except Exception:
                    break

            break

        return other
    
    def __lt__(self, other):
        return Expression(TYPE_BOOL, self.get_value() < self.__get_other_value(other))
    
    def __le__(self, other):
        return Expression(TYPE_BOOL, self.get_value() <= self.__get_other_value(other))
    
    def __gt__(self, other):
        return Expression(TYPE_BOOL, self.get_value() > self.__get_other_value(other))
    
    def __ge__(self, other):
        return Expression(TYPE_BOOL, self.get_value() >= self.__get_other_value(other))
    
    def __eq__(self, other):
        return Expression(TYPE_BOOL, self.get_value() == self.__get_other_value(other))
    
    def __ne__(self, other):
        return Expression(TYPE_BOOL, self.get_value() != self.__get_other_value(other))
    

    
    def __add__(self, other):
        other = self.__get_other_value(other)
        if self.type == TYPE_STRING or isinstance(other, str):
            return Expression(TYPE_STRING, str(self.get_value()) + str(other))

        result_type = get_max_type(self, other)
        if result_type is None:
            raise TypeError(f"Unsupported operand types for +: '{self.type}' and '{type(other).__name__}'")
        if result_type == TYPE_FLOAT:
            return Expression(TYPE_FLOAT, float(self.get_value()) + float(other))
        return Expression(TYPE_INT, int(self.get_value()) + int(other))

    def __sub__(self, other):
        other = self.__get_other_value(other)
        result_type = get_max_type(self, other)
        if result_type is None:
            raise TypeError(f"Unsupported operand types for -: '{self.type}' and '{type(other).__name__}'")
        if result_type == TYPE_FLOAT:
            return Expression(TYPE_FLOAT, float(self.get_value()) - float(other))
        return Expression(TYPE_INT, int(self.get_value()) - int(other))
    
    def __mul__(self, other):
        if self.type == TYPE_STRING or self.type == TYPE_TEXT:
            left_text = Text(self.get_value())
            return Text.__mul__(left_text, other)
        other = self.__get_other_value(other)
        result_type = get_max_type(self, other)
        if result_type is None:
            raise TypeError(f"Unsupported operand types for *: '{self.type}' and '{type(other).__name__}'")
        if result_type == TYPE_FLOAT:
            return Expression(TYPE_FLOAT, float(self.get_value()) * float(other))
        return Expression(TYPE_INT, int(self.get_value()) * int(other))
    
    def __truediv__(self, other):
        if self.type == TYPE_STRING or self.type == TYPE_TEXT:
            left_text = Text(self.get_value())
            return Text.__truediv__(left_text, other)
        other = self.__get_other_value(other)
        return Expression(TYPE_FLOAT, float(self.get_value()) / float(other))
    
    def __floordiv__(self, other):
        other = self.__get_other_value(other)
        return Expression(TYPE_INT, int(self.get_value() // other))
    


    def __mod__(self, other):
        if self.type == TYPE_STRING or self.type == TYPE_TEXT:
            left_text = Text(self.get_value())

            return Text.__mod__(left_text, other)

        # Unwrap both operands to primitives to avoid wrapper objects (Num, Variable)
        other = self.__get_other_value(other)
        lhs = Expression._to_primitive(self.get_value())
        rhs = Expression._to_primitive(other)

        # Decide float vs int result
        if isinstance(lhs, float) or isinstance(rhs, float):
            return Expression(TYPE_FLOAT, float(lhs) % float(rhs))
        return Expression(TYPE_INT, int(lhs) % int(rhs))
    
    def __pow__(self, other):
        other = self.__get_other_value(other)
        result_type = get_max_type(self, other)
        if result_type == TYPE_FLOAT:
            return Expression(TYPE_FLOAT, float(self.get_value()) ** float(other))
        return Expression(TYPE_INT, int(self.get_value()) ** int(other))
    
    def __iadd__(self, other):
        self.value = self.get_value() + self.__get_other_value(other)
        return self
    
    def __isub__(self, other):
        self.value = self.get_value() - self.__get_other_value(other)
        return self

    def __imul__(self, other):
        self.value = self.get_value() * self.__get_other_value(other)
        return self

    def __itruediv__(self, other):
        self.value = self.get_value() / self.__get_other_value(other)
        return self
    
    def __ifloordiv__(self, other):
        self.value = self.get_value() // self.__get_other_value(other)
        return self
    
    def __imod__(self, other):
        self.value = self.get_value() % self.__get_other_value(other)
        return self
    
    def __ipow__(self, other):
        self.value = self.get_value() ** self.__get_other_value(other)
        return self
    
    def __radd__(self, other):
        other = self.__get_other_value(other)
        if self.type == TYPE_STRING or isinstance(other, str):
            return Expression(TYPE_STRING, str(other) + str(self.get_value()))
        result_type = get_max_type(self, other)
        if result_type is None:
            raise TypeError(f"Unsupported operand types for +: '{type(other).__name__}' and '{self.type}'")
        if result_type == TYPE_FLOAT:
            return Expression(TYPE_FLOAT, float(other) + float(self.get_value()))
        return Expression(TYPE_INT, int(other) + int(self.get_value()))
    
    def __rsub__(self, other):
        other = self.__get_other_value(other)
        result_type = get_max_type(self, other)
        if result_type is None:
            raise TypeError(f"Unsupported operand types for -: '{type(other).__name__}' and '{self.type}'")
        if result_type == TYPE_FLOAT:
            return Expression(TYPE_FLOAT, float(other) - float(self.get_value()))
        return Expression(TYPE_INT, int(other) - int(self.get_value()))
    
    def __rmul__(self, other):
        other = self.__get_other_value(other)
        result_type = get_max_type(self, other)
        if result_type is None:
            raise TypeError(f"Unsupported operand types for *: '{type(other).__name__}' and '{self.type}'")
        if result_type == TYPE_FLOAT:
            return Expression(TYPE_FLOAT, float(other) * float(self.get_value()))
        return Expression(TYPE_INT, int(other) * int(self.get_value()))
    
    def __rtruediv__(self, other):
        other = self.__get_other_value(other)
        return Expression(TYPE_FLOAT, float(other) / float(self.get_value()))
    
    def __rfloordiv__(self, other):
        other = self.__get_other_value(other)
        return Expression(TYPE_INT, int(other) // self.get_value())
    
    def __rmod__(self, other):
        other = self.__get_other_value(other)
        result_type = get_max_type(self, other)
        if result_type == TYPE_FLOAT:
            return Expression(TYPE_FLOAT, float(other) % float(self.get_value()))
        return Expression(TYPE_INT, int(other) % int(self.get_value()))
    
    def __rpow__(self, other):
        other = self.__get_other_value(other)
        result_type = get_max_type(self, other)
        if result_type == TYPE_FLOAT:
            return Expression(TYPE_FLOAT, float(other) ** float(self.get_value()))
        return Expression(TYPE_INT, int(other) ** int(self.get_value()))
    
    