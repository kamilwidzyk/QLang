from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import Obs, ObsRegister

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

        # INPUT '(' ID ('[' expr ']')? (',' format)? ')'
        

        # 1. Terminal '('
        # 2. Terminal <obs_name>
        # If index specified:
        #   3a. Terminal '['
        #   3b. index -> handle block to get value
        #   3c. Terminal ']'
        # If format specified:
        #   4a. Terminal ','
        #   4b. Terminal <format> = BIN or HEX
        # 5. Terminal ')'

        #            (CHILD INDEX)
        # (0) (1) (2)  (3)  (4)  (5)  (6)  (7)
        # [1] [2] [5]                          -> (<obs>)
        # [1] [2] [3a] [3b] [3c] [5]           -> (<obs>[<index>])
        # [1] [2] [4a] [4b] [5]                -> (<obs>, format)
        # [1] [2] [3a] [3b] [3c] [4a] [4b] [5] -> (<obs>[<index>], format)

        for child_index in range(len(children)):
            child = children[child_index]

            if child_index == 0: # 1. 
                if not self.is_terminal(child, text='(', parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: chid index 0, expected '('")
                    exit()
            elif child_index == 1: # 2.
                var_name = self.extract_text(child, parent=block)
            elif child_index == 2: # 5. or 3a. or 4a
                if self.is_terminal(child, text='[', parent=block):
                    # 3a.
                    index_specified = True
                elif self.is_terminal(child, text=',', parent=block):
                    # 4a.
                    format_specified = True
                elif not self.is_terminal(child, text=')', parent=block): # 5.
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 2, expected '[' or ',' or ')'")
                    exit()
            elif child_index == 3: # 3b.(index specified) or 4b.(otherwise)
                if index_specified:
                    var_index = self.handle_block(child, parent=block)
                else:
                    format = self.handle_block(child, parent=block)
            elif child_index == 4: # 3c.(index specified) or 5.(otherwise)
                if index_specified:
                    if not self.is_terminal(child, text=']', parent=block):
                        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 4, expected ']'")
                        exit()
                else:
                    if not self.is_terminal(child, text=')', parent=block):
                        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 4, expected ')'")
                        exit()
            elif child_index == 5: # 4a.(format specified) or 5.(otherwise)
                if format_specified:
                    if not self.is_terminal(child, text=',', parent=block):
                        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 5, expected ','")
                        exit()
                else:
                    if not self.is_terminal(child, text=')', parent=block):
                        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 5, expected ')'")
                        exit()
            elif child_index == 6: # 4b.
                format = self.handle_block(child, parent=block)
            elif child_index == 7: # 5.
                if not self.is_terminal(child, text=')', parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: child index 7, expected ')'")
                    exit()

        print("IO operation: input")
        print("var_name: " + str(var_name))
        print("var_index: " + str(var_index))
        print("format: " + str(format))

        if not self.scopes.exists(var_name):
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Name Error", "IoStmtContext: input, variable does not exist")
            exit()

        variable: Obs | ObsRegister = self.scopes.get(var_name)

        if variable.type not in ["Obs", "ObsRegister"]:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Type Error", "IoStmtContext: input, variable must be of type 'Obs' or 'ObsRegister'")
            exit()

        if var_index is not None and variable.type == "Obs":
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Type Error", "IoStmtContext: input, variable of type 'Obs' is not indexable")
            exit()
        
        max_val = variable.max_val()
        min_val = 0

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
            self.console.write(f"[Invalid input, required value range {min_val}-{max_val} in {format_str} format] ")

        print("Parsed console input: " + str(value))

        variable.set(value)
        self.scopes.set(var_name, variable)


    else:
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IoStmtContext: operation " + ioOperation + " unknown or not implemented")
        exit()