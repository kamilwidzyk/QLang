from typing import Any, List
from multiprocessing import Process
import time
from network import QuantumNetwork
from script_errors import ScriptErrors
from dataclasses import dataclass
from state import State, StateRegister
from obs import Obs, ObsRegister
import re
from console import Console

@dataclass
class Scope:
    def __init__(self, pos: ScriptErrors.Position, scope_type="block", parent=None):
        self.vars = {}
        self.pos = pos
        self.parent = parent
        self.type = scope_type


class ScopeManager:
    def __init__(self):
        # initialize with global scope that begins at 0, 0
        self.current = Scope(ScriptErrors.Position(0, 0))

    def push(self, pos: ScriptErrors.Position, scope_type: str):
        # go one scope down, pos = position of element that started the scope
        self.current = Scope(pos, scope_type, parent=self.current)

    def pop(self):
        # exit from scope
        if self.current.parent is not None:
            self.current = self.current.parent
        else:
            raise Exception("Cannot pop global scope")
        
    def get(self, name):
        # get var/func from current scope or higher
        scope = self.current
        while scope:
            if name in scope.vars:
                return scope.vars[name]
            scope = scope.parent
        raise Exception(f"Variable {name} not defined")
    
    def set(self, name, value):
        # assign a variable:
        # if found: assign value
        # if not found: create variable at current scope and assign (this will propably change)
        # there will be most likely a create method added to prevent assigment of non-existing variables
        scope = self.current
        while scope:
            if name in scope.vars:
                scope.vars[name] = value
                return
            scope = scope.parent
        self.current.vars[name] = value

    def exists(self, name) -> bool:
        # check if variable with a given name exists at the current scope
        return name in self.current.vars
    
    def create(self, name: str, value: Any):
        # create variable with given name at current scope
        # value will be a class instance which will specify type and size
        self.current.vars[name] = value

    def assign(self, name: str, value: Any):
        # assign an existing variable
        # search all the scopes 
        scope = self.current
        while scope:
            if name in scope.vars:
                scope.vars[name] = value
                return
            scope = scope.parent
        


class Function:
    def __init__(self, name: str, params: List[FunctionParam], body, 
                 closure_scope, pos: ScriptErrors.Position):
        self.name = name
        self.params = params
        self.body = body
        self.closure_scope = closure_scope
        self.pos = pos
        self.type = "Function"

class FunctionParam:
    def __init__(self, name: str, type: str, size: int):
        self.name = name # param name
        self.type = type # param type 'state' or 'obs'
        self.size = size # param size or None if not specified
    


class Place:
    """
    Represents one place, holds name and inner code
    """
    name: str = None
    block: List = []
    network: QuantumNetwork
    script_errors: ScriptErrors
    declared_at: ScriptErrors.Position
    scopes: ScopeManager
    console: Console


    def __init__(self, name: str, script_errors: ScriptErrors, 
                 declared_at: ScriptErrors.Position, network: QuantumNetwork):
        """
        Initializes the place with a name

        Parameters:
            name (str): Place name, specified by the code
            script_errors (ScriptErrors): instance of class for displaying errors
            network (QuauntumNetwork): instance of QuantumNetwork
        """
        self.name = name
        self.script_errors = script_errors
        self.network = network
        self.block = []
        self.declared_at = declared_at
        self.scopes = ScopeManager()
        

    def add_code(self, code: Any):
        """
        Adds code to this place

        Parameters:
            code (Any): code to add to this place, type depends on code
        """
        self.block.append(code)

    # TODO: add displaying of proper errors
    def is_terminal(self, block, text=None, parent=None) -> bool:
        # check if given block is a terminal and text matches
        # pass parent for error displaying
        if "type" not in block:
            print("Terminal check: 'type' key missing")
            exit()
        
        if block["type"] != "Terminal":
            return False
        
        if "text" not in block:
            print("Terminal check: 'text' key missing")
            exit()
        
        if block["text"] != text:
            return False
        
        return True
    
    # check if block it terminal and try to read 'text'
    # TODO: add displaying of proper errors
    def extract_text(self, block, parent=None) -> str:
        if "type" not in block:
            print("extract text: 'type' key missing")
            exit()

        if block["type"] != "Terminal":
            print("extract text: block is not a terminal")
            exit()

        if "text" not in block:
            print("extract text: 'text' key missing")
            exit()

        return block["text"]

    # valid name can only contain a-z A-z 0-9 and '_'
    # name cannot be 'global' or any keyword
    def is_valid_name(self, name: str) -> bool:
        if re.match(r'[a-zA-Z0-9_]+', name) and name != "global":
            return True
        return False

    # check if block is the given type
    # TODO: add error displaying
    def is_type(self, block, type: str, parent=None) -> bool:
        if "type" not in block:
            print("is type: 'type' key missing")
            exit()
        
        return block["type"] == type

    # check if block has 'children' key and at least one child
    def has_children(self, block) -> bool:
        if "children" not in block:
            return False
        
        if len(block["children"]) == 0:
            return False
        
        return True
    
    # TODO: add displaying of errors, in places where there are 'print' now
    # handle block may return a value when handling a NumExpr or function return
    def handle_block(self, block, parent=None):
        # check if 'type' key exists
        if "type" not in block:
            print("'type' key missing")
            exit()
        
        pos = ScriptErrors.Position.extract(block)

        STATEMENT_CONTEXT = "StatementContext" # any statement
        OBS_DECL_CONTEXT = "ObsDeclContext" # declaration of Observation variable
        NUM_EXPR_CONTEXT = "NumExprContext" # number expr = just a number
        TERMINAL = "Terminal" # terminal string
        IO_STMT_CONTEXT = "IoStmtContext" # print/println/input/debug
        VAR_EXPR_CONTEXT = "VarExprContext" # <name>[<index>] or <name>
        FORMAT_CONTEXT = "FormatContext" # print format option
        PLACE_MEMBER_CONTEXT = "PlaceMemberContext" # top level items of place block
        FUNCTION_DECL_CONTEXT = "FunctionDeclContext" # function declaration
        BLOCK_CONTEXT = "BlockContext" # block of code in { }
        PARAM_LIST_CONTEXT = "ParamListContext" # list of function parameters
        PARAM_CONTEXT = "ParamContext" # one function parameter (part of the list)
        OBS_DEF_CONTEXT = "ObsDefContext" # Observation definition list item
        STR_EXPR_CONTEXT = "StrExprContext" # String literal
        FUNCTION_CALL_STMT_CONTEXT = "FunctionCallStmtContext"
        ARG_LIST_CONTEXT = "ArgListContext"
        FOR_STMT_CONTEXT = "ForStmtContext"

        block_type = block["type"]
        print(block)
        print("BLOCK TYPE: " + block_type)

        if block_type == STATEMENT_CONTEXT:
            # this block is a statement
            # new scope: no
            if "children" not in block:
                print("statementContext 'children' key missing")
                exit()

            children = block["children"]

            for child in children:
                self.handle_block(child, parent=block)

        elif block_type == OBS_DECL_CONTEXT:
            # this block is a obs variable declaration
            # new scope: no

            # children should be:
            # OPTION A
            # 1. Terminal 'obs'
            # 2. Terminal <variable_name>
            # If size defined:
            #   3a. Terminal '['
            #   3b. NumExprContext -> handle to get the size
            #   3c. Terminal ']'
            # If init with value:
            #   4a. Terminal '='
            #   4b. NumExprContext or measure(TODO!!!) -> handle to get value

            # OR (OPTION B)
            # 1. Terminal 'obs'
            # 2. ObsDefContext
            # Until end:
            #   3a. Terminal ','
            #   3b. ObsDefContext

            

            # Combinations:
            #         (CHILD INDEX)
            # (0) (1) (2)  (3)  (4)  (5)  (6)
            # [1] [2]                          -> obs name
            # [1] [2] [3a] [3b] [3c]           -> obs name[<size>]
            # [1] [2] [4a] [4b]                -> obs name = <val>
            # [1] [2] [3a] [3b] [3c] [4a] [4b] -> obs name[<size>] = <val>

            print("Parsing obs declaration")

            if not self.has_children(block):
                print("obsDeclContext: 'children' key missing or no children")
                exit()

            children = block["children"]

            if len(children) < 2:                
                print("obsDeclContext: at least 2 children required")

            
            if self.is_type(children[1], type=OBS_DEF_CONTEXT, parent=block):
                # OPTION B
                # ...
                expect_block = True

                for child in children[1:]: # ignore the first
                    if expect_block:
                        if not self.is_type(child, type=OBS_DEF_CONTEXT, parent=block):
                            print("obsDeclContext: optionB: expected ObsDefContext block")
                            exit()
                        self.handle_block(child, block)
                        expect_block = False
                    else:
                        if not self.is_terminal(child, text=",", parent=block):
                            print("obsDeclContext: optionB: expected Terminal ','")
                            exit()
                        expect_block = True


                return

            # OPTION A

            size_defined = False
            init_value_defined = False
            obs_size = None
            obs_value = None
            obs_name = None

            for child_index in range(len(children)):
                child = children[child_index]
                if child_index == 0: # 1. Terminal 'obs'
                    if not self.is_terminal(child, text="obs", parent=block):
                        print("ObsDeclContext: first child is not terminal 'obs'")
                        exit()
                    print("1. Terminal 'obs' OK")
                elif child_index == 1: # 2. Terminal <variable_name> or ObsDefContext
                    obs_name = self.extract_text(child, parent=block)
                    if not self.is_valid_name(obs_name):
                        print("obsDeclContext: name is not valid: " + obs_name)
                        exit()
                    print("2. Terminal <variable_name> = " + obs_name)
                elif child_index == 2: # can be '[' or '='
                    text = self.extract_text(child, parent=block)
                    if text == '[': # size definition
                        size_defined = True
                        print("3a. Size definition")
                    elif text == '=': # value assigment
                        init_value_defined = True
                        print("4a. Terminal '='")
                    else:
                        print("obsDeclContext: unexpected terminal: " + text)
                        exit()
                elif child_index == 3: # can be size num or assigment val
                    if size_defined:
                        if not self.is_type(child, NUM_EXPR_CONTEXT, parent=block):
                            print("obsDeclContext: expected block of type numExprContext")
                            exit()
                        # handle numExprContext to get size
                        obs_size = self.handle_block(child, parent=block)
                        print("3b. size = " + str(obs_size))
                    elif init_value_defined:
                        # TODO: add more value init types here 
                        if not self.is_type(child, NUM_EXPR_CONTEXT, parent=block):
                            print("obsDeclContext: expected block of type numExprContext")
                            exit()
                        # handle to get init value
                        obs_value = self.handle_block(child, parent=block)
                        print("4b. init value = " + str(obs_value))
                    else:
                        print("obsDeclContext: unexpected block at child index 3")
                        exit()
                elif child_index == 4: # must be ']'
                    if not self.is_terminal(child, text="]", parent=block):
                        if size_defined:
                            print("obsDeclContext: child index 4, expected ']'")
                        else:
                            print("obsDeclContext: child index 4, unexpected block")
                        exit()
                elif child_index == 5: # must be '='
                    if not self.is_terminal(child, text='=', parent=block):
                        print("obsDeclContext: child index 5, expected '='")
                        exit()
                    init_value_defined = True
                elif child_index == 6: # must be val 
                    if init_value_defined:
                        # TODO: add more value init types here 
                        if not self.is_type(child, NUM_EXPR_CONTEXT, parent=block):
                            print("obsDeclContext: expected block of type numExprContext")
                            exit()
                        # handle to get init value
                        obs_value = self.handle_block(child, parent=block)
                        print("4b. init value = " + str(obs_value))
                    else:
                        print("obsDeclContext, child index 6, unexpected block")                         
                        exit()
                else:
                    print("obsDeclContext, child index > 6, unexpected block")                         
                    exit()

            print("Parsing done: ")
            print("Name: " + str(obs_name))
            print("Value: " + str(obs_value))
            print("Size: " + str(obs_size))

            # Create variable instance
            obs = None 

            if obs_size is not None: # size specified
                if int(obs_size) != obs_size or obs_size <= 0:
                    print("obsDeclContext: obs_size is not int or <= 0")
                    exit()
                obs = ObsRegister(obs_size)
                if obs_value is not None: # value specified
                    if int(obs_value) != obs_value or obs_value < 0:
                        print("obsDeclContext: obs_value is not int or < 0")
                        exit()
                    max_val = obs.max_val()
                    if obs_value > max_val:
                        print(f"obsDeclContext: obs_value is too large to fit in {obs_size} bits")                
                        exit()
                    obs.set(obs_value) # set value
            else: # one bit obs
                obs = Obs()
                if obs_value != 0 and obs_value != 1:
                    print("obsDeclContext: no size specified -> value can only be 0 or 1")
                    exit()
                obs.set(obs_value)
            
            self.scopes.create(obs_name, obs)
            print(f"Observation with name '{obs_name}' created")

        elif block_type == NUM_EXPR_CONTEXT:
            # numerical expression
            # TODO: there will be more, not it's just a Terminal number
            print("Parsing numExprContext")

            if not self.has_children(block):
                print("numExprContext: 'children' key missing or no children")
                exit()

            val = None

            for child in block["children"]:
                # terminal -> just a numebr
                if self.is_type(child, type=TERMINAL, parent=block):
                    text = self.extract_text(child, parent=block)
                    # TODO: add more ways of writing numbers: hex, bin, not just dec
                    val = int(text)
            
            print("Parsing done, value: " + str(val))
            return val

        elif block_type == IO_STMT_CONTEXT:
            # first child can be 'print', 'println'(TODO) or 'input'(TODO), 'debug'(TODO)

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
                print("IoStmtContext: 'children' key missing or no children")
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
                            print("IoStmtContext: child index 1, expected '('")
                            exit()
                    elif child_index == 1: # must be VarExprContext or ')'
                        if self.is_terminal(child, text=')', parent=block):
                            to_print = ""
                            is_string = True
                            break
                        if self.is_type(child, type=VAR_EXPR_CONTEXT, parent=block):
                            to_print = self.handle_block(child, parent=block)
                        elif self.is_type(child, type=STR_EXPR_CONTEXT, parent=block):
                            is_string = True
                            to_print = self.handle_block(child, parent=block)
                        else:
                            print("IoStmtContext: child index 2, expected VarExprContext pr StrExprContext")
                            exit()
                        
                        
                    elif child_index == 2: # ')' or ','
                        if self.is_terminal(child, text=",", parent=block):
                            format_specified = True
                        elif not self.is_terminal(child, text=")", parent=block):
                            print("IoStmtContext: child index 3, unexpected terminal")
                            exit()
                    elif child_index == 3:
                        if not format_specified:
                            print("IoStmtContext: child index 4, unexpected block")
                            exit()
                        
                        if not self.is_type(child, type=FORMAT_CONTEXT, parent=block):
                            print("IoStmtContext: child index 4, expected 'FormatContext' block")
                            exit()

                        format = self.handle_block(child, parent=block)
                    elif child_index == 4: # must be ')'
                        if not format_specified:
                            print("IoStmtContext: child index 5, unexpected block")
                            exit()

                        if not self.is_terminal(child, text=")", parent=block):
                            print("IoStmtContext: child index 5, expected ')'")
                            exit()
                    else:
                        print("IoStmtContext, child index > 5, unexpected block")
                        exit()
                
                print("IoStmtContext, parsed 'print'")
                print("To print: " + str(to_print))
                print("Format: " + (str(format) if format_specified else "DEC")) 

                print_text = to_print

                if not is_string:

                    if format_specified:
                        if format == "BIN":
                            print_text = f"{to_print:b}"
                        elif format == "HEX":
                            print_text - f"{to_print:X}"
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
                            print("IoStmtContext: chid index 0, expected '('")
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
                            print("IoStmtContext: child index 2, expected '[' or ',' or ')'")
                            exit()
                    elif child_index == 3: # 3b.(index specified) or 4b.(otherwise)
                        if index_specified:
                            var_index = self.handle_block(child, parent=block)
                        else:
                            format = self.handle_block(child, parent=block)
                    elif child_index == 4: # 3c.(index specified) or 5.(otherwise)
                        if index_specified:
                            if not self.is_terminal(child, text=']', parent=block):
                                print("IoStmtContext: child index 4, expected ']'")
                                exit()
                        else:
                            if not self.is_terminal(child, text=')', parent=block):
                                print("IoStmtContext: child index 4, expected ')'")
                                exit()
                    elif child_index == 5: # 4a.(format specified) or 5.(otherwise)
                        if format_specified:
                            if not self.is_terminal(child, text=',', parent=block):
                                print("IoStmtContext: child index 5, expected ','")
                                exit()
                        else:
                            if not self.is_terminal(child, text=')', parent=block):
                                print("IoStmtContext: child index 5, expected ')'")
                                exit()
                    elif child_index == 6: # 4b.
                        format = self.handle_block(child, parent=block)
                    elif child_index == 7: # 5.
                        if not self.is_terminal(child, text=')', parent=block):
                            print("IoStmtContext: child index 7, expected ')'")
                            exit()

                print("IO operation: input")
                print("var_name: " + str(var_name))
                print("var_index: " + str(var_index))
                print("format: " + str(format))

                if not self.scopes.exists(var_name):
                    print("IoStmtContext: input, variable does not exist")
                    exit()

                variable: Obs | ObsRegister = self.scopes.get(var_name)

                if variable.type not in ["Obs", "ObsRegister"]:
                    print("IoStmtContext: input, variable must be of type 'Obs' or 'ObsRegister'")
                    exit()

                if var_index is not None and variable.type == "Obs":
                    print("IoStmtContext: input, variable of type 'Obs' is not indexable")
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
                print("IoStmtContext: operation " + ioOperation + " unknown or not implemented")
                exit()


        elif block_type == VAR_EXPR_CONTEXT:

            # ID ('[' expr ']')? 

            # 1. Terminal <variable_name>
            # If index specified:
            #   2a. Terminal '['
            #   2b. expression block -> handle to get index
            #   2c. Terminal ']'

            if not self.has_children(block):
                print("VarExprContext: 'children' key missing or not children")
                exit()

            children = block["children"]

            var_name = None
            index = None
            index_specified = False

            for child_index in range(len(children)):
                child = children[child_index]
                if child_index == 0:
                    var_name = self.extract_text(child, parent=block)
                elif child_index == 1: 
                    if not self.is_terminal(child, text="[", parent=block):
                        print("VarExprContext: child index 1, expected '['")
                        exit()
                    index_specified = True
                elif child_index == 2:
                    if not index_specified:
                        print("VarExprContext: child index 2, unexpected block")
                        exit()
                    index = self.handle_block(child, block)
                elif child_index == 3:
                    if not index_specified:
                        print("VarExprContext: child index 3, unexpected block")
                        exit()
                    if not self.is_terminal(child, text="]", parent=block):
                        print("VarExprContext: child index 3, expected ']'")
                        exit()
                else:
                    print("VarExprContext: child index > 3, unexpected block")
                    exit()
            
            print("VarExprContext parsed")
            print("Name: " + str(var_name))
            print("Index: " + str(index))

            if not self.scopes.exists(var_name):
                print("VarExprContext: variable '" + str(var_name) + "' does not exist")
                exit()

            variable = self.scopes.get(var_name)

            if type(variable) == int:
                return variable

            if variable.type in ["StateRegister", "State"]:
                print("VarExprContext: attempted reading of quantum state")
                exit()

            if index_specified:
                if int(index) != index or index < 0:
                    print("VarExprContext: index is not int or < 0")
                    exit()

                if variable.type != "ObsRegister":
                    print("VarExprContext: attempted accesing index of non index obs")
                    exit()
                
                return 1 if variable[index] else 0
            
            if variable.type == "Obs":
                return 1 if variable.get() else 0
            
            if variable.type == "ObsRegister":
                return variable.get() 
            
            print("varExprContext: incorrect variable type: " + variable.type)
            exit()
            
        elif block_type == PLACE_MEMBER_CONTEXT:
            
            if not self.has_children(block):
                print("PlaceMemberContext: 'children' key missing or no children")
                exit()

            for child in block["children"]:
                self.handle_block(child, parent=block)

                
        elif block_type == FUNCTION_DECL_CONTEXT:

            # functionDecl: FUNCTION ID '(' paramList? ')' block;
           
            # 1. Terminal 'function'
            # 2. Terminal <function_name>
            # 3. Terminal '('
            # Optional: 4. paramList -> handle block
            # 5. Terminal ')'
            # 6. BlockContext -> handle block

            if not self.has_children(block):
                print("functionDeclContext: 'children' key missing or no children")
                exit()

            children = block["children"]

            func_name = None
            param_list = None
            func_block = None
            no_params = False

            for child_index in range(len(children)):
                child = children[child_index]

                if child_index == 0: # 1. Terminal 'function'
                    if not self.is_terminal(child, text="function", parent=block):
                        print("functionDeclContext: child index 0, expected 'function'")
                        exit()
                elif child_index == 1: # 2. Terminal <function_name>
                    func_name = self.extract_text(child, parent=block)
                    if not self.is_valid_name(func_name):
                        print("functionDeclContext: child index 1, function name invalid")
                        exit()
                elif child_index == 2: # 3. Terminal '('
                    if not self.is_terminal(child, text="(", parent=block):
                        print("functionDeclContext: child index 2, expected '('")
                        exit()
                elif child_index == 3: # 4. or 5.
                    if self.is_type(child, TERMINAL, parent=block):
                        if not self.is_terminal(child, text=')', parent=block):
                            print("functionDeclContext: child index 3, expected ')'")
                            exit()
                        no_params = True # this function has no parameters
                    else:
                        param_list = self.handle_block(child, parent=block) 
                elif child_index == 4: # 5. or 6.
                    if no_params:
                        if not self.is_type(child, BLOCK_CONTEXT, parent=block):
                            print("functionDeclContext: child index 4, expected BlockContext")
                            exit()
                        func_block = self.handle_block(child, parent=block)
                    else:
                        if not self.is_terminal(child, text=')', parent=block):
                            print("functionDeclContext: child index 4, expected ')'")
                            exit()
                elif child_index == 5: # 6. only if function has params
                    if no_params:
                        print("functionDeclContext: child index 5, unexpected block")
                        exit()
                    else:
                        if not self.is_type(child, BLOCK_CONTEXT, parent=block):
                            print("funcDeclContext: child index 5, excepted BlockContext")
                            exit()
                        func_block = self.handle_block(child, parent=block)
                else:
                    print("functionDeclContext: child index > 5, unexpected block")
                    exit()

            print("Function Declaration parse done")
            print("Function name: " + str(func_name))
            print("Function parameters: " + str(param_list))
            print("Function code: " + str(func_block))

            if self.scopes.exists(func_name):
                print("FuncDeclContext: variable or function with this name already exists")
                exit()

            func = Function(func_name, param_list, func_block, self.scopes.current, pos)
            self.scopes.create(func_name, func)            
        
        elif block_type == PARAM_LIST_CONTEXT:
            # paramList: param (',' param)*;

            param_list = []

            if not self.has_children(block):
                print("ParamListContext: 'children' key missing or no children")
                exit()

            children = block["children"] 

            for child_index in range(len(children)):
                child = children[child_index]
                # ignore Terminals ','
                if not self.is_terminal(child, text=',', parent=block):
                    param_list.append(self.handle_block(child, block))

            return param_list

        elif block_type == PARAM_CONTEXT:
            # param: (STATE | OBS) ID ('[' NUMBER ']')?;

            # 1. Terminal 'state' or 'obs' => param type
            # 2. Terminal <variable_name> => param name (must be a valid name)
            # If size specified:
            #   3a. Terminal '['
            #   3b. Number -> handle block to get value
            #   3c. Terminal ']'

            param_type = None
            param_name = None
            param_size = None
            size_specified = False

            if not self.has_children(block):
                print("ParamContext: 'children' key missing or no children")
                exit()

            children = block["children"]

            for child_index in range(len(children)):
                child = children[child_index]

                if child_index == 0: # 1. Terminal 'state' or 'obs'
                    if self.is_terminal(child, text="state", parent=block):
                        param_type = "state"
                    elif self.is_terminal(child, text="obs", parent=block):
                        param_type = "obs"
                    else:
                        print("ParamContext: child index 0, expected terminal 'state' or 'obs'")
                        exit()
                elif child_index == 1: # 2. Terminal <variable_name>
                    param_name = self.extract_text(child, parent=block)
                    if not self.is_valid_name(param_name):
                        print("ParamContext: child index 1, param name is not valid")
                        exit()
                elif child_index == 2: # 3a. Terminal '[' 
                    if not self.is_terminal(child, text='[', parent=block):
                        print("ParamContext: child index 2, unexpected block")
                        exit()
                    size_specified = True
                elif child_index == 3: # 3b. Number
                    if not size_specified:
                        print("ParamContext: child index 3, unexpected block")
                        exit()
                    param_size = self.handle_block(child, parent=block)
                elif child_index == 4: # 3c. Terminal ']'
                    if not size_specified:
                        print("ParamContext: child index 4, unexpected block")
                        exit()
                    if not self.is_terminal(child, text="]", parent=block):
                        print("ParamContext: child index 4, expected ']'")
                        exit()
                else:
                    print("ParamContext: child index > 4, unexpected block")
                    exit()

            return FunctionParam(name=param_name, type=param_type, size=param_size)


        elif block_type == BLOCK_CONTEXT:
            # 1. Terminal '{' (first child)
            # 2. Block of code to return (everything in between)
            # 3. Terminal '}' (last child)

            if not self.has_children(block):
                print("BlockContext: missing 'children' key or no children")
                exit()

            children = block["children"]

            if len(children) < 2:
                print("BlockContext: at least 2 children required(empty block)")
                exit()

            if not self.is_terminal(children[0], text="{", parent=block):
                print("BlockContext: child index 0, expected '{'")
                exit()

            if not self.is_terminal(children[-1], text="}", parent=block):
                print("BlockContext: last child, expected '}'")
                exit()

            return children[1:-1]

        elif block_type == OBS_DEF_CONTEXT:
            # obsDef: ID ('[' expr ']')?;

            # 1. Terminal <variable_name> (must be valid name)
            # If size specified:
            #   2a. Terminal '['
            #   2b. expr -> handle to get size
            #   2c. Terminal ']'

            if not self.has_children(block):
                print("ObsDefContext: missing 'children' key or no children")
                exit()

            children = block["children"]

            var_name = None
            var_size = None
            size_specified = False

            for child_index in range(len(children)):
                child = children[child_index]

                if child_index == 0:
                    var_name = self.extract_text(child, parent=block)
                    if not self.is_valid_name(var_name):
                        print("ObsDefContext: variable name is not valid")
                        exit()
                elif child_index == 1:
                    if not self.is_terminal(child, text='[', parent=block):
                        print("ObsDefContext: child index 1, expected '['")
                        exit()
                    size_specified = True
                elif child_index == 2:
                    if not size_specified:
                        print("ObsDefContext: child index 2, unexpected block")
                        exit()
                    var_size = self.handle_block(child, parent=block)
                elif child_index == 3:
                    if not size_specified:
                        print("ObsDefContext: child index 3, unexpected block")
                        exit()
                    if not self.is_terminal(child, text=']', parent=block):
                        print("ObsDefContext: child index 3, expected ']'")
                        exit()
            
            if self.scopes.exists(var_name):
                print("ObsDefContext: variable name already exists")
                exit()

            if var_size <= 0:
                print("ObsDefContext: variable size is <= 0")
                exit()

            variable = None

            if size_specified:
                variable = ObsRegister(var_size)
            else:
                variable = Obs()

            self.scopes.create(var_name, variable)

        elif block_type == STR_EXPR_CONTEXT:
            # STRING     : '"' (~["\r\n])* '"' ;

            # 1. Terminal "<content>"

            if not self.has_children(block):
                print("StrExprContext: missing 'children' key or no children")
                exit()
            
            content = self.extract_text(block["children"][0], parent=block)

            if len(content) < 2:
                print("StrExprContent: content size of minimum 2 is required(empty string)")
                exit()
            
            return content[1:-1] # remove first and last characters(")

        elif block_type == FUNCTION_CALL_STMT_CONTEXT:
            # functionCallStmt: ID '(' argList? ')';

            # 1. Terminal <function_name> 
            # 2. Terminal '('
            # If has arguments:
            #   3. argList block
            # 4. Terminal ')'

            if not self.has_children(block):
                print("FunctionCallStmtContext")
                exit()
            
            children = block["children"]

            func_name = None
            args = None
            has_args = False

            for child_index in range(len(children)):
                child = children[child_index]
                if child_index == 0:
                    func_name = self.extract_text(child, block)
                elif child_index == 1:
                    if not self.is_terminal(child, text='(', parent=block):
                        print("FunctionCallStmtContext: child index 1, expected '('")
                        exit()
                elif child_index == 2:
                    if self.is_type(child, type=ARG_LIST_CONTEXT, parent=block):
                        args = self.handle_block(child, parent=block)
                        has_args = True
                    elif not self.is_terminal(child, text=')', parent=block):
                        print("FunctionCallStmtContext: child index 2, expected ')'")
                        exit()
                elif child_index == 3:
                    if not has_args:
                        print("FunctionCallStmtContext: child index 3, unexpected block")
                        exit()
                    if not self.is_terminal(child, text=")", parent=block):
                        print("FunctionCallStmtContext: child index 3, expected ')'")
                        exit()

            print("Function call: name: " + str(func_name) + " args: " + str(args))

           
            if not self.scopes.exists(func_name):
                print("FunctionCallStmtContext: Function does not exist")
                exit()

            # Call the function
            function_def: Function = self.scopes.get(func_name)

            # Create new scope for function
            new_scope = Scope(
                pos=pos,
                parent=function_def.closure_scope
            )

            # Add names functions args to it
            param_names = [p.name for p in function_def.params]
            for param_name, param_value in zip(param_names, args):
                new_scope.vars[param_name] = param_value
            
            # Switch execution context
            old_scope = self.scopes.current
            self.scopes.current = new_scope

            return_val = None
            # Execute function
            for func_block in function_def.body:
                return_val = self.handle_block(func_block)
                # TODO: This is propably wrong way to handle return values
                # but it will do for now
                if return_val is not None: # return called
                    break # do not execute more
            

            # Recover scope
            self.scopes.current = old_scope

            print("Function execution done")
            print("Return val: " + str(return_val))

            return return_val


        
        elif block_type == ARG_LIST_CONTEXT:
            # argList: expr (',' expr)*;

            if not self.has_children(block):
                print("ArgListContext: missing 'children' key or no children")
                exit()
            
            children = block["children"]

            args = []

            expect_block = True

            for child in children:
                if expect_block:
                    val = self.handle_block(child, block)
                    args.append(val)
                    expect_block = False
                else:
                    if not self.is_terminal(child, text=',', parent=block):
                        print("ArgListContext: expected ','")
                        exit()
                    expect_block = True

            return args

        elif block_type == FOR_STMT_CONTEXT:

            # forStmt: FOR ID FROM expr TO expr (STEP expr)? block;

            # for <name> from <start> to <end> block
            # for <name> from <start> to <end> step <step> block

            # 1. Terminal 'for'
            # 2. Terminal <name>
            # 3. Terminal 'from'
            # 4. Terminal <start>
            # 5. Terminal 'to'
            # 6. Terminal <end>
            # If step define:
            #   7a. Terminal 'step'
            #   7b. Terminal <step>
            # 8. BlockContext -> for body

            #            (CHILD INDEX)
            # (0) (1) (2) (3) (4) (5) (6)  (7)  (8)
            # [1] [2] [3] [4] [5] [6] [8]   
            # [1] [2] [3] [4] [5] [6] [7a] [7b] [8]
            # 
            
            if not self.has_children(block):
                print("ForStmtContext: missing 'child' key or no children")
                exit()

            children = block["children"]

            var_name = None
            start_val = None
            end_val = None
            step_defined = False
            step_val = None
            for_block = None


            for child_index in range(len(children)):
                child = children[child_index]

                if child_index == 0:
                    if not self.is_terminal(child, text='for', parent=block):
                        print("ForStmtContext: child index 0, expected 'for'")
                        exit()
                elif child_index == 1:
                    var_name = self.handle_block(child, parent=block)
                elif child_index == 2:
                    if not self.is_terminal(child, text='from', parent=block):
                        print("ForStmtContext: child index 2, expected 'from'")
                        exit()
                elif child_index == 3:
                    start_val = self.handle_block(child, parent=block)
                elif child_index == 4:
                    if not self.is_terminal(child, text='to', parent=block):
                        print("ForStmtContext: child index 4, expected 'to'")
                        exit()
                elif child_index == 5:
                    end_val = self.handle_block(child, parent=block)
                elif child_index == 6:
                    if self.is_terminal(child, text='step', parent=block):
                        step_defined = True
                    else:
                        for_block = self.handle_block(child, parent=block)
                elif child_index == 7:
                    if not step_defined:
                        print("ForStmtContext: child index 7, unexpecxted block")
                        exit()

                    step_val = self.handle_block(child, parent=block)
                elif child_index == 8:
                    if not step_defined:
                        print("ForStmtContext: child index 8, unexpected block")
                        exit()

                    for_block = self.handle_block(child, parent=block)
                else:
                    print("ForStmtContext: child index > 8, unexpected block")
                    exit()

            
            print("For loop")
            print("Variable name: " + var_name)
            print("Start: " + str(start_val))
            print("End: " + str(end_val))
            print("Step: " + str(step_val))
            print("Block: " + str(for_block))

            if start_val < 0:
                print("For loop: start_val < 0")
                exit()

            if end_val < 0:
                print("For loop: end_val < 0")
                exit()
            
            if step_val is None:
                step_val = 1

            if step_val < 0:
                print("For loop: step_val < 0")
                exit()

            if end_val < start_val:
                print("For loop: skip") # This is not an error
                return # do not run loop
            
            current_val = ObsRegister(32)
            current_val.set(start_val)

            # Enter new scope
            self.scopes.push(pos, scope_type="for")
            self.scopes.create(var_name, current_val)

            # Repeat block until current_val <= end_val
            while current_val.get() <= end_val:
                break_loop = False
                for child in for_block:
                    ret_val = self.handle_block(child, parent=block)

                    if ret_val is not None:
                        break_loop = True
                        print("For loop: break")
                        break

                if break_loop:
                    break

                current_val.set(current_val.get() + step_val)
                self.scopes.set(var_name, current_val)

            # Exit scope
            self.scopes.pop()

            print("For loop: done")

            
                
                

        











        elif block_type == TERMINAL:
            text = self.extract_text(block, parent)
            return text
        
        else:
            print(">>>>>>>>>>>>>>>>>>>> UNKNOWN BLOCK TYPE: " + block_type)
            exit()









    def process_target(self):
        """
        Place execution entry point
        """
        print("Opening console")

        self.console = Console("Place: " + self.name)
        self.console.launch()

        # For some unknown reason not global place ends up in double list
        if len(self.block) > 0 and type(self.block[0]) is list:
            print("Extra list removed")
            self.block = self.block[0]

        print(f"[{self.name}] Started!")


        print("---------------------------------------")

        for bl in self.block:
            self.handle_block(bl, parent=self.block)

        print("---------------------------------------")

        

    def run(self):
        """
        Starts execution of this place inside a separate process
        """
        self.proc = Process(target=self.process_target)
        self.proc.start()

    def wait_for_end(self):
        """
        Waits for execution to finish
        """
        self.proc.join()


    


