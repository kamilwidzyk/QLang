from .logger import log,WARNING

from .expression import *

class Text:
    """
    Represents a variable that can hold an text value. 
    """
    type: str = TYPE_TEXT
    name: str = None

    def __init__(self,initial_value: str = ""):
        self.value = initial_value

    def set(self,new_value: str|Expression):
        if isinstance(new_value, str):
            self.value = new_value
        elif isinstance(new_value, Expression):
            self.value = str(new_value.value)
        else:
            self.value = new_value
        

    def get(self) -> str:
        return self.value
    
