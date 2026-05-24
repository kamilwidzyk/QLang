from typing import Any, List
from multiprocessing import Process
import time
import re
from dataclasses import dataclass
import sys

from .script_errors import ScriptErrors
from .console import Console
from .consts import *
from .scope import ScopeManager
from .sim.client import QuantumClient

from .logger import log, PLACE, INFO, FATAL

from antlr4 import *
from antlr4.tree.Tree import TerminalNode
from .QLang.QLangLexer import QLangLexer
from .QLang.QLangParser import QLangParser

######################## EXCEPTIONS #############################
from .exception.assignment_to_expression import AssignmentToExpressionException
from .exception.divide_by_zero import DivideByZeroException
from .exception.modulo_over_zero import ModuloOverZeroException
from .exception.operator_type_mismatch import OperatorTypeMismatchException
from .exception.size_error import SizeErrorException
from .exception.trying_to_modify_const import TryingToModifyConstException
from .exception.variable_redefinition import VariableRedefiniotionException
from .exception.index_not_int import IndexNotIntException
from .exception.index_out_of_range import IndexOutOfRangeException

######################## CONTEXT HANDLERS #############################
from .context.statement              import handle_statement

##### VARIABLES #####
from .context.variable.declaration   import handle_variable_declaration, handle_const_variable_declaration
from .context.expression.size_expr   import handle_expression_size_expr, \
                                            handle_expression_size_getter

##### LIST #####
from .context.expression.list_expr import   handle_expression_list, \
                                            handle_expression_list_empty, \
                                            handle_expression_list_expr, \
                                            handle_expression_list_non_empty

##### NUMBERS #####
from .context.expression.int_number  import handle_expression_int_number
from .context.expression.number      import handle_expression_number



from .context.io.io_statement           import handle_io_statement
from .context.expression.variable_expression    import handle_variable_expression
from .context.expression.type_expr             import handle_type_expr
from .context.place_member           import handle_place_member
from .context.function.function_declaration   import handle_function_declaration
from .context.function.param_list             import handle_param_list
from .context.function.param                  import handle_param
from .context.block                  import handle_block_ctx
from .context.variable.obs_definition         import handle_obs_definition
from .context.string                 import handle_string
from .context.function.function_call          import handle_function_call
from .context.function.arg_list               import handle_arg_list
from .context.control.for_loop               import handle_for_loop
from .context.control.while_loop             import handle_while
from .context.math.power                  import handle_power
from .context.io.format                 import handle_format
from .context.control.if_condition           import handle_if, handle_short_if
from .context.operator.rel_comp               import handle_rel_comp
from .context.math.add_sub                import handle_add_sub
from .context.operator.not_op                 import handle_not
from .context.math.mul_div_mod            import handle_mul_div_mod
from .context.operator.eq_comp                import handle_eq_comp
from .context.math.logic.and_op                 import handle_and
from .context.math.logic.or_op                  import handle_or
from .context.expression.bool_val               import handle_bool
from .context.expression.null_val               import handle_null
from .context.expression.parentheses            import handle_parentheses
from .context.terminal               import handle_terminal
from .context.io.constraint             import handle_constraint
from .context.variable.assigment              import handle_assigment
from .context.variable.num_declaration        import handle_num_declaration
from .context.math.minus_op               import handle_minus
from .context.operator.pre_post               import handle_pre_decrement, handle_post_decrement
from .context.operator.pre_post               import handle_pre_increment, handle_post_increment
from .context.math.plus_op                import handle_plus
from .context.variable.assignment_expr        import handle_assignment_expr
from .context.math.plus_eq_op             import handle_plus_eq_op
from .context.math.minus_eq_op            import handle_minus_eq_op
from .context.math.mul_eq_op              import handle_mul_eq_op
from .context.math.div_eq_expr            import handle_div_eq_op
from .context.math.mod_eq_op              import handle_mod_eq_op
from .context.math.pow_eq_op              import handle_pow_eq_op
from .context.math.logic.and_eq_op              import handle_and_eq_op
from .context.math.logic.or_eq_op               import handle_or_eq_op
from .context.operator.reference import handle_reference
from .context.operator.reset import handle_reset_expr
from .context.quantum import handle_gate_statement, handle_measure_expr
from .context.operator.parent import handle_operator_parent
from .context.operator.const import handle_operator_const
from .context.network import handle_send_statement, handle_receive_declaration, handle_available_expression

class Place:
    """
    Represents one place.

    Every instance of place starts a separate process to execute its code in.
    """
    name: str = None
    block: List = []
    script_errors: ScriptErrors
    declared_at: ScriptErrors.Position
    scopes: ScopeManager
    console: Console
    test_mode: bool = False


    def __init__(self, name: str, script_errors: ScriptErrors, 
                 declared_at: ScriptErrors.Position):
        """
        Initializes the place with a name

        Parameters:
            name (str): Place name, specified by the code
            script_errors (ScriptErrors): instance of class for displaying errors
        """
        self.name = name
        self.script_errors = script_errors
        self.block = []
        self.declared_at = declared_at
        self.scopes = ScopeManager()
        self.quantum_client = None
        self.quantum_network = None
        self.quantum_network = None
        
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

            ##### VARIABLES #####
            VarDeclCtx:             handle_variable_declaration,
            ConstDeclarationCtx:    handle_const_variable_declaration,
            SizeGetterCtx:          handle_expression_size_getter,
            SizeGetterExprCtx:      handle_expression_size_expr,
            GateStmtCtx:            handle_gate_statement,
            MeasureExprCtx:         handle_measure_expr,

            ##### LIST #####
            ListExprCtx:            handle_expression_list_expr,
            TypeExprCtx:            handle_type_expr,
            ListCtx:                handle_expression_list,
            EmptyListCtx:           handle_expression_list_empty,
            NonEmptyListCtx:        handle_expression_list_non_empty,

            ##### NUMBERS #####
            NumExprCtx:             handle_expression_number,
            IntNumExprCtx:          handle_expression_int_number,
            NumCastExprCtx:         handle_function_call,



            IoStmtCtx:              handle_io_statement,
            VarExprCtx:             handle_variable_expression,
            PlaceMemberCtx:         handle_place_member,
            FunctionDeclCtx:        handle_function_declaration,
            ParamListCtx:           handle_param_list,
            ParamCtx:               handle_param,
            BlockCtx:               handle_block_ctx,
            StrExprCtx:             handle_string,
            FunctionCallStmtCtx:    handle_function_call,
            FunctionCallExprCtx:    handle_function_call,
            ArgListCtx:             handle_arg_list,
            ForStmtCtx:             handle_for_loop,
            WhileStmtCtx:           handle_while,
            PowExprCtx:             handle_power,
            FormatCtx:              handle_format,
            IfStmtCtx:              handle_if,
            ResetExprCtx:       handle_reset_expr,
            ShortIfExprCtx:     handle_short_if,
            RelExprContext:         handle_rel_comp,
            AddSubExprContext:      handle_add_sub,
            
            MulDivModExprCtx:       handle_mul_div_mod,
            EqExprCtx:              handle_eq_comp,
            AndExprCtx:             handle_and,
            OrExprCtx:              handle_or,
            BoolExprCtx:            handle_bool,
            NullExprCtx:            handle_null,
            ParenExprCtx:           handle_parentheses,
            ConstraintCtx:          handle_constraint,
            AssigmentStmtCtx:       handle_assigment,
            SendStmtCtx:            handle_send_statement,
            ReceiveDeclCtx:         handle_receive_declaration,
            AvailableExprContext:   handle_available_expression,
            
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
            OrEqExprCtx:            handle_or_eq_op,
            # Reference '@'
            ReferenceCtx:           handle_reference,
            # Parent '^'
            ParentExprCtx:          handle_operator_parent,
            # Operator const
            ConstDeclCtx:           handle_operator_const



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
        except TryingToModifyConstException as e:
            e.show(self.script_errors)
            exit()
        except ModuloOverZeroException as e:
            e.show(self.script_errors)
            exit()
        except OperatorTypeMismatchException as e:
            e.show(self.script_errors)
            exit()
        except SizeErrorException as e:
            e.show(self.script_errors)
            exit()
        except VariableRedefiniotionException as e:
            e.show(self.script_errors)
            exit()
        except IndexNotIntException as e:
            e.show(self.script_errors)
            exit()
        except IndexOutOfRangeException as e:
            e.show(self.script_errors)
            exit()

        print(block)
        # Handler not found show error and exit
        log(PLACE, FATAL, "Handler for block not found, type: " + block.__class__.__name__)
        exit()

    def process_target(self, quantum_network=None, quantum_command_queue=None, quantum_response_queue=None):
        """
        Place execution entry point
        """
        sys.setrecursionlimit(4_000_000)
        sys.stdout.reconfigure(encoding='utf-8')
        self.quantum_network = quantum_network
        if quantum_command_queue is not None and quantum_response_queue is not None:
            self.quantum_client = QuantumClient(self.name, quantum_command_queue, quantum_response_queue)

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

        

    def run(self, quantum_network=None, quantum_command_queue=None, quantum_response_queue=None):
        """
        Starts execution of this place inside a separate process
        """
        self.proc = Process(
            target=self.process_target,
            args=(quantum_network, quantum_command_queue, quantum_response_queue),
        )
        self.proc.start()
        log(PLACE, INFO, f"Place {self.name} started")

    def wait_for_end(self):
        """
        Waits for execution to finish
        """
        self.proc.join()
        log(PLACE, INFO, f"Place {self.name} stopped")



    


