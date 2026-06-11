import os
import sys
import multiprocessing

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from .QLang.QLangLexer import QLangLexer
from .QLang.QLangParser import QLangParser

from .imports import preprocess_text
from .logger import init_log, log, log_level, log_test, enable_test_mode
from .logger import INIT
from .logger import WARNING, DEBUG

from .script_errors import ScriptErrors

from .places import divideIntoPlaces
from .network import create_quantum_network
from .sim.server import start_server

from .consts import *

import re

class QLangErrorListener(ErrorListener):
    def __init__(self):
        super(QLangErrorListener, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # by default only the start position is known
        start_col = column
        end_col = column

        # is offendingSymbol is known then we also have the stop position
        if offendingSymbol is not None:
            length = offendingSymbol.stop - offendingSymbol.start
            end_col = start_col + length + 1

        no_viable_alternative_at_input_pattern = "^no viable alternative at input '.*'$"

        stack = []
        context_list = ""

        ctx = getattr(recognizer, "_ctx", None)
        if ctx is None:
            context_list += " [NO CONTEXT]"
        while(ctx):
            context_list += f" [{type(ctx).__name__}]"
            stack.append(ctx)
            ctx = ctx.parentCtx

        

        def get_stack(index):
            nonlocal stack
            if index < len(stack):
                return stack[index]
            return None

        def is_stack(index, obj):
            item = get_stack(index)
            if item:
                return isinstance(item, obj)
            return False
        
        def in_stack(obj):
            for i in range(len(stack)):
                if is_stack(i, obj):
                    return True
            return False
        
        title = ""

        # For now there are no 'else' in inner if's
        # They will be added later - now they will eat the unhandled messages

        if re.match(no_viable_alternative_at_input_pattern, msg) or \
            (msg.startswith("mismatched input ';' expecting {") and len(msg) > 60):
            title = "SomethingMissing"
            if is_stack(0, StatementCtx):
                msg = "What is this supposed to mean?"
            elif is_stack(0, QLangParser.ListContext):
                msg = "You sure this list is correct?"
            else:
                msg = "I think there should be something more."
            start_col -= 1
            end_col -= 1
        elif msg.startswith("extraneous input '<EOF>' expecting "):
            title = "LeftOpen"
            msg = "You forgot to close some brackets."
        elif msg.startswith("extraneous input '}' expecting "):
            title = "ClosedAlready"
            msg = "No open braces to close here."
        elif msg.startswith("extraneous input 'else if' expecting '('"):
            title = "NoIf"
            msg = "Where is the IF part of this if?"
        elif msg.startswith("extraneous input '->' expecting ';'"):
            title = "OneSeat"
            msg = "This gate has room only for one."
        elif msg.startswith("mismatched input '=' expecting ';'") or msg.startswith("extraneous input '=' expecting "):
            title = "NoAssign4You"
            if is_stack(0, QLangParser.ConstDeclarationContext):
                msg = "Const with nothing in it. Intresting."
            elif is_stack(0, QLangParser.ReturnStatementContext):
                msg = "What is that 'return' doing here?"
            else:
                msg = "To what I'm supposed to assign it?"
        elif msg.startswith("mismatched input ';' expecting {')', ','}"):
            title = "MakeYourMind"
            msg = "If you have some more args tell me."
        elif msg.startswith("missing ';' at '<EOF>'"):
            title = "WrongEnd"
            msg = "Something should end here but not the file. Try adding a ';'."
        elif msg.startswith("extraneous input 'else' expecting "):
            title = "GoodButBad"
            msg = "Good that you have alternatives, but I don't want to know them."
        elif re.match("extraneous input '.*' expecting ';'", msg):
            title = "NotHere"
            msg = f"Find some better place for '{getattr(offendingSymbol, "text", "unknown")}'."
        elif msg.startswith("extraneous input 'function' expecting "):
            title = "CheckDeclaration"
            msg = f"Make sure the declaration is all right."
        elif msg.startswith("extraneous input 'available' expecting "):
            title = "NoAssign4You"
            msg = f"Where should I put the result?"
        elif msg.startswith("mismatched input 'available' expecting "):
            title = "BadThink"
            msg = f"You think this should be here? I don't."
        elif msg.startswith("mismatched input 'break' expecting "):
            title = "NothingToBreak"
            msg = f"There is nothing to break!"
        elif msg.startswith("extraneous input 'else if' expecting "):
            title = "BrokenIf"
            msg = f"If not structured correctly, fix it!"
        elif msg.startswith("mismatched input '{' expecting '('"):
            if is_stack(0, IfStmtCtx):
                title = "BrokenIf"  
                msg = f"Maybe check the condition? I don't know."
            else:
                title = "BadBlock"
                msg = f"Not so good place to start a block."
        elif msg.startswith("missing ID at 'to'"):
            if is_stack(0, ForStmtCtx):
                title = "BrokenFor"
                msg = f"No end value specified"
            else:
                title = "NoDestination"
                msg = f"Where are you going to?"
        elif msg.startswith("mismatched input '{' expecting 'to'"):
            if is_stack(0, ForStmtCtx):
                title = "BrokenFor"
                msg = f"Check if you specified the end value."
            else:
                title = "BadBlock"
                msg = f"There should be something before that block"
        elif msg.startswith("missing {STRING, ID} at ';'"):
            if is_stack(0, (QLangParser.AvailableFilterContext, 
                            QLangParser.ReceiveFilterContext,
                            QLangParser.SendStmtContext)):
                title = "NoSource"
                msg = f"There should be a place name."
        elif re.match("mismatched input '.*' expecting STRING", msg):
            title = "NoString"
            msg = f"Forgotten \" \"?"
        elif msg.startswith("missing STRING at ';'"):
            if is_stack(0, QLangParser.SendStmtContext):
                title = "NoName"
                msg = f"Give the packet a name."
        elif msg.startswith("extraneous input 'to' expecting "):
            if in_stack(QLangParser.SendStmtContext):
                title = "NoVariable"
                msg = f"There should be a variable name."
        elif re.match("missing '\\(' at '.*'", msg):
            title = "NoParen"
            if is_stack(0, QLangParser.IfStmtContext):
                msg = f"You forgotten '(' after if."
            elif is_stack(0, QLangParser.WhileStmtContext):
                msg = f"You forgotten '(' after while."
            elif is_stack(0, QLangParser.IoStmtContext):
                msg = f"You forgotten '(' after IO function."
        elif re.match("missing '\\)' at '.*'", msg):
            title = "LeftOpen"
            if is_stack(0, QLangParser.IfStmtContext):
                msg = f"if's '(' was not closed"
            elif is_stack(0, QLangParser.ParenExprContext):
                msg = "'(' was not closed"
            elif is_stack(0, QLangParser.WhileStmtContext):
                msg = "while's '(' was not closed"
        elif msg.startswith("extraneous input '{' expecting ") or msg.startswith("mismatched input '{' expecting "):
            if is_stack(0, QLangParser.ExprContext) and is_stack(1, QLangParser.ForStmtContext):
                title = "NoStep"
                msg = f"Where is the step value?"
        elif re.match("missing 'from' at '.*'", msg):
            if is_stack(0, QLangParser.ForStmtContext):
                title = "FromWhere"
                msg = f"From where you want to start?"
        elif msg.startswith("missing ID at 'from'"):
            if is_stack(0, QLangParser.ForStmtContext):
                title = "NoVariable"
                msg = f"Did you forget the specify the variable?"
        elif msg.startswith("mismatched input 'step' expecting 'to'"):
            if is_stack(0, QLangParser.ForStmtContext):
                title = "NoEnd"
                msg = f"Where should I stop?"
        elif msg.startswith("mismatched input '<EOF>' expecting "):
            if is_stack(0, QLangParser.IfStmtContext):
                title = "BrokenIf"
                msg = f"Something missing in that if."
            elif is_stack(0, QLangParser.BlockContext):
                title = "BrokenBlock"
                msg = f"A block needs to start here"
            elif is_stack(0, (QLangParser.ListContext, QLangParser.NonEmptyListContext, QLangParser.EmptyListContext)):
                title = "BrokenList"
                msg = f"Make sure all '[' are closed and items seperated by ','."
            else:
                title = "BrokenSomething"
                msg = f"The file should not end here!"
        elif msg.startswith("mismatched input ')' expecting "):
            if is_stack(1, QLangParser.IfStmtContext):
                title = "BrokenIf"
                msg = f"Broken if condition."
            else:
                title = "CloseWhat"
                msg = f"There is no '(' to close."
        elif re.match("extraneous input '.*' expecting {'index', '{'}", msg):
            if is_stack(0, QLangParser.IterateStmtContext):
                title = "BrokenIterate"
                msg = f"You meant index?, or block start?"
        elif msg.startswith("missing ID at '{'"):
            if is_stack(0, QLangParser.IterateStmtContext):
                title = "BrokenIterate"
                msg = f"Item or index name missing."
            elif is_stack(0, QLangParser.PlaceDeclContext):
                title = "BadPlace"
                msg = "You forgot to name the place"
        elif re.match("missing 'as' at '.*'", msg):
            if is_stack(0, QLangParser.IterateStmtContext):
                title = "BrokenIterate"
                msg = f"Did you forget 'as'?"
        elif re.match("missing '{' at '.*'", msg) or msg.startswith("mismatched input '<EOF>' expecting '{'"):
            if is_stack(0, QLangParser.BlockContext):
                title = "BrokenBlock"
                msg = f"A block needs to start here"
        elif msg.startswith("mismatched input ';' expecting {'[', '='}") or msg.startswith("mismatched input ';' expecting {'[', '='}"):
            if is_stack(0, QLangParser.ConstAssignContext):
                title = "WhyConst"
                msg = f"How will you assign a value later to it?"
        elif re.match("mismatched input '.*' expecting {'text', 'state', 'obs', 'num', 'any', ID}", msg):
            if is_stack(0, QLangParser.ConstDeclContext):
                title = "NoType"
                msg = f"I can't guess the type of this const."
        elif msg.startswith("mismatched input '=' expecting '{'"):
            if is_stack(0, QLangParser.PlaceDeclContext):
                title = "NoPlaceAssign"
                msg = f"Can't assign to a place. A block should start here."
        elif msg.startswith("extraneous input ',' expecting ID"):
            if is_stack(0, QLangParser.VarAssignContext):
                title = "TooMuch"
                msg = f"Did you put too much ','?"
        elif msg.startswith("missing ';' at '['"):
            if is_stack(0, QLangParser.VarDeclarationContext):
                title = "Mess"
                msg = "Fix that list."
        elif msg.startswith("extraneous input ',' expecting "):
            title = "NotComma"
            msg = "What is that ',' doing here?"
        elif msg.startswith("mismatched input ';' expecting {'[', ID}"):
            title = "MeasureWhat"
            msg = "Specify what you want to measure"
        elif msg.startswith("extraneous input '*' expecting "):
            title = "MultiplyWhat"
            msg = "There is nothing to multiply."
        elif msg.startswith("missing ID at ';'"):
            if is_stack(1, QLangParser.ResetExprContext):
                title = "ResetWhat"
                msg = "Tell me what you want to reset."
            elif is_stack(0, QLangParser.SizeGetterContext):
                title = "SizeWhat"
                msg = "Tell me what you need the size of."    
            elif is_stack(1, QLangParser.GateStmtContext):
                title = "BadGate"
                msg = "On what should I apply this gate?"    
        elif msg.startswith("extraneous input ':' expecting "):
            if is_stack(1, QLangParser.ShortIfExprContext):
                title = "NoYes"
                msg = "What should I do when the condition is true?"
        elif msg.startswith("mismatched input '...' expecting "):
            title = "..."
            msg = "Allowed only in function declaration(once! and last!)."
        elif re.match("token recognition error at: '\".*'", msg):
            title = "???"
            msg = "What is this? A not closed string?"
        elif msg.startswith("extraneous input '||' expecting "):
            title = "YouSure"
            msg = "You sure this should be here?"
        elif msg.startswith("missing ')' at ';'"):
            title = "LeftOpen"
            msg = "You forgot to close '(' before ending your statement."
        elif msg.startswith("extraneous input '..' expecting {']', ','}"):
            title = "BrokenRange"
            msg = "If this is a range, then make it correct."
        elif re.match("extraneous input '.*' expecting {']', ','}", msg):
            title = "NoComma"
            msg = "Did you forget a comma between values?"
        elif msg.startswith("mismatched input '@'"):
            title = "BadReference"
            msg = "That's not how reference operator is used."
        elif msg.startswith("missing ID at ')'"):
            if is_stack(0, QLangParser.ReferenceContext):
                title = "BadReference"
                msg = "Is that a reference to nothing?"
        elif msg.startswith("missing ID at ','"):
            if is_stack(0, QLangParser.IoStmtContext):
                title = "BadIO"
                msg = "Did you forget the variable?"
        elif re.match("missing '\\(' at '.*'", msg):
            if is_stack(0, QLangParser.IoStmtContext):
                title = "BadIO"
                msg = "Is there '(' before the variable?"
        elif re.match("extraneous input '.*' expecting {'\\)', ','}", msg):
            title = "BadArgs"
            msg = "Did you forget to put ',' between args? or close '('?"
        elif re.match("mismatched input '.*' expecting ID", msg):
            title = "BadName"
            if is_stack(0, QLangParser.PlaceDeclContext):
                msg = "Place can't be named like that"
            else:
                msg = "This is not a valid name"
        elif msg.startswith("mismatched input ']' expecting "):
            title = "BadList"
            msg = "You sure this is the of the list?"
        elif msg.startswith("mismatched input ';' expecting {']', ','}") or \
             msg.startswith("mismatched input '<EOF>' expecting {']', ','}"):
            title = "BadList"
            msg = "Make sure all '[' are closed and items separated with ','."
        elif msg.startswith("mismatched input 'stepy' expecting {'step', '{'}"):
            title = "BadFor"
            msg = "Is this a typo in 'step'?"
        elif re.match("missing 'to' at '.*'", msg):
            if is_stack(0, QLangParser.ForStmtContext):
                title = "BadFor"
                msg = "No end - are we going to infinity?"
        elif msg.startswith("extraneous input 'as' expecting "):
            if is_stack(1, QLangParser.IterateStmtContext):
                title = "BadIterate"
                msg = "What am I supposed to iterate?"
        elif re.match("extraneous input '.*' expecting '{'", msg):
            if is_stack(0, QLangParser.BlockContext):
                title = "BadBlock"
                msg = "A block should begin here"
            elif is_stack(0, QLangParser.PlaceDeclContext):
                title = "BadPlace"
                msg = "Place's block should start here"
        elif re.match("missing '->' at '.*'", msg) or \
             re.match("mismatched input '.*' expecting '->'", msg):
            if is_stack(0, QLangParser.GateStmtContext):
                title = "BadGate"
                msg = "This gate requires two qubits separated by '->'."
        elif msg.startswith("extraneous input '->' expecting ID"):
            title = "BadGate"
            msg = "Is '->' outside a two qubit gate?"
        elif msg.startswith("extraneous input '?' expecting "):
            title = "???"
            msg = "What happend here?"
        elif re.match("missing ':' at '.*'", msg):
            if is_stack(0, QLangParser.ShortIfExprContext):
                title = "BadShortIf"
                msg = "Did you forget ':'?"
        
        
        
        
        

        
        # Default message when can't handle it
        # Comment out to see ANTLR output in messages
        #if title == "":
        #    title = "Unknown"
        #    msg = "Fix your mess, please."

        
        
        # store error info 
        error_entry = {
            "line": line,
            "start_col": start_col,
            "end_col" : end_col,
            "message": msg,
            "recognizer" : recognizer,
            "offendingSymbol": offendingSymbol,
            "title": title,
            "stack": stack,
            "e": e
        }
        self.errors.append(error_entry)

    def has_errors(self) -> bool:
        """
        Check if any erros occured

        Returns:
            True: some error occured
            False: no errors
        """
        return len(self.errors) > 0
    

TEST_MODE = False 
SYNTAX_CHECK_MODE = False


def main():
    global TEST_MODE, SYNTAX_CHECK_MODE
    sys.stdout.reconfigure(encoding='utf-8')
    # Start terminal logger
    log_level(DEBUG)
    init_log()

    # Get filename and extract only the name
    input_filename = sys.argv[1]
    input_name = ("".join(input_filename.split(".")[:-1])).split("\\")[-1]

    # Check the second arg for 'TEST_MODE'
    if len(sys.argv) > 2 and sys.argv[2] == "TEST_MODE":
        TEST_MODE = True
        log(INIT, WARNING, "Running in TEST MODE!")
        enable_test_mode()

    # Check the second arg for 'SYNTAX_MODE'
    if len(sys.argv) > 2 and sys.argv[2] == "SYNTAX_MODE":
        SYNTAX_CHECK_MODE = True
        TEST_MODE = True
        enable_test_mode()
        log(INIT, WARNING, "Running in SYNTAX MODE! The interpreter will exit after the syntax check.")


    

    log_test("SYS_ARGV=" + str(sys.argv))

    # Open file, read it(text is needed later)
    input_text = str(open(input_filename, encoding='utf-8').read())
    input_dir = os.path.dirname(os.path.abspath(input_filename))
    processed_text = preprocess_text(input_text, input_dir)
    input_stream = InputStream(processed_text)

    log_test("INPUT_TEXT=" + processed_text)

    # Create error listener for lexer and parser
    error_listener = QLangErrorListener()

    # Setup lexer
    lexer = QLangLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)

    # Setup parser
    stream = CommonTokenStream(lexer)
    parser = QLangParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    
    # Start the parse
    tree = parser.program()

    # Create error logging class instane
    scriptErrors = ScriptErrors(input_text)

    # If any syntax errors found -> show then and stop
    if error_listener.has_errors():
        print("------ SYNTAX ERRORS FOUND -----------")
        # TODO: There will be the script errors class called
        log_test("SYNTAX_ERRORS=1")

        for i, err in enumerate(error_listener.errors):
            print(f"Error at Line {err['line']}, Col {err['start_col']}-{err['end_col']}: {err['message']}")
            log_test(f"SYNTAX_ERROR_LINE[{i}]={err['line']}")
            log_test(f"SYNTAX_ERROR_COL_START[{i}]={err['start_col']}")
            log_test(f"SYNTAX_ERROR_COL_END[{i}]={err['end_col']}")
            log_test(f"SYNTAX_ERROR_MESSAGE[{i}]={err['message']}")
            log_test(f"SYNTAX_ERROR_TITLE[{i}]={err['title']}")
            log_test(f"SYNTAX_ERROR_STACK[{i}]={err['stack']}")

        return
    
    log_test("SYNTAX_ERRORS=0")
    if(SYNTAX_CHECK_MODE): # exit if SYNTAX_CHECK_MODE is active
        log(INIT, WARNING, "SYNTAX MODE active, exiting now!")
        exit()

    # Scan the tree and divide the code into multiple places that will run in parrael
    places = divideIntoPlaces(tree, scriptErrors, parser)
    for place in places.places:
        log_test(f"PLACE_NAME={place}")
        log_test(f"PLACE_CODE={places.places[place].block}")
    log_test("PLACE_END")

    quantum_network, quantum_network_manager = create_quantum_network()
    quantum_network.valid_places = set(places.list_names())
    places.quantum_network = quantum_network
    quantum_command_queue = multiprocessing.Queue()
    quantum_response_queues = {
        place_name: multiprocessing.Queue()
        for place_name in places.list_names()
    }
    quantum_server_process = multiprocessing.Process(
        target=start_server,
        args=(quantum_command_queue, quantum_response_queues),
        name="QuantumSimulatorServer",
    )
    quantum_server_process.start()
    places.set_quantum_channels(quantum_command_queue, quantum_response_queues)

    try:
        # Start every place in separate process
        if(TEST_MODE):
            places.enable_test_mode()
        places.run()

        log_test("ALL_PLACES_STARTED")

        # Wait for all places to finish execution
        places.wait_for_end()

        log_test("ALL_PLACES_FINISHED")
    finally:
        quantum_command_queue.put(None)
        quantum_server_process.join(timeout=10.0)
        if quantum_server_process.is_alive():
            quantum_server_process.terminate()
            quantum_server_process.join(timeout=10.0)








    

if __name__ == '__main__':
    main()
