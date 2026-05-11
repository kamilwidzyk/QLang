

from .expression import *
from .logger import log, INTERNAL, FATAL, VARIABLE
from .obs import Obs, ObsRegister
from .num import Num
from .text import Text

# Class enclosing every variable
# Supports making arrays with multiple dimensions
# Name is variable ID
# Type is the same type as in expression.py
# Variable is the variable class
# dimensions is a list of array dimensions, [0] for single value
# 
class Variable:
    def __init__(self, name: str, type: str, dimensions: list[int], index: list[int] = None):
        self.name = name
        self.type = type
        self.dimensions = dimensions
        self.data = None
        self.is_list = False
        self.index = index # this is used when handler returns a Variable with access index
        if type in [TYPE_INT, TYPE_FLOAT, TYPE_BOOL, TYPE_STRING]:
            log(INTERNAL, FATAL, "Attempted to create instance of Variable with type of " + str(type))
            exit()
        if type == TYPE_OBS:
            self._create_array_of_obs()
        elif type == TYPE_OBS_REGISTER:
            self._create_array_of_obs_register()
        elif type == TYPE_NUM:
            self._create_array_of_num()
        elif type == TYPE_STATE:
            self._create_array_of_state()
        elif type == TYPE_STATE_REGISTER:
            self._create_array_of_state_register()
        elif type == TYPE_TEXT:
            self._create_array_of_text()
        else:
            log(INTERNAL, FATAL, "Attempted to create instance of Variable with unknown type of " + str(type))
            exit()

    def _create_array_of(self, cls, dimensions, size=None):
        if not dimensions:
            if size is None:
                return cls()
            else:
                return cls(size=size)
        
        return [self._create_array_of(cls, dimensions[1:]) for _ in range(dimensions[0])]
    

    def _create_array_of_obs(self):
        if self.dimensions != [0]:
            self.data = self._create_array_of(Obs, self.dimensions)
            self.is_list = True
        else:
            self.data = Obs()

    def _create_array_of_obs_register(self):
        if len(self.dimensions) == 1:
            self.data = ObsRegister(size=self.dimensions[0])
        else:
            register_size = self.dimensions[-1]
            self.data = self._create_array_of(ObsRegister, self.dimensions[:-1], register_size)
            self.is_list = True

    def _create_array_of_num(self):
        if self.dimensions != [0]:
            self.data = self._create_array_of(Num, self.dimensions)
            self.is_list = True
        else:
            self.data = Num()

    def _create_array_of_state():
        raise NotImplementedError()

    def _create_array_of_state_register():
        raise NotImplementedError()
    
    def _create_array_of_text(self):
        if self.dimensions != [0]:
            self.data = self._create_array_of(Text, self.dimensions)
            self.is_list = True
        else:
            self.data = Text("")
    
    def assign_values(self, data, values):
        print("Assigning values to variable", self.name)
        print("Data before assignment: ", data)
        print("Values to assign: ", values)
        if isinstance(values, Expression):
            values = values.value
        print("Data: ", data)
        print()
        print("Values: ", values)
        if isinstance(data, list):
            if not isinstance(values, list):
                log(VARIABLE, FATAL, "Shape mismatch: expected list")
                exit()
            if len(data) != len(values):
                log(VARIABLE, FATAL, "Shape mismatch: different lengths")
                exit()
        
            for d, v in zip(data, values):
                self.assign_values(d, v)
        else:
            data.set(values)

    def set(self, new_value: Expression):
        if self.index is not None and len(self.index) > 0:
            target = self.data
            if len(self.index) > 1:
                target = self.get_data_at_index(self.data, self.index[:-1])

            last_index = self.index[-1]
            
            if isinstance(target, Text):
                # Handle string indexing
                if isinstance(new_value.value, Text) and len(new_value.value) == 1:
                    char = new_value.value
                else:
                    char = str(new_value.value)[0] if new_value.value else '\0'
                
                # Expand string if necessary
                while len(target.value) <= last_index:
                    target.value += '\0'
                
                # Replace character
                target.value = target.value[:last_index] + char + target.value[last_index+1:]
                
                # Update the data
                if len(self.index) == 1:
                    self.data = target
                else:
                    # Need to set back in the parent structure
                    parent = self.data
                    for idx in self.index[:-2]:
                        parent = parent[idx]
                    parent[self.index[-2]] = target
                return
            
            element = target[last_index] if isinstance(target, list) else target

            if isinstance(element, list):
                if new_value.type != TYPE_LIST:
                    log(VARIABLE, FATAL, "List expression required")
                    exit()
                self.assign_values(element, new_value.value)
            else:
                element.set(new_value.value)
            return

        if self.is_list:
            if new_value.type != TYPE_LIST:
                log(VARIABLE, FATAL, "List expression required")
                exit()
            self.assign_values(self.data, new_value.value)
        else:
            if isinstance(self.data, Text):
                # Setting entire string
                self.data.value = str(new_value.value) if new_value.value is not None else ""
            else:
                self.data.set(new_value.value)

    def get_data_at_index(self, data, indexes):
        for idx in indexes:
            if isinstance(data, Text):
                data.value = data.value[idx]
        return data

    def get(self):
        if self.index is not None:
            return self.get_data_at_index(self.data, self.index)
        return self.data



    



    
