from __future__ import annotations
from typing import List

from .logger import log, OBS, WARNING, FATAL

from .expression import *

class ObsRegister:
    """
    Represents observation register

    Bits are stored as:
        index 0 = Most Significant Bit
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
    
    def set(self, new_value: int):
        """
        Converts the given number to binary and stores it
        Value must fit in the number is bits this register has

        Parameters:
            new_value (int): Value to set

        Raises:
            OverflowError: number is too large to store in this register
            ValueError: number is negative or not int
        """


        if int(new_value) != new_value:
            raise ValueError("int is required")
        if new_value < 0:
            raise ValueError("Value needs to be >= 0")

        if(new_value > self.max_val()):
            raise OverflowError(f"Value {new_value} will not fit into {self.size} bits")

        bits = [(new_value >> i) & 1 == 1 for i in reversed(range(self.size))]
        for i in range(self.size):
            self[i] = bits[i]

    def get(self) -> int:
        """
        Returns value of the register represented as int
        """
        result = 0
        for i in range(self.size):
            result = (result << 1) | self[i]
        return result

    def get_value(self) -> int:
        return self.get()
    
    

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
    
    def max_val(self) -> int:
        return 1