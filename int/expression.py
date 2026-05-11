

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

def type_to_rank(type: str):
    if type == TYPE_BOOL:
        return 1
    if type == TYPE_INT:
        return 2
    if type == TYPE_FLOAT:
        return 3
    
def rank_to_type(type: int):
    if type == 1:
        return TYPE_BOOL
    if type == 2:
        return TYPE_INT
    if type == 3:
        return TYPE_FLOAT

def get_max_type(left, right):
    left_rank = type_to_rank(left.type)
    right_rank = type_to_rank(right.type)
    if left_rank is None:
        left_rank = 1
        if isinstance(left, int):
            left_rank = 2
        if isinstance(left, float):
            left_rank = 3
    if right_rank is None:
        right_rank = 1
        if isinstance(right, int):
            right_rank = 2
        if isinstance(right, float):
            right_rank = 3

    return rank_to_type(max(left_rank, right_rank))



class Expression:
    def __init__(self, type: str, value=None, variable=None, shape=None):
        self.type = type         # internal type
        self.value = value
        self.variable = variable
        self.shape = shape # when type is list -> this is the shape from outer to inner
