from typing import Any, List
from multiprocessing import Process
import time
import re
from dataclasses import dataclass
import sys

from .network import QuantumNetwork
from .script_errors import ScriptErrors
from .console import Console
from .consts import *
from .scope import ScopeManager

from .logger import log, PLACE, INFO

######################## CONTEXT HANDLERS #############################
from .context.statement              import handle_statement
from .context.obs_declaration        import handle_obs_declaration
from .context.number_expression      import handle_number_expression
from .context.io_statement           import handle_io_statement
from .context.variable_expression    import handle_variable_expression
from .context.place_member           import handle_place_member
from .context.function_declaration   import handle_function_declaration
from .context.param_list             import handle_param_list
from .context.param                  import handle_param
from .context.block                  import handle_block_ctx
from .context.obs_definition         import handle_obs_definition
from .context.string                 import handle_string
from .context.function_call          import handle_function_call
from .context.arg_list               import handle_arg_list
from .context.for_loop               import handle_for_loop
from .context.power                  import handle_power
from .context.format                 import handle_format
from .context.if_condition           import handle_if
from .context.rel_comp               import handle_rel_comp
from .context.add_sub                import handle_add_sub
from .context.not_op                 import handle_not
from .context.mul_div_mod            import handle_mul_div_mod
from .context.eq_comp                import handle_eq_comp
from .context.and_op                 import handle_and
from .context.or_op                  import handle_or
from .context.bool_val               import handle_bool
from .context.parentheses            import handle_parentheses
from .context.terminal               import handle_terminal
from .context.constraint             import handle_constraint

class Place:
    """
    Represents one place.

    Every instance of place starts a separate process to execute its code in.
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

    def is_terminal(self, block, text: str, parent=None) -> bool:
        """
        Check if a block matches is a Terminal and text matches

        Parameters:
            block: Block to test
            text(str): Text to match
            parent: Block one level higher than block, used for errors
        Returns:
            True: given block is a Terminal with given text
            False: otherwise
        """

        if "type" not in block:
            pos = ScriptErrors.Position.extract(block)
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", 
                                        "Terminal check: 'type' key missing in block structure")
            exit()
        
        if block["type"] != "Terminal":
            return False
        
        if "text" not in block:
            pos = ScriptErrors.Position.extract(block)
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", 
                                        "Terminal check: 'text' key missing in block structure")
            exit()
        
        if block["text"] != text:
            return False
        
        return True
    
    def extract_text(self, block, parent=None) -> str:
        """
        Extracts text from Terminal block

        Parameters:
            block: Block to extract text from
            parent: Block one level higher, used for errors
        Returns:
            str: Extracted text
        """
        if "type" not in block:
            pos = ScriptErrors.Position.extract(block)
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", 
                                        "Extract text: 'type' key missing in block structure")
            exit()

        if block["type"] != "Terminal":
            pos = ScriptErrors.Position.extract(block)
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", 
                                        "Extract text: block is not a terminal (type: " + block["type"] + ")")
            exit()

        if "text" not in block:
            pos = ScriptErrors.Position.extract(block)
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", 
                                        "Extract text: 'text' key missing in terminal block")
            exit()

        return block["text"]

    def is_valid_name(self, name: str) -> bool:
        """
        Checks if given name is a valid name.
        Valid name:
            - can only contains a-z A-Z 0-9 '_'
            - can't be a keyword

        Parameters:
            name(str): Name to check
        
        Returns:
            True: name is valid
            False: name is invalid
        """
        keywords = ["global"] # TODO: Add more keywords here

        # Polish/Unicode identifiers allowed (letters/digits/underscore), but cannot be a keyword
        return re.match(r'^[\w]+$', name, flags=re.UNICODE) and name not in keywords

    def is_type(self, block, type: str, parent=None) -> bool:
        """
        Checks if a block is of given type

        Parameters:
            block: Block to check
            type: Which type to expect
            parent: Block one level higher, for errors

        Returns:
            True: Block is of given type
            False: Block type is different
        """
        if "type" not in block:
            pos = ScriptErrors.Position.extract(block)
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", 
                                        "Is type: 'type' key missing in block structure")
            exit()
        
        return block["type"] == type

    def has_children(self, block) -> bool:
        """
        Returns True is given block has any children
        """
        if "children" not in block:
            return False
        
        if len(block["children"]) == 0:
            return False
        
        return True
    
    def handle_block(self, block, parent=None):
        """
        Recursive tree code execution

        Parameters:
            block: block to execute
            parent: block one level higher or none(if top-level)
        
        Returns:
            Return value depends on the block content
        """

        # check if type key exists and extract block position in code
        if "type" not in block:
            pos = ScriptErrors.Position.extract(block)
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", 
                                        "Handle block: 'type' key missing in block structure")
            exit()
        block_type = block["type"]

        pos = ScriptErrors.Position.extract(block)
        
        # Uncomment to show content of every executed block
        #print(block)
        #print("BLOCK TYPE: " + block_type)

        # Dictionary of handlers for every block type implemented
        HANDLERS = {
            TERMINAL:                       handle_terminal,
            STATEMENT_CONTEXT:              handle_statement,
            OBS_DECL_CONTEXT:               handle_obs_declaration,
            NUM_EXPR_CONTEXT:               handle_number_expression,
            IO_STMT_CONTEXT:                handle_io_statement,
            VAR_EXPR_CONTEXT:               handle_variable_expression,
            PLACE_MEMBER_CONTEXT:           handle_place_member,
            FUNCTION_DECL_CONTEXT:          handle_function_declaration,
            PARAM_LIST_CONTEXT:             handle_param_list,
            PARAM_CONTEXT:                  handle_param,
            BLOCK_CONTEXT:                  handle_block_ctx,
            OBS_DEF_CONTEXT:                handle_obs_definition,
            STR_EXPR_CONTEXT:               handle_string,
            FUNCTION_CALL_STMT_CONTEXT:     handle_function_call,
            FUNCTION_CALL_EXPR_CONTEXT:     handle_function_call,
            ARG_LIST_CONTEXT:               handle_arg_list,
            FOR_STMT_CONTEXT:               handle_for_loop,
            POW_EXPR_CONTEXT:               handle_power,
            FORMAT_CONTEXT:                 handle_format,
            IF_STMT_CONTEXT:                handle_if,
            REL_EXPR_CONTEXT:               handle_rel_comp,
            ADD_SUB_EXPR_CONTEXT:           handle_add_sub,
            NOT_EXPR_CONTEXT:               handle_not,
            MUL_DIV_MOD_EXPR_CONTEXT:       handle_mul_div_mod,
            EQ_EXPR_CONTEXT:                handle_eq_comp,
            AND_EXPR_CONTEXT:               handle_and,
            OR_EXPR_CONTEXT:                handle_or,
            BOOL_EXPR_CONTEXT:              handle_bool,
            PAREN_EXPR_CONTEXT:             handle_parentheses,
            CONSTRAINT_CONTEXT:             handle_constraint,
        }

        # Unknown block, do not execute, show error
        if block_type not in HANDLERS:
            if self.is_type(block, type="ExprContext", parent=parent):
                self.script_errors.showError(pos, "RUNTIME ERROR", "Syntax Error", 
                                        "Something is wrong, check syntax!")
                exit()

            self.script_errors.showError(pos, "DEEP ERROR", "Unknown Block Type", 
                                        "Unknown block type in AST: " + str(block_type) + " (not implemented)")
            exit()

        # Choose the fitting handler and run it on the block
        handle_args = (self, block, parent, pos)
        return HANDLERS[block_type](*handle_args)



    def process_target(self):
        """
        Place execution entry point
        """
        sys.setrecursionlimit(4_000_000)

        # Open console with title that includes place's name
        self.console = Console("Place: " + self.name)
        self.console.launch()

        # For some unknown reason not global place ends up in a double list
        if len(self.block) > 0 and type(self.block[0]) is list:
            self.block = self.block[0]

        # Run every top-level block of code
        for bl in self.block:
            self.handle_block(bl, parent=self.block)
        

    def run(self):
        """
        Starts execution of this place inside a separate process
        """
        self.proc = Process(target=self.process_target)
        self.proc.start()
        log(PLACE, INFO, f"Place {self.name} started")

    def wait_for_end(self):
        """
        Waits for execution to finish
        """
        self.proc.join()
        log(PLACE, INFO, f"Place {self.name} stopped")



    


