from __future__ import annotations
from typing import List

from .logger import log, OBS, WARNING, FATAL

from .expression import *
from .exception.modulo_over_zero import ModuloOverZeroException
from .exception.divide_by_zero import DivideByZeroException

class ObsRegister:
    """
    Represents observation register

    Bits are stored as:
        index 0 = Least Significant Bit
    """
    obs: List[Obs]
    size: int
    type: str = TYPE_OBS_REGISTER
    name: str = None

    def __init__(self, size: int):
        """
        Inits observation register with given size.
        Default initial value is 0s
        """
        self.obs = [Obs() for _ in range(size)]
        self.size = size

    def __getitem__(self, index) -> bool:
        """
        Returns bit state at given index
        """
        return self.obs[index].get()
    
    def __setitem__(self, index, value):
        """
        Sets bit at given index
        Value needs to be 0/1 or True/False
        """
        self.obs[index].set(value)

    def __len__(self):
        return self.size

    def max_val(self) -> int:
        return (2**self.size) - 1
    
    def set(self, new_value: int | Expression):
        """
        Converts the given number to binary and stores it
        Value must fit in the number is bits this register has

        Parameters:
            new_value (int): Value to set

        Raises:
            OverflowError: number is too large to store in this register
            ValueError: number is negative or not int
        """
        if isinstance(new_value, Expression):
            if new_value.type == TYPE_LIST:
                new_value = new_value.value
            else:
                new_value = new_value.get_value()

        if isinstance(new_value, list):
            if len(new_value) != self.size:
                raise ValueError(f"List length {len(new_value)} does not match register size {self.size}")

            for i, bit in enumerate(new_value):
                bit = ValueResolver.extract_raw_value(bit)
                if isinstance(bit, bool):
                    self[i] = int(bit)
                elif isinstance(bit, int):
                    if bit not in (0, 1):
                        raise ValueError("ObsRegister bits must be 0 or 1")
                    self[i] = bit
                else:
                    raise ValueError("ObsRegister list assignment requires boolean or integer bits")
            return

        if int(new_value) != new_value:
            raise ValueError("int is required")
        if new_value < 0:
            raise ValueError("Value needs to be >= 0")

        if(new_value > self.max_val()):
            raise OverflowError(f"Value {new_value} will not fit into {self.size} bits")

        bits = [((new_value >> i) & 1) == 1 for i in range(self.size)]
        for i in range(self.size):
            self[i] = bits[i]

    def get(self) -> int:
        """
        Returns value of the register represented as int
        """
        result = 0
        for i in range(self.size):
            if self[i]:
                result |= 1 << i
        return result

    def get_value(self) -> int:
        return self.get()
    
    def __get_other_value(self, other):
        return ValueResolver.resolve_for_operation(other)

    def __str__(self):
        return str(self.get_value())

    def __bool__(self):
        return self.get_value() != 0
        
    def __lt__(self, other):
        return Expression(TYPE_BOOL, self.get_value() < self.__get_other_value(other))
    
    def __le__(self, other):
        return Expression(TYPE_BOOL, self.get_value() <= self.__get_other_value(other))
    
    def __gt__(self, other):
        return Expression(TYPE_BOOL, self.get_value() > self.__get_other_value(other))
    
    def __ge__(self, other):
        return Expression(TYPE_BOOL, self.get_value() >= self.__get_other_value(other))
    
    def __eq__(self, value):
        return Expression(TYPE_BOOL, self.get_value() == self.__get_other_value(value))
    
    def __ne__(self, value):
        return Expression(TYPE_BOOL, self.get_value() != self.__get_other_value(value))
    
    def __add__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value() + other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() + other)
        if isinstance(other, str): # string concatenation
            return Expression(TYPE_STRING, str(self) + other)
        
        raise TypeError("(ObsRegister) Unsupported type for addition with ObsRegister: " + str(type(other)))

    def __sub__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value() - other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() - other)
        
        raise TypeError("(ObsRegister) Unsupported type for subtraction with ObsRegister: " + str(type(other)))
    
    def __mul__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value() * other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() * other)
        
        raise TypeError("(ObsRegister) Unsupported type for multiplication with ObsRegister: " + str(type(other)))
    
    def __mod__(self, other):
        other = self.__get_other_value(other)
        if other == 0:
            raise ModuloOverZeroException(None)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value() % other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() % other)
        
        raise TypeError("(ObsRegister) Unsupported type for modulo with ObsRegister: " + str(type(other)))

    def __truediv__(self, other):
        other = self.__get_other_value(other)
        if other == 0:
            raise DivideByZeroException(None)
        if isinstance(other, int):
            return Expression(TYPE_FLOAT, self.get_value() / other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() / other)
        
        raise TypeError("(ObsRegister) Unsupported type for division with ObsRegister: " + str(type(other)))

    def __floordiv__(self, other):
        other = self.__get_other_value(other)
        if other == 0:
            raise DivideByZeroException(None)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value() // other)
        if isinstance(other, float):
            return Expression(TYPE_INT, self.get_value() // other)
        
        raise TypeError("(ObsRegister) Unsupported type for floor division with ObsRegister: " + str(type(other)))

    def __pow__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value() ** other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value() ** other)
        
        raise TypeError("(ObsRegister) Unsupported type for exponentiation with ObsRegister: " + str(type(other)))
    
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
        return other.__add__(self)
    
    def __rsub__(self, other):
        return other.__sub__(self)
    
    def __rmul__(self, other):
        return other.__mul__(self)
    
    def __rmod__(self, other):
        return other.__mod__(self)
    
    def __rtruediv__(self, other):
        return other.__truediv__(self)
    
    def __rfloordiv__(self, other):
        return other.__floordiv__(self)
    
    def __rpow__(self, other):
        return other.__pow__(self)
    




class Obs:
    """
    Represents one classical bit
    """
    state: int = 0 
    type: str = TYPE_OBS
    name: str = None

    def set(self, new_value: int | bool | Expression):
        """
        Sets the new value 
        If the value is not valid, warning is logger and value is ignored

        Parameters:
            new_value (int|bool|Expression): Value to set, 0/1 or True/False
        """
        if isinstance(new_value, Expression):
            if new_value.type == TYPE_BOOL:
                if new_value.value == True:
                    self.state = 1
                else:
                    self.state = 0
            elif new_value.type in [TYPE_INT, TYPE_FLOAT]:
                if new_value.value > 0:
                    self.state = 1
                else:
                    self.state = 0
            elif new_value.type == TYPE_STRING:
                if len(new_value.value) > 0:
                    self.state = 1
                else:
                    self.state = 0
            elif new_value.type in [TYPE_NUM, TYPE_OBS]:
                if new_value.get() > 0:
                    self.state = 1
                else:
                    self.state = 0
            else:
                log(OBS, FATAL, "Attempted to set value " + str(new_value) + "as obs value")
                exit()
        elif new_value == 0 or new_value == False:
            self.state = 0
        elif new_value == 1 or new_value == True:
            self.state = 1
        else:
            log(OBS, FATAL, "There was an attempt at setting " + str(new_value) + " as obs value")
            exit()

    def __len__(self):
        return 1
    
    def __getitem__(self, key):
        raise TypeError("Obs object is not subscriptable")

    def get(self) -> bool:
        """
        Gets the value

        Returns:
            True: state is 1
            False: otherwise
        """
        return self.state == 1

    def get_value(self) -> bool:
        return self.get()
    
    def get_value_as_int(self) -> int:
        return 1 if self.get() else 0
    
    def max_val(self) -> int:
        return 1
    
    def __get_other_value(self, other):
        return ValueResolver.resolve_for_operation(other)
        
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

    def __str__(self):
        return 'T' if self.get_value() else 'F'
    
    def __bool__(self):
        return self.get_value()
    
    def __add__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value_as_int() + other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value_as_int() + other)
        if isinstance(other, str): # string concatenation
            return Expression(TYPE_STRING, str(self) + other)
        
        raise TypeError("(Obs) Unsupported type for addition with Obs: " + str(type(other)))
    
    def __sub__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value_as_int() - other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value_as_int() - other)
        
        raise TypeError("(Obs) Unsupported type for subtraction with Obs: " + str(type(other)))
    
    def __mul__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value_as_int() * other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value_as_int() * other)
        
        raise TypeError("(Obs) Unsupported type for multiplication with Obs: " + str(type(other)))
    
    def __mod__(self, other):
        other = self.__get_other_value(other)
        if other == 0:
            raise ModuloOverZeroException(None)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value_as_int() % other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value_as_int() % other)
        
        raise TypeError("(Obs) Unsupported type for modulo with Obs: " + str(type(other)))

    def __truediv__(self, other):
        other = self.__get_other_value(other)
        if other == 0:
            raise DivideByZeroException(None)
        if isinstance(other, int):
            return Expression(TYPE_FLOAT, self.get_value_as_int() / other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value_as_int() / other)
        
        raise TypeError("(Obs) Unsupported type for division with Obs: " + str(type(other)))
    
    def __floordiv__(self, other):
        other = self.__get_other_value(other)
        if other == 0:
            raise DivideByZeroException(None)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value_as_int() // other)
        if isinstance(other, float):
            return Expression(TYPE_INT, self.get_value_as_int() // other)
        
        raise TypeError("(Obs) Unsupported type for floor division with Obs: " + str(type(other)))
    
    def __pow__(self, other):
        other = self.__get_other_value(other)
        if isinstance(other, int):
            return Expression(TYPE_INT, self.get_value_as_int() ** other)
        if isinstance(other, float):
            return Expression(TYPE_FLOAT, self.get_value_as_int() ** other)
        
        raise TypeError("(Obs) Unsupported type for exponentiation with Obs: " + str(type(other)))
    
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
        return other.__add__(self)
    
    def __rsub__(self, other):
        return other.__sub__(self)
    
    def __rmul__(self, other):
        return other.__mul__(self)
    
    def __rmod__(self, other):
        return other.__mod__(self)
    
    def __rtruediv__(self, other):
        return other.__truediv__(self)
    
    def __rfloordiv__(self, other):
        return other.__floordiv__(self)
    
    def __rpow__(self, other):
        return other.__pow__(self)
    
    
    
