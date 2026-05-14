from .logger import log,WARNING

from .expression import *

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
    
