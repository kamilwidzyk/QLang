from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister
from ...num import Num

import random
from ...logger import log, DEBUG, IN_OUT

from ...expression import *
from ...variable import Variable
if TYPE_CHECKING:
    from place import Place

def handle_io_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # first child can be 'print', 'println' or 'input', 'debug'(TODO)

    # PRINT
    # print()                -> print nothing
    # print(<val>)           -> print decimal
    # print(<val>, <format>) -> print bin/hex 
    # <val> = VarExprContext
    # (same for println)

    # 1. Terminal 'print'
    # 2. Terminal '('
    # 3. VarExprContext or StrExprContext
    # If format defined:
    #   4a. Terminal ','
    #   4b. block 'format' HEX/BIN 
    # 5. Terminal ')'

    # Combinations
    #       (CHILD INDEX)
    # (0) (1) (2)  (3)  (4)
    # [2] [5]               -> ()
    # [2] [3] [5]           -> (<val>)
    # [2] [3] [4a] [4b] [5] -> (<val>, <format>)

    def handle_print(add_newline: bool = False):
        nonlocal block
        format = None

        # no expr -> print a newline if enabled
        if block.expr() is None and add_newline:
            self.console.write("\n")
            return
        
        # Get format string if specified
        if block.format_():
            format = self.handle_block(block.format_(), block)

        # evaluate value to print
        to_print = self.handle_block(block.expr(), block)

        if isinstance(to_print, Num):
            to_print = to_print.get().value

        if isinstance(to_print, Expression):
            if to_print.type == TYPE_INT:
                to_print = int(to_print.value)
            elif to_print.type == TYPE_FLOAT:
                to_print = float(to_print.value)
            elif to_print.type == TYPE_BOOL:
                to_print = 'T' if to_print.value else 'F'
            elif to_print.type == TYPE_OBS:
                to_print = 'T' if to_print.get() else 'F'
            elif to_print.type == TYPE_OBS_REGISTER:
                to_print = to_print.get()
            elif to_print.type == TYPE_NUM:
                to_print = to_print.value
        

        def map_list(data, func):
            if isinstance(data, list):
                return [map_list(x, func) for x in data]
            else:
                return func(data)

        def convert_element(item):
            return item.value

        if isinstance(to_print, list):
            to_print = map_list(to_print, convert_element)
            
            
            



        

        print_text = to_print

        if format is not None:
            # when format is used, formated value cannot be a string
            if isinstance(print_text, str):
                self.script_errors.showError(
                    pos=pos,
                    error_type="RUNTIME ERROR",
                    title="String can't be a number",
                    msg="Try using digits next time. Just a suggestion."
                )
                exit()

            # format the number as BIN or HEX, decimal is the default
            if format == "BIN":
                print_text = f"0b{print_text:b}"
            elif format == "HEX":
                print_text = f"0x{print_text:X}"
        else:
            print_text = str(print_text)

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


    stmt_type = block.getChild(0).getText()

    if stmt_type == "print":
        handle_print()
    elif stmt_type == "println":
        handle_print(add_newline=True)
    elif stmt_type == "debug":
        pass
    elif stmt_type == "input":
        handle_input()
        
