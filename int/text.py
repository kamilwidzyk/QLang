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
        
    def __get_other_value(self, other):
        while hasattr(other, 'get_value'):
            other = other.get_value()
        return other
        
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
    
    def __str__(self):
        return self.get()
    
    def __bool__(self):
        return len(self.get_value()) > 0
    
    def __add__(self, other):
        other = self.__get_other_value(other)
        # Text + str: concatenation
        # Text + int: convert int to str and concatenate
        # Text + float: convert float to str and concatenate
        # Text + list: convert list to str and concatenate
        return Expression(TYPE_STRING, str(self) + str(other))

    def __sub__(self, other):
        other = self.__get_other_value(other)
        # Text - str: remove all occurrences of every character in str from text
        if isinstance(other, str):
            result = self.get_value()
            for char in other:
                result = result.replace(char, "")
            return Expression(TYPE_STRING, result)
    
        raise TypeError("(Text) Unsupported type for subtraction with Text: " + str(type(other)))
    
    def __mul__(self, other):
        from .expression import Expression, TYPE_STRING

        other = self.__get_other_value(other)
        # Text * int: repeat text int times
        if isinstance(other, int):
            return Expression(TYPE_STRING, self.get_value() * other)
        if isinstance(other, float) and int(other) == other:
            return Expression(TYPE_STRING, self.get_value() * int(other))
        
        raise TypeError("(Text) Unsupported type for multiplication with Text: " + str(type(other)))
    
    def __is_item_extracted(self, item):
        if isinstance(item, list):
            return all(self.__is_item_extracted(subitem) for subitem in item)
        
        return not hasattr(item, 'get_value')

    def __get_value_of_list(self, other_list):
        # fix this: every item in a list can be a list or a multileyered classes with 'get_value' method(value has to be exreacted until no 'get_value' attr is left)

        if self.__is_item_extracted(other_list):
            return other_list
        
        if isinstance(other_list, list):
            return [self.__get_value_of_list(item) for item in other_list]
        if hasattr(other_list, 'get_value'):
            return self.__get_other_value(other_list)



    def __mod__(self, other):
        from .expression import Expression, TYPE_STRING
        other = self.__get_other_value(other)

        # Text % something: format text with tuple of something
        if isinstance(other, list):
            other_list = self.__get_value_of_list(other)
            return Expression(TYPE_STRING, self.get_value() % tuple(other_list))
        
        return Expression(TYPE_STRING, self.get_value() % other)
    
    def __truediv__(self, other):
        from .expression import Expression, TYPE_LIST, TYPE_STRING

        other = self.__get_other_value(other)

        # Text / str: split text by str and return list of substrings
        if isinstance(other, str):
            splits = [
                Expression(TYPE_STRING, substring) 
                for substring in self.get_value().split(other)]
            return Expression(TYPE_LIST, splits, shape=[len(splits)])

        raise TypeError("(Text) Unsupported type for division with Text: " + str(type(other)))
    
    def __floordiv__(self, other):
        raise TypeError("(Text) Unsupported division with Text: " + str(type(other)))
    
    def __pow__(self, other):
        raise TypeError("(Text) Unsupported exponentiation with Text: " + str(type(other)))
    
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
        # Text + str: concatenation
        # Text + int: convert int to str and concatenate
        # Text + float: convert float to str and concatenate
        # Text + list: convert list to str and concatenate
        return Expression(TYPE_STRING, str(other) + str(self))
    
    def __rsub__(self, other):
        other = self.__get_other_value(other)
        # str - Text: remove all occurrences of every character in str from text
        if isinstance(other, str):
            result = other
            for char in self.get_value():
                result = result.replace(char, "")
            return Expression(TYPE_STRING, result)
    
        raise TypeError("(Text) Unsupported type for subtraction with Text: " + str(type(other)))
    
    def __rmul__(self, other):
        raise TypeError("(Text) Unsupported type for multiplication with Text: " + str(type(other)))
    
    def __rtruediv__(self, other):
        other = self.__get_other_value(other)

        # str / Text: split text by str and return list of substrings
        if isinstance(other, str):
            return Expression(TYPE_LIST, [
                Expression(TYPE_STRING, substring) 
                for substring in other.split(self.get_value())])

        raise TypeError("(Text) Unsupported type for division with Text: " + str(type(other)))
    
    def __rfloordiv__(self, other):
        raise TypeError("(Text) Unsupported division with Text: " + str(type(other)))
    
    def __rmod__(self, other):
        other = self.__get_other_value(other)

        # something % Text: format text with tuple of something
        if isinstance(other, str):
            return Expression(TYPE_STRING, other % (self.get_value()))

        raise TypeError("(Text) Unsupported type for modulus with Text: " + str(type(other)))        
    def __rpow__(self, other):
        raise TypeError("(Text) Unsupported exponentiation with Text: " + str(type(other)))
    


        

        

