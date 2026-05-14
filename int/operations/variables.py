# This file contains the implementation of the variable manimulation operations
# Do not make changes directly in the context, instead call the do_* 
# methods defined here to keep things consistent and to avoid code duplication

# Functions in this file should not raise any exceptions, all error handling should be done in the context!

from ..expression import Expression

def extract_variable_value(variable):
    while hasattr(variable, 'get_value'):
        variable = variable.get_value()
    return variable

# PRE DECREMENT
def do_variable_pre_decrement(place, variable): # --expr
    var_value = extract_variable_value(variable)
    var_type = variable.get().type
    var_value -= 1
    variable.set(Expression(var_type, var_value))
    place.scopes.set(variable.name, variable)
    return Expression(var_type, var_value)


# POST DECREMENT
def do_variable_post_decrement(place, variable): # expr--
    var_name = variable.name
    orig_value = extract_variable_value(variable)
    orig_type = variable.get().type
    variable.set(Expression(orig_type, orig_value - 1))
    place.scopes.set(var_name, variable)
    return Expression(orig_type, orig_value)

# PRE INCREMENT
def do_variable_pre_increment(place, variable): # ++expr
    var_name = variable.name
    var_value = extract_variable_value(variable)
    var_type = variable.get().type
    var_value += 1
    variable.set(Expression(var_type, var_value))
    place.scopes.set(var_name, variable)
    return Expression(var_type, var_value)

# POST INCREMENT
def do_variable_post_increment(place, variable): # expr++
    var_name = variable.name
    orig_value = extract_variable_value(variable)
    orig_type = variable.get().type
    variable.set(Expression(orig_type, orig_value + 1))
    place.scopes.set(var_name, variable)
    return Expression(orig_type, orig_value)

# ASSIGNMENT
def do_variable_assignment(place, variable, new_value): # var = expr
    var_name = variable.name
    var_type = variable.type
    variable.set(new_value)
    place.scopes.set(var_name, variable)
    print("DO variable assignment", var_name, var_type)
    return Expression(var_type, new_value.value)