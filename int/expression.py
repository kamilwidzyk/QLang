

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





class Expression:
    def __init__(self, type: str, value=None, variable=None, shape=None):
        self.type = type         # internal type
        self.value = value
        self.variable = variable
        self.shape = shape # when type is list -> this is the shape from outer to inner

    def get(self):
        if self.variable is not None:
            return self.variable.get()
        return self.value
    
    def __len__(self):
        if self.variable is not None:
            return len(self.variable)
        if self.value is not None:
            return len(self.value)
        return 0
    
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
        if hasattr(val, 'get_value'):
            if val.__class__.__name__ == 'State':
                return val
            return val.get_value()
        return val

    @staticmethod
    def _to_primitive(value):
        # Force-extract primitive numeric/string from wrappers.
        if isinstance(value, Expression):
            return Expression._to_primitive(value.get_value())
        if hasattr(value, 'get_value'):
            return Expression._to_primitive(value.get_value())
        if hasattr(value, 'get'):
            return Expression._to_primitive(value.get())
        if hasattr(value, 'value'):
            return Expression._to_primitive(value.value)
        if hasattr(value, 'data'):
            return Expression._to_primitive(value.data)
        return value
    
    def _extract_value_from(value):
        from .variable import Variable

        if isinstance(value, (Expression, Variable)):
            return Expression._extract_value_from(value.get_value())
        return value

    def extract_value(self):
        return Expression._extract_value_from(self)

    def extract_raw_value(self):
        val = self
        while hasattr(val, 'get_value'):
            if val.__class__.__name__ == 'State':
                break
            val = val.get_value()
        return val

    def __bool__(self):
        return bool(self.get_value())

    def __get_other_value(self, other):
        # Deterministic unwrapping loop. Try common accessors in order until
        # we reach a Python primitive (int/float/str/bool/list) or exhaust attempts.
        for _ in range(10):
            # Direct Expression objects -> primitive via get_value()
            if isinstance(other, Expression):
                other = other.get_value()
                continue

            # Objects exposing get_value() (Variable, Num, etc.)
            if hasattr(other, 'get_value'):
                try:
                    new = other.get_value()
                    if new is other:
                        break
                    other = new
                    continue
                except Exception:
                    pass

            # Objects exposing get() (Variables sometimes)
            if hasattr(other, 'get'):
                try:
                    new = other.get()
                    if new is other:
                        break
                    other = new
                    continue
                except Exception:
                    pass

            # Common value containers
            if hasattr(other, 'value') and not isinstance(other, (int, float, str, bool, list)):
                try:
                    new = other.value
                    if new is other:
                        break
                    other = new
                    continue
                except Exception:
                    pass

            if hasattr(other, 'data') and not isinstance(other, (int, float, str, bool, list)):
                try:
                    new = other.data
                    if new is other:
                        break
                    other = new
                    continue
                except Exception:
                    pass

            break

        return other

        # Extra fallback: handle wrapped numeric types that slipped through
        # (e.g., Num). Use name-check to avoid hard import cycles.
        try:
            if type(other).__name__ == 'Num':
                if hasattr(other, 'get_value'):
                    other = other.get_value()
                elif hasattr(other, 'get'):
                    other = other.get()
                elif hasattr(other, 'value'):
                    other = other.value
                elif hasattr(other, 'data'):
                    other = other.data
        except Exception:
            pass

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
    
    