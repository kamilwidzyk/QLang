import sys
import json
from logger import init_log, log, logln, INIT, PLACE, log_level 
from logger import FATAL, ERROR, WARNING, SUCCESS, INFO, DEBUG


def load_json(path):
    logln(INIT, INFO, "Loading JSON tree...")
    try:
        json_content = open(path).read()
        tree = json.loads(json_content)
    except FileNotFoundError:
        logln(INIT, FATAL, "JSON input file not found")
        exit()
    except json.JSONDecodeError:
        logln(INIT, FATAL, "JSON input file: can't decode")

    logln(INIT, SUCCESS, "JSON tree loaded!")
    return tree


def load_script(path):
    logln(INIT, INFO, "Loading QLang script...")
    try:
        script = open(path).read()
    except FileNotFoundError:
        logln(INIT, FATAL, "QLang script file not found")
        exit()
    
    logln(INIT, SUCCESS, "QLang script loaded!")
    return script

def load_input_files():
    arg_len = len(sys.argv)
    if(arg_len != 3):
        logln(INIT, FATAL, "Required arguments missing!")
        logln(INIT, FATAL, "Args: <JSON tree path> <QLang script path>")
        exit()
    
    tree = load_json(sys.argv[1])
    script = load_script(sys.argv[2])

    return tree, script

def divideIntoPlaces(tree):
    """ 
    Divides original tree into places. 
    Code not in any place ends up in 'global' place.
    Therefore 'global' is not a valid place name.
    
    """
    logln(PLACE, INFO, "Dividing into places...")

    PROGRAM_CONTEXT = "ProgramContext"
    STATEMENT_CONTEXT = "StatementContext"
    PLACE_DECLARATION_CONTEXT = "PlaceDeclContext"

    
    places = {
        # placeID -> code inside
        "global": []
    }

    # Check if ProgramContext is at the start
    if(tree["type"] != PROGRAM_CONTEXT):
        logln(PLACE, FATAL, f"First node is not {PROGRAM_CONTEXT}")
        exit()

    # Extract second layer
    global_items = tree["children"]

    # Iterate second layer
    for global_item in global_items:
        if(global_item["type"] == "Terminal" and 
           global_item["text"] == "<EOF>"):
            continue
        # Extract third layer
        inside = global_item["children"][0]
        if(inside["type"] == PLACE_DECLARATION_CONTEXT):
            # this is a place declaration
            place_name = inside["children"][1]["text"]
            places[place_name] = inside["children"][3:]
        else:
            # this is something else -> put into global place
            places["global"].append(inside)

    logln(PLACE, DEBUG, f"Got places: {" ".join(places.keys())}")
    return places

def main():
    init_log()

    log_level(DEBUG)

    tree, script = load_input_files()

    places = divideIntoPlaces(tree)

    ### TODO: run every place at the same time(including 'global')
    

    
    



    

if __name__ == '__main__':
    main()