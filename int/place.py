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

from .logger import log, PLACE, INFO, FATAL, enable_test_mode

from antlr4 import *
from antlr4.tree.Tree import TerminalNode
from .QLang.QLangLexer import QLangLexer
from .QLang.QLangParser import QLangParser
import traceback

BinaryFromListExprContext = QLangParser.BinaryFromListExprContext
BinaryToListExprContext = QLangParser.BinaryToListExprContext
FloatCastExprContext = QLangParser.FloatCastExprContext

######################## EXCEPTIONS #############################
from .exception.exit_exception import ExitException

######################## CONTEXT HANDLERS #############################
from .context.statement.statement              import handle_statement

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

##### TIME #####
from .context.time.wait_stmt              import handle_wait_stmt
from .context.time.time_unit          import handle_time_unit

from .context.io.io_statement           import handle_io_statement
from .context.expression.variable_expression    import handle_variable_expression
from .context.expression.type_expr             import handle_type_expr
from .context.place_member           import handle_place_member
from .context.function.function_declaration   import handle_function_declaration
from .context.function.param_list             import handle_param_list
from .context.function.param                  import handle_param
from .context.block                  import handle_block_ctx
from .context.string                 import handle_string
from .context.function.function_call          import handle_function_call
from .context.function.arg_list               import handle_arg_list
from .context.control.for_loop               import handle_for_loop
from .context.control.while_loop             import handle_while
from .context.control.iterate_loop           import handle_iterate

from .context.math.power                  import handle_power
from .context.io.format                 import handle_format
from .context.control.if_condition           import handle_if, handle_short_if
from .context.operator.rel_comp               import handle_rel_comp
from .context.operator.binary_conversion      import handle_binary_from_list, handle_binary_to_list
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
from .context.math.minus_op               import handle_minus
from .context.operator.pre_post               import handle_pre_decrement, handle_post_decrement
from .context.operator.pre_post               import handle_pre_increment, handle_post_increment
from .context.math.plus_op                import handle_plus
from .context.variable.assignment_expr        import handle_assignment_expr
from .context.operator.float_cast             import handle_float_cast
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

from .context.statement.continue_break import handle_continue, handle_break

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
        self.packet_log_enabled = False
        
    def enable_test_mode(self):
        self.test_mode = True

    def add_code(self, code: Any, start_line: int = None):
        """
        Adds code to this place

        Parameters:
            code (Any): code to add to this place
            start_line (int | None): Optional starting line from the original input
        """
        if start_line is None:
            self.block.append(code)
        else:
            self.block.append((code, start_line))

    def has_code(self) -> bool:
        """
        Returns True when this place contains at least one top-level member.
        """
        return len(self.block) > 0

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
    
    def execute_block(self, block, parent=None):
        """
        Executes given block of code in the context of this place.
        """
        from .context.statement.continue_break import ContinueLoop

        if isinstance(block, BlockCtx):
            for child in self.handle_block(block, parent=parent):
                try:
                    self.handle_block(child, parent=block)
                except ContinueLoop:
                    return
        else:
            self.handle_block(block, parent=parent)

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

            ##### TIME #####
            timeUnitCtx:           handle_time_unit,
            waitStmtCtx:            handle_wait_stmt,



            breakStatementCtx:          handle_break,
            continueStatementCtx:       handle_continue,
            IoStmtCtx:              handle_io_statement,
            VarExprCtx:             handle_variable_expression,
            PlaceMemberCtx:         handle_place_member,
            FunctionDeclCtx:        handle_function_declaration,
            FunctionDeclStatementCtx: handle_function_declaration,
            ParamListCtx:           handle_param_list,
            ParamCtx:               handle_param,
            BlockCtx:               handle_block_ctx,
            StrExprCtx:             handle_string,
            FunctionCallStmtCtx:    handle_function_call,
            FunctionCallExprCtx:    handle_function_call,
            ArgListCtx:             handle_arg_list,
            ForStmtCtx:             handle_for_loop,
            WhileStmtCtx:           handle_while,
            IterateStmtCtx:         handle_iterate,
            PowExprCtx:             handle_power,
            FormatCtx:              handle_format,
            IfStmtCtx:              handle_if,
            ResetExprCtx:       handle_reset_expr,
            ShortIfExprCtx:     handle_short_if,
            RelExprContext:         handle_rel_comp,
            AddSubExprContext:      handle_add_sub,
            BinaryFromListExprContext: handle_binary_from_list,
            BinaryToListExprContext: handle_binary_to_list,
            
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
            # Float cast
            FloatCastExprContext:   handle_float_cast,
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

        if block is None:
            parent_type = parent.__class__.__name__ if parent is not None else "None"
            parent_text = parent.getText() if hasattr(parent, 'getText') else None
            msg = [
                f"handle_block received None, parent type: {parent_type}",
                f"Parent text: {parent_text}",
                "Stack:",
                *traceback.format_stack(limit=10)
            ]
            with open("debug_handle_block.log", "a", encoding="utf-8") as debug_file:
                debug_file.write("\n".join(str(x) for x in msg))
                debug_file.write("\n---\n")
            log(PLACE, FATAL, "handle_block received None, parent type: " + parent_type)
            if parent_text is not None:
                log(PLACE, FATAL, "Parent text: " + str(parent_text))
            log(PLACE, FATAL, "Stack:\n" + "\n".join(traceback.format_stack(limit=10)))
            exit()

        # scan handlers for given block instance
        try:
            for type in HANDLERS.keys():
                if isinstance(block, type):
                    # Handler found, send the block to it
                    handle_args = (self, block, parent, pos)
                    return HANDLERS[type](*handle_args)
        except ExitException as e:
            e.show(self.script_errors)
            exit()

        # print(block) # uncomment to debug which blocks are handled
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
            enable_test_mode()
            self.console.enable_test_mode()
        self.console.launch()

        # For some unknown reason not global place ends up in a double list
        if len(self.block) > 0 and type(self.block[0]) is list:
            self.block = self.block[0]

        # Reconstruct place decl for the parser to not parse every member individually
        place_text = "place " + self.name + "{\n"

        # Add every top-level block of code, preserving original blank lines
        prev_end_line = 0
        for bl in self.block:
            if isinstance(bl, tuple) and len(bl) == 2:
                code, start_line = bl
                gap = start_line - prev_end_line - 1
                if gap > 0:
                    place_text += "\n" * gap
                place_text += code + "\n"
                prev_end_line = start_line + code.count("\n")
            else:
                place_text += bl + "\n"

        place_text += "};"

        prev_offset = ScriptErrors.Position.LINE_OFFSET
        ScriptErrors.Position.LINE_OFFSET = -1
        try:
            input_stream = InputStream(place_text)
            lexer = QLangLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = QLangParser(token_stream)
            tree = parser.placeDecl()

            for place_member in tree.placeMember():
                member = place_member.getChild(0)
                self.handle_block(member, None)
        finally:
            ScriptErrors.Position.LINE_OFFSET = prev_offset

        if not self.console.test_mode:
            self.console.write("-----[END]-----\n")
            self.console.write("Press Return key to close...")
            self.console.read("")
            self.console.close()

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
        if not hasattr(self, "proc"):
            return
        self.proc.join()
        log(PLACE, INFO, f"Place {self.name} stopped")



    


