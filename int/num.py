from .logger import log, WARNING

from .expression import *
from .exception.modulo_over_zero import ModuloOverZeroException
from .exception.divide_by_zero import DivideByZeroException

class Num:
    """
    Represents a variable that can hold an numerical value. 
    It is used to store the value of variables in the program. 
    It is not limited to a specific number of bits, 
    but it can be used to represent any value.
    """
    type: str = TYPE_NUM
    name: str = None
    is_float: bool = False
    def __init__(self,initial_value: float = 0.0):
        self.value = float(initial_value)

    def set(self,new_value: float|Expression|int):
        if isinstance(new_value, float):
            self.is_float = True
            self.value = new_value
        elif isinstance(new_value, Expression):
            if new_value.type == TYPE_FLOAT:
                self.is_float = True
            elif new_value.type == TYPE_NUM:
                self.is_float = new_value.is_float
            elif new_value.type in TYPE_INT:
                self.is_float = False
            val = new_value.value
            while hasattr(val, 'get_value'):
                val = val.get_value()
            self.value = val
        elif type(new_value).__name__ == 'Num':
            self.is_float = new_value.is_float
            self.value = new_value.value
        else:
            self.is_float = False
            self.value = new_value

    def __len__(self):
        return 1
    
    def __getitem__(self, key):
        raise TypeError("Num object is not subscriptable")
        

    def get(self) -> float:
        if self.is_float:
            return Expression(TYPE_FLOAT, self.value)
        else:
            return Expression(TYPE_INT, self.value)
        
    def get_value(self) -> float:
        return self.get().value
    
    def __get_other_value(self, other):
        while hasattr(other, 'get_value'):
            other = other.get_value()
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
    
    def __extract_value(self, value):
        while hasattr(value, 'get_value'):
            value = value.get_value()
        return value

    def __list_to_str(self, lst):
        lst = self.__extract_value(lst)
        if isinstance(lst, list):
            return "[" + ", ".join(self.__list_to_str(x) for x in lst) + "]"
        else:
            if isinstance(lst, Expression):
                return str(lst.get_value())
            return str(lst)
        


    def __str__(self):
        val = self.get_value()
        if isinstance(val, list):
            return self.__list_to_str(val)
        return str(val)


    def __bool__(self):
        return self.get_value() != 0

    def __add__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, self.get_value() + other)
            return Expression(TYPE_INT, self.get_value() + other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() + other)
        if isinstance(other, str): # string concatenation
            return Expression(TYPE_STRING, str(self) + other)
        
        raise TypeError("(Num) Unsupported type for addition: " + str(type(other).__name__))
    
    def __sub__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, self.get_value() - other)
            return Expression(TYPE_INT, self.get_value() - other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() - other)
        # num - string: type error
        raise TypeError("(Num) Unsupported type for subtraction: " + str(type(other).__name__))            

    def __mul__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, self.get_value() * other)
            return Expression(TYPE_INT, self.get_value() * other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() * other)

        raise TypeError("(Num) Unsupported type for multiplication: " + str(type(other).__name__))

    
    def __mod__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if other == 0:
                raise ModuloOverZeroException(None)
            if self.is_float:
                return Expression(TYPE_FLOAT, self.get_value() % other)
            return Expression(TYPE_INT, self.get_value() % other)
        if isinstance(other, float):
            if other == 0.0:
                raise ModuloOverZeroException(None)
            return Expression(TYPE_FLOAT, self.get_value() % other)
        # num % string: type error
        raise TypeError("(Num) Unsupported type for modulo: " + str(type(other).__name__))
    
    def __truediv__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if other == 0:
                raise DivideByZeroException(None)
            return Expression(TYPE_FLOAT, self.get_value() / other)
        if isinstance(other, float):
            if other == 0.0:
                raise DivideByZeroException(None)
            return Expression(TYPE_FLOAT, self.get_value() / other)
        # num / string: type error
        raise TypeError("(Num) Unsupported type for division: " + str(type(other).__name__))
    
    def __floordiv__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if other == 0:
                raise DivideByZeroException(None)
            return Expression(TYPE_INT, self.get_value() // other)
        if isinstance(other, float):
            if other == 0.0:
                raise DivideByZeroException(None)
            return Expression(TYPE_INT, self.get_value() // other)
        # num // string: type error
        raise TypeError("(Num) Unsupported type for floor division: " + str(type(other).__name__))

    def __pow__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, self.get_value() ** other)
            return Expression(TYPE_INT, self.get_value() ** other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() ** other)
        # num ** string: type error
        raise TypeError("(Num) Unsupported type for exponentiation: " + str(type(other).__name__))

    def __iadd__(self, other):
        self.set(self.__add__(other))
        return self
    
    def __isub__(self, other):
        self.set(self.__sub__(other))
        return self

    def __imul__(self, other):
        self.set(self.__mul__(other))
        return self

    def __imod__(self, other):
        self.set(self.__mod__(other))
        return self
    
    def __itruediv__(self, other):
        self.set(self.__truediv__(other))
        return self
    
    def __ifloordiv__(self, other):
        self.set(self.__floordiv__(other))
        return self
    
    def __ipow__(self, other):
        self.set(self.__pow__(other))
        return self

    def __radd__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, other + self.get_value())
            return Expression(TYPE_INT, other + self.get_value())
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, other + self.get_value())
        if isinstance(other, str): # string concatenation
            return Expression(TYPE_STRING, other + str(self))
        
        raise TypeError("(Num) Unsupported type for addition: " + str(type(other).__name__))
    
    def __rsub__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, other - self.get_value())
            return Expression(TYPE_INT, other - self.get_value())
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, other - self.get_value())
        # string - num: type error
        raise TypeError("(Num) Unsupported type for subtraction: " + str(type(other).__name__))

    def __rmul__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, other * self.get_value())
            return Expression(TYPE_INT, other * self.get_value())
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, other * self.get_value())
        # string * num: type error
        raise TypeError("(Num) Unsupported type for multiplication: " + str(type(other).__name__))

    def __rtruediv__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, other / self.get_value())
            return Expression(TYPE_INT, other / self.get_value())
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, other / self.get_value())
        # string / num: type error
        raise TypeError("(Num) Unsupported type for true division: " + str(type(other).__name__))

    def __rfloordiv__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, other // self.get_value())
            return Expression(TYPE_INT, other // self.get_value())
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, other // self.get_value())
        # string // num: type error
        raise TypeError("(Num) Unsupported type for floor division: " + str(type(other).__name__))

    def __rmod__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, other % self.get_value())
            return Expression(TYPE_INT, other % self.get_value())
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, other % self.get_value())
        # string % num: type error
        raise TypeError("(Num) Unsupported type for modulo: " + str(type(other).__name__))

    def __rpow__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            if self.is_float:
                return Expression(TYPE_FLOAT, other ** self.get_value())
            return Expression(TYPE_INT, other ** self.get_value())
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, other ** self.get_value())
        # string ** num: type error
        raise TypeError("(Num) Unsupported type for power: " + str(type(other).__name__))

    
    


