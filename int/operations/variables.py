# This file contains the implementation of the variable manimulation operations
# Do not make changes directly in the context, instead call the do_* 
# methods defined here to keep things consistent and to avoid code duplication

# Functions in this file should not raise any exceptions, all error handling should be done in the context!

# PRE DECREMENT
def do_variable_pre_decrement(place, variable): # --expr
    var_value = variable.get()
    var_value -= 1
    variable.set(var_value)
    place.scopes.set(variable.name, variable)
    return var_value


# POST DECREMENT
def do_variable_post_decrement(place, variable): # expr--
    var_name = variable.name
    orig_value = variable.get()
    variable.set(orig_value - 1)
    place.scopes.set(var_name, variable)
    return orig_value

# PRE INCREMENT
def do_variable_pre_increment(place, variable): # ++expr
    var_name = variable.name
    var_value = variable.get()
    var_value += 1
    variable.set(var_value)
    place.scopes.set(var_name, variable)
    return var_value

# POST INCREMENT
def do_variable_post_increment(place, variable): # expr++
    var_name = variable.name
    orig_value = variable.get()
    variable.set(orig_value + 1)
    place.scopes.set(var_name, variable)
    return orig_value

# ASSIGNMENT
def do_variable_assignment(place, variable, new_value): # var = expr
    var_name = variable.name
    variable.set(new_value)
    place.scopes.set(var_name, variable)
    return new_value