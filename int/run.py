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
        
        # store error info 
        error_entry = {
            "line": line,
            "start_col": start_col,
            "end_col" : end_col,
            "message": msg,
            "recognizer" : recognizer,
            "offendingSymbol": offendingSymbol,
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


def main():
    global TEST_MODE
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
    print("Parsing started")
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
        return
    
    log_test("SYNTAX_ERRORS=0")
    print("No errors found")

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
