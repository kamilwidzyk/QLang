from int.exception.index_out_of_range import IndexOutOfRangeException
from int.exception.shape_mismatch import ShapeMismatchException

from .expression import *
from .logger import log, INTERNAL, FATAL, VARIABLE
from .obs import Obs
from .num import Num
from .text import Text
from .state import State
from .script_errors import ScriptErrors
from .exception.trying_to_modify_const import TryingToModifyConstException
from .index_types import SimpleIndex, RangeIndex, ListIndex

# Class enclosing every variable
# Supports making arrays with multiple dimensions
# Name is variable ID
# Type is the same type as in expression.py
# Variable is the variable class
# dimensions is a list of array dimensions, [0] for single value
# 
class Variable:
    def __init__(self, name: str, type: str, dimensions: list[int], index: list[int] = None, quantum_client=None, is_const: bool = False, initial_data=None, is_dynamic: bool = False):
        self.name = name
        self.type = type
        self.declared_type = type
        self.dimensions = dimensions
        self.is_dynamic = is_dynamic or (-100 in self.dimensions)
            
        if not self.is_dynamic and initial_data is not None and isinstance(initial_data, list) and self.dimensions == [0]:
            self.is_dynamic = True
        self.index = index # this is used when handler returns a Variable with access index
        self.quantum_client = quantum_client
        self.initial_value = None
        self.is_const = is_const
        if type in [TYPE_INT, TYPE_FLOAT, TYPE_BOOL, TYPE_STRING]:
            log(INTERNAL, FATAL, "Attempted to create instance of Variable with type of " + str(type))
            exit()
        if type == TYPE_OBS:
            self._create_array_of_obs()
        elif type == TYPE_NUM:
            self._create_array_of_num()
        elif type == TYPE_STATE:
            self._create_array_of_state()
        elif type == TYPE_TEXT:
            self._create_array_of_text()
        elif type == TYPE_ANY:
            self.data = None
        else:
            log(INTERNAL, FATAL, "Attempted to create instance of Variable with unknown type of " + str(type))
            exit()

        if initial_data is not None:
            if self.is_dynamic and isinstance(initial_data, list):
                self.data = ValueResolver.wrap_list(self.type, initial_data, self.quantum_client)
            else:
                self.data = initial_data
            self.is_list = isinstance(self.data, list)

    def _create_array_of(self, cls, dimensions, size=None):
        if not dimensions:
            if size is None:
                return cls()
            else:
                return cls(size=size)
            
        if isinstance(dimensions, int):
            dimensions = [dimensions]
        
        return [self._create_array_of(cls, dimensions[1:], size=size) for _ in range(dimensions[0])]
    

    def _create_array_of_obs(self):
        if self.dimensions != [0]:
            self.data = self._create_array_of(Obs, self.dimensions)
            self.is_list = True
        else:
            self.data = Obs()

    def _create_array_of_num(self):
        if self.dimensions != [0]:
            self.data = self._create_array_of(Num, self.dimensions)
            self.is_list = True
        else:
            self.data = Num()

    def _create_array_of_state(self):
        if self.dimensions != [0]:
            self.data = self._create_array_of_state_data(self.dimensions)
            self.is_list = True
        else:
            self.data = State(client=self.quantum_client)

    def _create_array_of_state_data(self, dimensions):
        if not dimensions:
            return State(client=self.quantum_client)
        return [self._create_array_of_state_data(dimensions[1:]) for _ in range(dimensions[0])]
    
    def _create_array_of_text(self):
        if self.dimensions != [0]:
            self.data = self._create_array_of(Text, self.dimensions)
            self.is_list = True
        else:
            self.data = Text("")
    
    def assign_values(self, data, values, is_dynamic=False):
        if isinstance(values, Expression):
            values = values.value
        if isinstance(data, list):
            if not isinstance(values, list):
                # code SM-1
                raise ShapeMismatchException(
                    pos=ScriptErrors.UNKNOWN_POSITION,
                    left_shape=len(data),
                    right_shape=0,
                    code="1"
                )
            
            if is_dynamic:
                for i in range(len(values)):
                    if i < len(data):
                        self.assign_values(data[i], values[i], is_dynamic)
                    else:
                        data.append(values[i])
            else:
                if len(data) != len(values) and not is_dynamic:
                    # code SM-1
                    raise ShapeMismatchException(
                        pos=ScriptErrors.UNKNOWN_POSITION,
                        left_shape=len(data),
                        right_shape=len(values),
                        code="1"
                    )
            
                for d, v in zip(data, values):
                    self.assign_values(d, v, is_dynamic)
        else:
            val = ValueResolver.extract_raw_value(values)
            data.set(val)

    def set(self, new_value: Expression, allow_const_init: bool = False, pos: ScriptErrors.Position = None):
        if self.is_const and not allow_const_init:
            raise TryingToModifyConstException(pos or ScriptErrors.Position(0, 0), self.name)

        if self.type == TYPE_ANY:
            from .type_inference import infer_type_from_value
            inferred_type = infer_type_from_value(new_value)
            self.type = inferred_type
            
            if hasattr(new_value, 'shape') and new_value.shape is not None:
                self.dimensions = [new_value.shape] if isinstance(new_value.shape, int) else new_value.shape
            self.is_list = isinstance(self.dimensions, list) and len(self.dimensions) > 0 and self.dimensions != [0]
            
            if inferred_type == TYPE_OBS:
                self._create_array_of_obs()
            elif inferred_type == TYPE_NUM:
                self._create_array_of_num()
            elif inferred_type == TYPE_STATE:
                self.data = None
            elif inferred_type == TYPE_TEXT:
                self._create_array_of_text()
            elif inferred_type == TYPE_ANY:
                self.data = new_value.value if isinstance(new_value, Expression) else new_value
                self.is_list = isinstance(self.data, list)
                return
            elif inferred_type == "Function":
                self.data = None

        if self.type == TYPE_STATE and self.declared_type != TYPE_ANY:
            raise TypeError("Quantum state cannot be assigned directly")

        if self.index is not None and len(self.index) > 0:
            target = self.data
            if len(self.index) > 1:
                target = self.get_data_at_index(self.data, self.index[:-1], pos)

            last_index = self.index[-1]

            # Range/List index assignment is not supported
            if isinstance(last_index, (RangeIndex, ListIndex)):
                raise TypeError("Cannot assign to a slice or index list")

            # Resolve SimpleIndex
            if isinstance(last_index, SimpleIndex):
                last_index = last_index.resolve(len(target) if hasattr(target, '__len__') else 0)
            
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
                        if isinstance(idx, SimpleIndex):
                            idx = idx.resolve(len(parent) if hasattr(parent, '__len__') else 0)
                        parent = parent[idx]
                    prev_idx = self.index[-2]
                    if isinstance(prev_idx, SimpleIndex):
                        prev_idx = prev_idx.resolve(len(parent) if hasattr(parent, '__len__') else 0)
                    parent[prev_idx] = target
                return
            
            if isinstance(target, list):
                element = target[last_index]
            else:
                element = target

            if isinstance(element, list):
                if new_value.type != TYPE_LIST:
                    log(VARIABLE, FATAL, "List expression required")
                    exit()
                self.assign_values(element, new_value.value, self.is_dynamic)
            else:
                val = ValueResolver.extract_raw_value(new_value)
                element.set(val)
            return

        if self.is_list:
            if isinstance(new_value, list):
                self.assign_values(self.data, new_value, self.is_dynamic)
                return

            if new_value.type != TYPE_LIST and not (new_value.shape is not None and new_value.shape != [0]):
                log(VARIABLE, FATAL, "List expression required")
                exit()

            if self.is_dynamic:
                self.data = ValueResolver.wrap_list(self.type, new_value.value, self.quantum_client)
                self.is_list = isinstance(self.data, list)
                return

            self.assign_values(self.data, new_value.value, self.is_dynamic)
        else:
            if isinstance(self.data, Text):
                # Setting entire string
                self.data.value = str(new_value) if new_value is not None else ""
            elif self.type == "Function":
                self.data = new_value.extract_raw_value() if hasattr(new_value, 'extract_raw_value') else Expression._extract_value_from(new_value)
            elif self.type == TYPE_STATE and self.declared_type == TYPE_ANY:
                self.data = ValueResolver.extract_raw_value(new_value)
            else:
                if self.is_dynamic and isinstance(new_value.value, list):
                    self.data = ValueResolver.wrap_list(self.type, new_value.value, self.quantum_client)
                    self.is_list = True
                    return
                val = ValueResolver.extract_raw_value(new_value)
                self.data.set(val)

    def _default_scalar_value(self):
        if self.type == TYPE_TEXT:
            return ""
        return 0

    def _default_list_value(self, dimensions=None):
        if dimensions is None:
            dimensions = self.dimensions


        if not dimensions or dimensions == [0]:
            return self._default_scalar_value()

        if isinstance(dimensions, int):
            dimensions = [dimensions]

        if len(dimensions) == 1:
            return [self._default_scalar_value() for _ in range(dimensions[0])]

        return [self._default_list_value(dimensions[1:]) for _ in range(dimensions[0])]

    def _wrap_expression(self, value):
        if isinstance(value, Expression):
            return value
        if isinstance(value, list):
            return Expression(TYPE_LIST, value, shape=self._list_shape(value))
        return Expression(self.type, value)

    def _get_initial_value_at_index(self, indexes):
        if self.initial_value is None:
            return None

        value = self.initial_value
        if isinstance(value, Expression):
            if value.type == TYPE_LIST:
                value = value.value
            else:
                if not indexes:
                    return value

        for idx in indexes:
            if isinstance(value, Expression) and value.type == TYPE_LIST:
                value = value.value
            value = value[idx]

        return self._wrap_expression(value)

    def reset(self, pos):
        if self.type == TYPE_STATE:
            raise TypeError("Quantum states cannot be reset directly")

        if self.index is not None and len(self.index) > 0:
            target = self.data
            if len(self.index) > 1:
                target = self.get_data_at_index(self.data, self.index[:-1], pos)

            last_index = self.index[-1]
            if isinstance(target, list):
                element = target[last_index]
            else:
                element = target[last_index]
            reset_value = self._get_initial_value_at_index(self.index)

            if isinstance(element, list):
                if reset_value is None:
                    reset_value = self._default_list_value(self._list_shape(element))
                if isinstance(reset_value, Expression) and reset_value.type == TYPE_LIST:
                    reset_value = reset_value.value
                self.assign_values(element, reset_value)
                return Expression(TYPE_LIST, element, shape=self._list_shape(element))

            if reset_value is None:
                reset_value = self._default_scalar_value()

            if isinstance(reset_value, Expression):
                reset_value = reset_value.get_value()
            element.set(reset_value)
            return self.get()

        if self.initial_value is not None:
            self.set(self.initial_value)
            return self.get()

        if self.is_list:
            default_value = self._default_list_value()
            self.set(Expression(TYPE_LIST, default_value, shape=self._list_shape(default_value)))
            return self.get()

        default_value = self._default_scalar_value()
        if self.type == TYPE_TEXT:
            self.set(Expression(TYPE_TEXT, default_value))
        else:
            self.set(Expression(self.type, default_value))
        return self.get()

    def __len__(self):
        if self.is_list:
            return len(self.data)
        if self.data is not None:
            return len(self.data)
        return 0
    
    def __getitem__(self, key):
        if self.is_list:
            return self.data[key]
        if self.data is not None:
            return self.data[key]
        raise TypeError("Variable is not subscriptable")
    
    def __setitem__(self, key, new_value):
        if self.is_list:
            self.data[key] = new_value
        elif self.data is not None:
            self.data[key] = new_value
        else:
            raise TypeError("Variable is not subscriptable")

    def get_data_at_index(self, data, indexes, pos):
        if not indexes:
            return data
            
        idx = indexes[0]
        length = len(data) if hasattr(data, '__len__') else 0
        
        if isinstance(idx, SimpleIndex):
            resolved = idx.resolve(length)
            if resolved >= len(data):
                # code IOR-1
                raise IndexOutOfRangeException(
                    pos=pos,
                    index_value=resolved,
                    length=len(data),
                    code="1"
                )
            return self.get_data_at_index(data[resolved], indexes[1:], pos)
            
        elif isinstance(idx, RangeIndex):
            start, end = idx.resolve(length)
            if isinstance(data, Text):
                sliced_data = data.value[start:end]
            else:
                sliced_data = data[start:end]
                
            if len(indexes) == 1:
                if isinstance(data, Text):
                    return Text(sliced_data)
                return sliced_data
            else:
                return [self.get_data_at_index(item, indexes[1:], pos) for item in sliced_data]
                
        elif isinstance(idx, ListIndex):
            resolved = idx.resolve(length)
            if len(indexes) == 1:
                if isinstance(data, Text):
                    return Text(''.join(data.value[i] for i in resolved))
                elif isinstance(data, str):
                    return ''.join(data[i] for i in resolved)
                return [data[i] for i in resolved]
            else:
                return [self.get_data_at_index(data[i], indexes[1:], pos) for i in resolved]
        else:
            # Legacy plain int index
            return self.get_data_at_index(data[idx], indexes[1:], pos)

    def _list_shape(self, data):
        if not isinstance(data, list):
            return []
        if not data:
            return [0]
        return [len(data)] + self._list_shape(data[0])

    def get(self, pos = None):
        if self.index is not None and len(self.index) > 0:
            data = self.get_data_at_index(self.data, self.index, ScriptErrors.UNKNOWN_POSITION if pos is None else pos)
            if isinstance(data, Text):
                return Expression(TYPE_STRING, data.value)
            if isinstance(data, list):
                return Expression(TYPE_LIST, data, shape=self._list_shape(data))
            if isinstance(data, bool):
                result = Expression(TYPE_BOOL, data)
                result.display_as_python_bool = True
                return result
            if isinstance(data, int):
                return Expression(TYPE_INT, data)
            if isinstance(data, float):
                return Expression(TYPE_FLOAT, data)
            if isinstance(data, str):
                return Expression(TYPE_STRING, data)
            return Expression(data.type, data, shape=len(data) if isinstance(data, list) else None)
        return Expression(self.type, self.data, shape=len(self.data) if self.is_list else None)
    
    def get_value(self):
        return ValueResolver.extract_raw_value(self.data)
        
    def _extract_value_from(value):
        return ValueResolver.extract_raw_value(value)

    def extract_value(self):
        return ValueResolver.extract_raw_value(self)

    def extract_raw_value(self):
        return ValueResolver.extract_raw_value(self)
        
    def __get_other_value(self, other):
        return ValueResolver.resolve_for_operation(other)

    
    def __lt__(self, other):
        other = self.__get_other_value(other)

        if isinstance(other, list):
            if self.type != TYPE_LIST:
                raise TypeError("Cannot compare non-list variable with list")
            return self.get_value() < other

        return Expression(TYPE_BOOL, self.get_value() < self.__get_other_value(other))
    
    def __le__(self, other):
        other = self.__get_other_value(other)

        if isinstance(other, list):
            if self.type != TYPE_LIST:
                raise TypeError("Cannot compare non-list variable with list")
            return self.get_value() < other


        return Expression(TYPE_BOOL, self.get_value() <= self.__get_other_value(other))
    
    def __gt__(self, other):
        other = self.__get_other_value(other)

        if isinstance(other, list):
            if self.type != TYPE_LIST:
                raise TypeError("Cannot compare non-list variable with list")
            return self.get_value() > other

        return Expression(TYPE_BOOL, self.get_value() > self.__get_other_value(other))
    
    def __ge__(self, other):
        other = self.__get_other_value(other)

        if isinstance(other, list):
            if self.type != TYPE_LIST:
                raise TypeError("Cannot compare non-list variable with list")
            return self.get_value() >= other

        return Expression(TYPE_BOOL, self.get_value() >= self.__get_other_value(other))

    def __eq__(self, other):
        other = self.__get_other_value(other)

        if isinstance(other, list):
            if self.type != TYPE_LIST:
                raise TypeError("Cannot compare non-list variable with list")
            return self.get_value() == other

        return Expression(TYPE_BOOL, self.get_value() == self.__get_other_value(other))

    def __ne__(self, other):
        other = self.__get_other_value(other)

        if isinstance(other, list):
            if self.type != TYPE_LIST:
                raise TypeError("Cannot compare non-list variable with list")
            return self.get_value() == other
        
        return Expression(TYPE_BOOL, self.get_value() != self.__get_other_value(other))


    



    
