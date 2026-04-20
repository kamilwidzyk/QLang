import sys
import json
from typing import List, Dict
import re
import antlr4

from .QLang.QLangLexer import QLangLexer
from .QLang.QLangParser import QLangParser

from .logger import init_log, log, log_level
from .logger import INIT, PLACE
from .logger import FATAL, ERROR, WARNING, SUCCESS, INFO, DEBUG, NOTHING

from .load import load_input_files
from .script_errors import ScriptErrors

from .places import divideIntoPlaces, Places
from .network import QuantumNetwork, create_quantum_network

def main():
    # Init logging
    log_level(DEBUG)
    init_log()

    # Load input files (json_tree to słownik JSON, script to tekst programu)
    json_tree, script = load_input_files()

    # Parse script to ANTLR tree
    input_stream = antlr4.InputStream(script)
    lexer = QLangLexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = QLangParser(token_stream)
    antlr_tree = parser.program()

    # Start a quantum network used for communication between places
    network, manager = create_quantum_network()

    # Split script into places that will run in parrael
    scriptErrors = ScriptErrors(script)

    places = divideIntoPlaces(antlr_tree, scriptErrors, network) # <------- Zamiast json_tree przekazujemy antlr_tree

    # Start every place in separate processes
    places.run()

    # Wait for all places to finish execution
    places.wait_for_end()


if __name__ == '__main__':
    main()

