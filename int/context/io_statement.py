from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import Obs, ObsRegister

import random

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



    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: 'children' key missing or no children")
        exit()
    
    ioOperation = self.extract_text(block["children"][0], parent=block)

    if ioOperation in ["print", "println"]:
        
        add_new_line = ioOperation == "println"
        format_specified = False
        format = None
        to_print = None
        is_string = False

        children = block["children"][1:]

        for child_index in range(len(children)):
            child = children[child_index]
            if child_index == 0: # must be '('
                if not self.is_terminal(child, text="(", parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 1, expected '('")
                    exit()
            elif child_index == 1: # must be VarExprContext or ')'
                if self.is_terminal(child, text=')', parent=block):
                    to_print = ""
                    is_string = True
                    break


                if self.is_type(child, type=STR_EXPR_CONTEXT, parent=block):
                    is_string = True
                
                to_print = self.handle_block(child, parent=block)
                
            elif child_index == 2: # ')' or ','
                if self.is_terminal(child, text=",", parent=block):
                    format_specified = True
                elif not self.is_terminal(child, text=")", parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 3, unexpected terminal")
                    exit()
            elif child_index == 3:
                if not format_specified:
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 4, unexpected block")
                    exit()
                
                if not self.is_type(child, type=FORMAT_CONTEXT, parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 4, expected 'FormatContext' block")
                    exit()

                format = self.handle_block(child, parent=block)
            elif child_index == 4: # must be ')'
                if not format_specified:
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 5, unexpected block")
                    exit()

                if not self.is_terminal(child, text=")", parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 5, expected ')'")
                    exit()
            else:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext, child index > 5, unexpected block")
                exit()
        
        print("IoStmtContext, parsed 'print'")
        print("To print: " + str(to_print))
        print("Format: " + (str(format) if format_specified else "DEC")) 

        print_text = to_print

        if not is_string:

            if format_specified:
                if format == "BIN":
                    print_text = f"0b{to_print:b}"
                elif format == "HEX":
                    print_text = f"0x{to_print:X}"
            else:
                print_text = str(to_print)
        if add_new_line:
            self.console.write(print_text + "\n")
        else:
            self.console.write(print_text)

    elif ioOperation == "input":
        children = block["children"][1:]

        format_specified = False
        format = None
        index_specified = False
        var_index = None
        var_name = None
        constraint_specified = False
        constraint_min = None
        constraint_max = None


        # INPUT '(' ID ('[' expr ']')? (',' format)? (',' constraint)? ')'
        

        # 1. Terminal '('
        # 2. Terminal <obs_name>
        # If index specified:
        #   3a. Terminal '['
        #   3b. index -> handle block to get value
        #   3c. Terminal ']'
        # If format specified:
        #   4a. Terminal ','
        #   4b. Terminal <format> = BIN or HEX
        # If constraint specified:
        #   5a. Terminal ','
        #   5b. Block ConstraintContext -> returns as (min, max)
        # 6. Terminal ')'

        #            (CHILD INDEX)
        # (0) (1) (2)  (3)  (4)  (5)  (6)  (7)  (8)  (9)
        # [1] [2] [6]                                    -> (<obs>)
        # [1] [2] [3a] [3b] [3c] [6]                     -> (<obs>[<index>])
        # [1] [2] [4a] [4b] [6]                          -> (<obs>, format)
        # [1] [2] [3a] [3b] [3c] [4a] [4b] [6]           -> (<obs>[<index>], format)
        # (0) (1) (2)  (3)  (4)  (5)  (6)  (7)  (8)  (9)
        # [1] [2] [5a] [5b] [6]                          -> (<obs>, constraint)
        # [1] [2] [3a] [3b] [3c] [5a] [5b] [6]           -> (<obs>[<index>], constraint)
        # [1] [2] [4a] [4b] [5a] [5b] [6]                -> (<obs>, format, constraint)
        # [1] [2] [3a] [3b] [3c] [4a] [4b] [5a] [5b] [6] -> (<obs>[<index>], format, constraint)

        args = []

        arg = []
        for child in children:
            if self.is_terminal(child, text=',', parent=block):
                args.append(arg)
                arg = []
            elif not self.is_terminal(child, text='(', parent=block) and not self.is_terminal(child, text=')', parent=block):
                arg.append(child)
        args.append(arg)

        if len(args) < 1:
            self.script_errors.showError(pos, "RUNTIME ERROR", "You Error", "No arguments. Where should I put the data?")
            exit()

        print(args)

        var_arg = args[0]

        # <obs>[<index>]?
        for child_index in range(len(var_arg)):
            child = var_arg[child_index]

            if child_index == 0: # Terminal <var_name>
                var_name = self.extract_text(child, parent=block)
            elif child_index == 1: # Terminal '[' -> index specified
                if self.is_terminal(child, text='[', parent=block):
                    index_specified = True
            elif child_index == 2: # index expr
                if not index_specified:
                    self.script_errors.showError(pos, "SYNTAX ERROR", "Unexpected thing", "There should not be anything more")
                    exit()
                var_index = self.handle_block(child, block)
            elif child_index == 3:
                if not index_specified:
                    self.script_errors.showError(pos, "SYNTAX ERROR", "Unexpected thing", "There should not be anything more")
                    exit()
                if not self.is_terminal(child, text=']', parent=block):
                    self.script_errors.showError(pos, "SYNTAX ERROR", "Expected ']'", "Close the index, please")
                    exit()
        
        # check the second arg(format or constraint) if it exists
        if len(args) > 1:
            second_arg = args[1]
            # format or constraint

            for child_index in range(len(second_arg)):
                child = second_arg[child_index]

                if child_index == 0:
                    if self.is_type(child, type=FORMAT_CONTEXT, parent=block):
                        format_specified = True
                        format = self.handle_block(child, parent=block)
                    elif self.is_type(child, type=CONSTRAINT_CONTEXT, parent=block):
                        constraint_specified = True
                        constraint_min, constraint_max = self.handle_block(child, parent=block)
                    else:
                        print(child["type"])
                        print(child["text"])
                        self.script_errors.showError(pos, "SYNTAX ERROR", "Unexpected block", "There can only be a format or a constraint")
                        exit()
                else:
                    self.script_errors.showError(pos, "SYNTAX ERROR", "Unexpected block", "There can only be a format or a constraint")
                    exit()
            
        # check the third arg(constraint) if it exists
        if len(args) > 2:
            third_arg = args[2]
            # constraint only

            for child_index in range(len(second_arg)):
                child = second_arg[child_index]

                if child_index == 0:
                    if self.is_type(child, type=CONSTRAINT_CONTEXT, parent=block):
                        constraint_specified = True
                        constraint_min, constraint_max = self.handle_block(child, parent=block)
                    else:
                        self.script_errors.showError(pos, "SYNTAX ERROR", "Unexpected block", "There can only be a constraint")
                        exit()
                else:
                    self.script_errors.showError(pos, "SYNTAX ERROR", "Unexpected block", "There can only be a constraint")
                    exit()

        print("IO operation: input")
        print("var_name: " + str(var_name))
        print("var_index: " + str(var_index))
        print("format: " + str(format))
        print("Min: " + str(constraint_min))
        print("Max: " + str(constraint_max))

        if not self.scopes.exists(var_name):
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "You Error", "No variable. You forgot to make it, input lost to the void.")
            exit()

        variable: Obs | ObsRegister = self.scopes.get(var_name)

        if variable.type not in ["Obs", "ObsRegister"]:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Type Error", "Not how this works. I need an observation(s).")
            exit()

        if var_index is not None and variable.type == "Obs":
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Index Error", "You are looking too deep into something that can only be 0 or 1.")
            exit()
        
        # default value constraint is 0 to variable max val
        max_val = variable.max_val()
        min_val = 0

        # update to given constraint if possible
        if constraint_specified:
            if constraint_min is not None:
                min_val = constraint_min
            if constraint_max is not None:
                max_val = constraint_max


        value = None

        while True:
            print("Waiting for console input...")
            console_in = self.console.read("")
            print("Console input: " + str(console_in))

            if console_in is None:
                continue
                
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
                    value = int(console_in)
                    if value >= min_val and value <= max_val:
                        break # valid value received -> end of loop
                except:
                    pass # not a number
            
            format_str = {None: "decimal", "BIN": "binary", "HEX": "hexadecimal"}[format]
            invalid = [
                "That's not gonna work.", "What evein is that input.", "Try again, but correctly.",
                "I can't work with that.", "Rejected.", "Input denied.", "Nice try, but no.",
                "Be serious.", "No idea what that is.", "Nah.", "Hard no.", "Rejected in 0ms.",
                "Absolutely not.", "Fail.", "Not today.", "Not a chance.", "Try harder.",
                "LOL, no.", "Wrong.", "No.", "Nope.", "That's a no.", "Do better.",
                "Denied.", "I can't let that slide."
            ]

            self.console.write(f"[{random.sample(invalid, 1)[0]} I need a number in range {min_val}-{max_val} in {format_str} format] ")

        print("Parsed console input: " + str(value))

        variable.set(value)
        self.scopes.set(var_name, variable)


    else:
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: operation " + ioOperation + " unknown or not implemented")
        exit()