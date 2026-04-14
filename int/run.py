import sys

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from .QLang.QLangLexer import QLangLexer
from .QLang.QLangParser import QLangParser

from .logger import init_log, log, log_level 
from .logger import INIT, PLACE
from .logger import FATAL, ERROR, WARNING, SUCCESS, INFO, DEBUG, NOTHING

from .load import load_input_files
from .script_errors import ScriptErrors

from .places import divideIntoPlaces, Places

from .network import QuantumNetwork, create_quantum_network

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
    




def main():
    # Start terminal logger
    log_level(DEBUG)
    init_log()

    # Get filename and extract only the name
    input_filename = sys.argv[1]
    input_name = ("".join(input_filename.split(".")[:-1])).split("\\")[-1]

    # Open file, read it(text is needed later)
    input_text = str(open(input_filename, encoding='utf-8').read())
    input_stream = InputStream(input_text)

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
        for err in error_listener.errors:
            print(f"Error at Line {err['line']}, Col {err['start_col']}-{err['end_col']}: {err['message']}")
        return
    
    print("No errors found")

    # Prepare for interpreter start

    # Create a quantum network for communication between places
    network, manager = create_quantum_network()

    # Scan the tree and divide the code into multiple places that will run in parrael
    places = divideIntoPlaces(tree, scriptErrors, network, parser)

    # Start every place in separate process
    places.run()

    # Wait for all places to finish execution
    places.wait_for_end()








    

if __name__ == '__main__':
    main()