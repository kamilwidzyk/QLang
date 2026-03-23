from typing import Any, List
from multiprocessing import Process
import time
import re
from dataclasses import dataclass
import sys


from .network import QuantumNetwork
from .script_errors import ScriptErrors
from .state import State, StateRegister
from .obs import Obs, ObsRegister
from .console import Console
from .consts import *
from .function import Function, FunctionParam
from .scope import Scope, ScopeManager

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

        

        block_type = block["type"]
        #print(block)
        print("BLOCK TYPE: " + block_type)

        handle_args = (self, block, parent, pos)

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
        }

        if block_type not in HANDLERS:
            print("UNKNOWN BLOCK TYPE: " + str(block_type))
            exit()

        return HANDLERS[block_type](*handle_args)



    def process_target(self):
        """
        Place execution entry point
        """
        sys.setrecursionlimit(4_000_000)

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


    


