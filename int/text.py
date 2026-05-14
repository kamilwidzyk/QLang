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
        
    def __len__(self):
        return len(self.value)
    
    def __getitem__(self, key):
        return self.value[key]
    
    def __setitem__(self, key, new_value):
        self.value[key] = new_value

    def get_value(self) -> str:
        return self.get()

    def get(self) -> str:
        return self.value
    
