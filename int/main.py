import sys
import json
from typing import List, Dict
import re

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

    # Load input files
    tree, script = load_input_files()

    # Start a quantum network used for communication between places
    network, manager = create_quantum_network()
    # Split script into places that will run in parrael
    scriptErrors = ScriptErrors(script)
    places = divideIntoPlaces(tree, scriptErrors, network)

    

    # Start every place in separate processes
    places.run()
    places.wait_for_end()



    
    



    

if __name__ == '__main__':
    main()