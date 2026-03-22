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
    def __init__(self, name: str, params, body, 
                 closure_scope, pos: ScriptErrors.Position):
        self.name = name
        self.params = params
        self.body = body
        self.closure_scope = closure_scope
        self.pos = pos
        self.type = "Function"

    
    


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

        STATEMENT_CONTEXT = "StatementContext"
        OBS_DECL_CONTEXT = "ObsDeclContext"
        NUM_EXPR_CONTEXT = "NumExprContext"
        TERMINAL = "Terminal"
        IO_STMT_CONTEXT = "IoStmtContext"
        VAR_EXPR_CONTEXT = "VarExprContext" 
        FORMAT_CONTEXT = "FormatContext"
        PLACE_MEMBER_CONTEXT = "PlaceMemberContext"
        FUNCTION_DECL_CONTEXT = "FunctionDeclContext"
        BLOCK_CONTEXT = "BlockContext"

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
            # 1. Terminal 'obs'
            # 2. Terminal <variable_name>
            # If size defined:
            #   3a. Terminal '['
            #   3b. NumExprContext -> handle to get the size
            #   3c. Terminal ']'
            # If init with value:
            #   4a. Terminal '='
            #   4b. NumExprContext or measure(TODO!!!) -> handle to get value

            # Combinations:
            #         (CHILD INDEX)
            # (0) (1) (2)  (3)  (4)  (5)  (6)
            # [1] [2]                          -> obs name
            # [1] [2] [3a] [3b] [3c]           -> obs name[<size>]
            # [1] [2] [4a] [4b]                -> obs name = <val>
            # [1] [2] [3a] [3b] [3c] [4a] [4b] -> obs name[<size>] = <val>

            print("Parsing obs declaration")

            if not self.has_children(block):
                print("obsDeclContext 'children' key missing or no children")
                exit()

            children = block["children"]
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
                elif child_index == 1: # 2. Terminal <variable_name>
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
            # first child can be 'print', 'println' or 'input', 'debug'

            # PRINT
            # print(<val>)           -> print decimal
            # print(<val>, <format>) -> print bin/hex 
            # <val> = VarExprContext

            # 1. Terminal 'print'
            # 2. Terminal '('
            # 3. VarExprContext
            # If format defined:
            #   4a. Terminal ','
            #   4b. block 'format' HEX/BIN 
            # 5. Terminal ')'

            # Combinations
            #       (CHILD INDEX)
            # (0) (1) (2)  (3)  (4)
            # [2] [3] [5]           -> (<val>)
            # [2] [3] [4a] [4b] [5] -> (<val>, <format>)

            if not self.has_children(block):
                print("IoStmtContext: 'children' key missing or no children")
                exit()
            
            ioOperation = self.extract_text(block["children"][0], parent=block)

            if ioOperation == "print":
                format_specified = False
                format = None
                to_print = None

                children = block["children"][1:]

                for child_index in range(len(children)):
                    child = children[child_index]
                    if child_index == 0: # must be '('
                        if not self.is_terminal(child, text="(", parent=block):
                            print("IoStmtContext: child index 1, expected '('")
                            exit()
                    elif child_index == 1: # must be VarExprContext
                        if not self.is_type(child, type=VAR_EXPR_CONTEXT, parent=block):
                            print("IoStmtContext: child index 2, expected VarExprContext")
                            exit()
                        
                        to_print = self.handle_block(child, parent=block)
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

                if format_specified:
                    if format == "BIN":
                        print_text = f"{to_print:b}"
                    elif format == "HEX":
                        print_text - f"{to_print:X}"
                
                self.console.write(print_text)

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
            # paramList: param (',' param)*;
            # param: (STATE | OBS) ID ('[' NUMBER ']')?;
            # block: '{' statement* '}';

            # NUMBER: HEX_NUMBER | BIN_NUMBER | DEC_NUMBER;
            # fragment HEX_NUMBER: '0x' [0-9a-fA-F]+;
            # fragment BIN_NUMBER: '0b' [01]+;
            # fragment DEC_NUMBER: [0-9]+;

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


    


