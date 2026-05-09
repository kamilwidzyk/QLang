from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister
from ...num import Num

import random
from ...logger import log, DEBUG, IN_OUT

from ...expression import *
from ...variable import Variable
from ...function import Function
if TYPE_CHECKING:
    from place import Place

def handle_io_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # first child can be 'print', 'println' or 'input', 'debug'

    def convert_value(value):
        if isinstance(value, Num):
            return value.get().value
        if isinstance(value, Expression):
            if value.type == TYPE_INT:
                return int(value.value)
            elif value.type == TYPE_FLOAT:
                return float(value.value)
            elif value.type == TYPE_BOOL:
                return 'T' if value.value else 'F'
            elif value.type == TYPE_OBS:
                return 'T' if value.get() else 'F'
            elif value.type == TYPE_OBS_REGISTER:
                return value.get()
            elif value.type == TYPE_NUM:
                return value.value
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            def map_list(data):
                if isinstance(data, list):
                    return [map_list(x) for x in data]
                else:
                    return convert_value(data)
            return map_list(value)
        return str(value)
    
    def handle_print(add_newline=False):
        nonlocal block

        # no expr -> print a newline if enabled
        if not block.expr():
            if add_newline:
                self.console.write("\n")
            return
        
        # Get all expressions
        exprs = []
        for i in range(len(block.expr())):
            exprs.append(self.handle_block(block.expr(i), block))

        # If first is string with %, treat as printf
        if len(exprs) > 0 and isinstance(exprs[0], str) and '%' in exprs[0]:
            format_str = exprs[0]
            args = exprs[1:]
            # Convert args to values
            converted_args = []
            for arg in args:
                converted_args.append(convert_value(arg))
            try:
                print_text = format_str % tuple(converted_args)
            except Exception as e:
                self.script_errors.showError(
                    pos=pos,
                    error_type="RUNTIME ERROR",
                    title="Printf format error",
                    msg=str(e)
                )
                exit()
        else:
            # Print all args separated by space
            print_parts = []
            for expr in exprs:
                print_parts.append(str(convert_value(expr)))
            print_text = ' '.join(print_parts)

        # add a newline if the command was println
        if add_newline:
            self.console.write(print_text + "\n")
        else:
            self.console.write(print_text)

    def handle_input():
        nonlocal block
        # INPUT '(' ID ('[' expr ']')? (',' format)? (',' constraint)? ')'

        if self.console.test_mode:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos,
                error_type="RUNTIME ERROR",
                title="Input not supported in TEST MODE",
                msg="This program asks for input(), but TEST_MODE does not provide interactive console input.",
            )
            exit()
        
        # variable name(ID) is required
        var_name = block.ID().getText()

        # variable index is optional
        index = None
        if block.expr():
            index = self.handle_block(block.expr(), block)

        # format is optional(BIN, HEX)
        format = None
        if block.format_():
            format = self.handle_block(block.format_(), block)
        
        # constraint is optional(value range: min..max or range(min, max))
        constraint_min = None
        constraint_max = None
        if block.constraint():
            constraint_min, constraint_max = self.handle_block(block.constraint(), block)

        # check if variable exists
        if not self.scopes.exists(var_name):
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="You Error", 
                msg="No variable. You forgot to make it, input lost to the void."
            )
            exit()

        variable: Obs | ObsRegister | Num = self.scopes.get(var_name)

        # check if the variable is of correct type
        if variable.type not in ["Obs", "ObsRegister", "Num"]:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="Type Error", 
                msg="Not how this works. I need an observation(s)."
            )
            exit()

        # check if variable can be indexed
        if index is not None and variable.type == "Obs":
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="Index Error", 
                msg="You are looking too deep into something that can only be 0 or 1."
            )
            exit()
        

        # update to given constraint if possible
        if constraint_min is not None:
            min_val = constraint_min
        if constraint_max is not None:
            max_val = constraint_max

        if variable.type == "Num":
            max_val = float('inf') if constraint_max is None else max_val
            min_val = float('-inf') if constraint_min is None else min_val
        else:
            max_val = variable.data.max_val() if constraint_max is None else max_val
            min_val = 0 if constraint_min is None else min_val
        value = None

        # Try forever to get a value from the user
        while True:
            # read a line from the console window(not the terminal)
            log(IN_OUT, DEBUG, f"{self.name}: Waiting for console input...")
            console_in = self.console.read("")
            log(IN_OUT, DEBUG, f"{self.name}: Console input: {console_in}")

            if console_in is None:
                continue
            
            # check formatting
            if format is not None:
                if format == "BIN" and console_in.startswith("0b"):
                    try:
                        value = int(console_in, 2)
                        if value >= min_val and value <= max_val:
                            break # valid value received -> end of loop
                    except:
                        pass # not a number
                elif format == "HEX" and console_in.startswith("0x"):
                    try:
                        value = int(console_in, 16)
                        if value >= min_val and value <= max_val:
                            break # valid value received -> end of loop
                    except:
                        pass # not a number
            else:
                try:
                    if variable.type == "Num":
                        value = float(console_in)
                    else:
                        value = int(console_in)

                    if value >= min_val and value <= max_val:
                        break # valid value received -> end of loop
                except:
                    pass # not a number
            
            # user input is invalid, show a message what is expected on the input
            format_str = {None: "decimal", "BIN": "binary", "HEX": "hexadecimal"}[format]
            invalid = [
                "That's not gonna work.", "What even is that input.", "Try again, but correctly.",
                "I can't work with that.", "Rejected.", "Input denied.", "Nice try, but no.",
                "Be serious.", "No idea what that is.", "Nah.", "Hard no.", "Rejected in 0ms.",
                "Absolutely not.", "Fail.", "Not today.", "Not a chance.", "Try harder.",
                "LOL, no.", "Wrong.", "No.", "Nope.", "That's a no.", "Do better.",
                "Denied.", "I can't let that slide."
            ]

            self.console.write(f"[{random.sample(invalid, 1)[0]} I need a number in range {min_val}-{max_val} in {format_str} format] ")

        # set value to the variable and update variable in the scope
        value_type = TYPE_FLOAT if variable.type == "Num" else TYPE_INT
        variable.set(Expression(value_type, value))
        self.scopes.set(var_name, variable)

    def handle_debug():
        nonlocal block
        
        # DEBUG '(' ID ('[' expr ']')* ')'
        var_name = block.ID().getText()
        
        if not self.scopes.exists(var_name):
            self.script_errors.showError(
                pos=pos,
                error_type="RUNTIME ERROR",
                title="Debug Error",
                msg=f"Variable '{var_name}' not found."
            )
            exit()
        
        variable = self.scopes.get(var_name)
        
        index = []
        for expr in block.expr():
            expr_value = self.handle_block(expr, block)
            if hasattr(expr_value, 'value'):
                index.append(expr_value.value)
            else:
                index.append(expr_value)
        
        debug_info = f"DEBUG {var_name}"
        if len(index) > 0:
            for i in index:
                debug_info += f"[{i}]"
        debug_info += ": "

        # TODO: make the debug output more structured, not just everything in one line
        # make it multiline and more readable

        def format_variable_value(var):
            if isinstance(var, Num):
                return f"Num(value={var.value}, is_float={var.is_float})"
            elif isinstance(var, Obs):
                return f"Obs(value={var.get()})"
            elif isinstance(var, ObsRegister):
                return f"ObsRegister(value={var.get()})"
            elif isinstance(var, list):
                return f"[{', '.join(format_variable_value(x) for x in var)}]"
            else:
                return str(var)
        
        if isinstance(variable, Variable):
            debug_info += f"Variable(type={variable.type}, dimensions={variable.dimensions}"
            if len(index) == 0:
                if variable.data is None:
                    debug_info += ", data=None"
                else:
                    debug_info += f", data={format_variable_value(variable.data)}"
                debug_info += ")"
            else:
                try:
                    if variable.is_list:
                        indexed_value = variable.data
                        for idx in index if isinstance(index, list) else [index]:
                            indexed_value = indexed_value[idx]
                        debug_info += f", indexed_value={format_variable_value(indexed_value)})"
                    else:
                        debug_info += ", not a list, cannot index)"
                except Exception as e:
                    debug_info += f", error accessing index: {e})"
        elif isinstance(variable, Function):
            debug_info += f"Function(param_count={len(variable.params)}"
            
            for p in variable.params or []:
                debug_info += f", param_{p.name}={{name: {p.name}, type: {p.type}, size: {p.size}, initial_value: {format_variable_value(p.initial_value)}}}"
            
            debug_info += f", body_length={len(variable.body)}"
            # position in code
            debug_info += f", pos={variable.pos})"


            
        else:
            debug_info += f"Other(type={type(variable)}, value={variable})"
        
        self.console.write(debug_info + "\n")



    stmt_type = block.getChild(0).getText()

    if stmt_type == "print":
        handle_print()
    elif stmt_type == "println":
        handle_print(add_newline=True)
    elif stmt_type == "debug":
        handle_debug()

    elif stmt_type == "input":
        handle_input()
        
