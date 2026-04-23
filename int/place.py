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

from .logger import log, PLACE, INFO, FATAL

from antlr4 import *
from antlr4.tree.Tree import TerminalNode
from .QLang.QLangLexer import QLangLexer
from .QLang.QLangParser import QLangParser

######################## EXCEPTIONS #############################
from .exception.assignment_to_expression import AssignmentToExpressionException
from .exception.divide_by_zero import DivideByZeroException
from .exception.modulo_over_zero import ModuloOverZeroException

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
from .context.assigment              import handle_assigment
from .context.num_declaration        import handle_num_declaration
from .context.minus_op               import handle_minus
from .context.pre_post               import handle_pre_decrement, handle_post_decrement
from .context.pre_post               import handle_pre_increment, handle_post_increment
from .context.plus_op                import handle_plus
from .context.assignment_expr        import handle_assignment_expr
from .context.plus_eq_op             import handle_plus_eq_op
from .context.minus_eq_op            import handle_minus_eq_op
from .context.mul_eq_op              import handle_mul_eq_op
from .context.div_eq_expr            import handle_div_eq_op
from .context.mod_eq_op              import handle_mod_eq_op
from .context.pow_eq_op              import handle_pow_eq_op
from .context.and_eq_op              import handle_and_eq_op
from .context.or_eq_op               import handle_or_eq_op

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
    test_mode: bool = False


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
        
    def enable_test_mode(self):
        self.test_mode = True

    def add_code(self, code: Any):
        """
        Adds code to this place

        Parameters:
            code (Any): code to add to this place, type depends on code
        """
        self.block.append(code)

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

    def handle_block(self, block, parent=None):
        """
        Recursive tree code execution

        Parameters:
            block: block to execute
            parent: block one level higher or none(if top-level)
        
        Returns:
            Return value depends on the block content
        """

        
        # Dictionary of handlers for every block type implemented
        HANDLERS = {
            TerminalCtx:            handle_terminal,
            StatementCtx:           handle_statement,
            ObsDeclCtx:             handle_obs_declaration,
            NumExprCtx:             handle_number_expression,
            IoStmtCtx:              handle_io_statement,
            VarExprCtx:             handle_variable_expression,
            PlaceMemberCtx:         handle_place_member,
            FunctionDeclCtx:        handle_function_declaration,
            ParamListCtx:           handle_param_list,
            ParamCtx:               handle_param,
            BlockCtx:               handle_block_ctx,
            ObsDefCtx:              handle_obs_definition,
            StrExprCtx:             handle_string,
            FunctionCallStmtCtx:    handle_function_call,
            FunctionCallExprCtx:    handle_function_call,
            ArgListCtx:             handle_arg_list,
            ForStmtCtx:             handle_for_loop,
            PowExprCtx:             handle_power,
            FormatCtx:              handle_format,
            IfStmtCtx:              handle_if,
            RelExprContext:         handle_rel_comp,
            AddSubExprContext:      handle_add_sub,
            
            MulDivModExprCtx:       handle_mul_div_mod,
            EqExprCtx:              handle_eq_comp,
            AndExprCtx:             handle_and,
            OrExprCtx:              handle_or,
            BoolExprCtx:            handle_bool,
            ParenExprCtx:           handle_parentheses,
            ConstraintCtx:          handle_constraint,
            AssigmentStmtCtx:       handle_assigment,
            QLangParser.NumDeclContext: handle_num_declaration,
            
            #################### Operators ####################
            # Not
            NotExprContext:         handle_not,
            # Minus
            MinusExprCtx:           handle_minus,
            # Plus
            PlusExprCtx:            handle_plus,    
            # Pre-post increment and decrement
            PreDecrementCtx:        handle_pre_decrement,
            PostDecrementCtx:       handle_post_decrement,
            PreIncrementCtx:        handle_pre_increment,
            PostIncrementCtx:       handle_post_increment,
            # Assignment expr
            AssignExprCtx:          handle_assignment_expr,
            # Plus equal
            PlusEqExprCtx:          handle_plus_eq_op,
            # Minus equal
            MinusEqExprCtx:         handle_minus_eq_op,
            # Mul equal
            MulEqExprCtx:           handle_mul_eq_op,
            # Div equal
            DivEqExprCtx:           handle_div_eq_op,
            # Mod equal
            ModEqExprCtx:           handle_mod_eq_op,
            # Pow equal
            PowEqExprCtx:           handle_pow_eq_op,
            # And equal
            AndEqExprCtx:           handle_and_eq_op,
            # Or equal
            OrEqExprCtx:            handle_or_eq_op



        }
        pos = ScriptErrors.Position.extract(block)

        # scan handlers for given block instance
        try:
            for type in HANDLERS.keys():
                if isinstance(block, type):
                    # Handler found, send the block to it
                    handle_args = (self, block, parent, pos)
                    return HANDLERS[type](*handle_args)
        except AssignmentToExpressionException as e:
            e.show(self.script_errors)
            exit()
        except DivideByZeroException as e:
            e.show(self.script_errors)
            exit()
        except ModuloOverZeroException as e:
            e.show(self.script_errors)
            exit()

        # Handler not found show error and exit
        log(PLACE, FATAL, "Handler for block not found, type: " + block.__class__.__name__)
        exit()

    def process_target(self):
        """
        Place execution entry point
        """
        sys.setrecursionlimit(4_000_000)
        sys.stdout.reconfigure(encoding='utf-8')

        # Open console with title that includes place's name
        self.console = Console("Place: " + self.name)
        if(self.test_mode):
            self.console.enable_test_mode()
        self.console.launch()

        # For some unknown reason not global place ends up in a double list
        if len(self.block) > 0 and type(self.block[0]) is list:
            self.block = self.block[0]

        # Reconstruct place decl for the parser to not parse every member individually
        place_text = "place " + self.name + "{\n"

        # Add every top-level block of code
        for bl in self.block:
            place_text += bl + "\n"

        place_text += "};"

        input_stream = InputStream(place_text)
        lexer = QLangLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = QLangParser(token_stream)
        tree = parser.placeDecl()

        for place_member in tree.placeMember():
            member = place_member.getChild(0) 
            self.handle_block(member, None)

        

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



    


