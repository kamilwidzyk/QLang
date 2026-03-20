import sys
import json
from typing import List, Dict
import re

from logger import init_log, log, log_level 
from logger import INIT, PLACE
from logger import FATAL, ERROR, WARNING, SUCCESS, INFO, DEBUG, NOTHING

from load import load_input_files
from script_errors import ScriptErrors

def divideIntoPlaces(tree, scriptErrors: ScriptErrors) -> Dict[str, List]:
    """ 
    Divides original tree into places. 
    Code not in any place ends up in 'global' place.
    Therefore 'global' is not a valid place name.
    
    Place name can only contain a-z A-Z 0-9 _ 

    ProgramContext
        TopLevelItemContext
            PlaceDeclContext
                Terminal place
                Terminal <name>
                Terminal {
                    ... (this is the place content)
                Terminal }
        ...
    """
    log(PLACE, INFO, "Dividing into places...", end=False)

    PROGRAM_CONTEXT = "ProgramContext"
    STATEMENT_CONTEXT = "StatementContext"
    PLACE_DECLARATION_CONTEXT = "PlaceDeclContext"
    TOP_LEVEL_ITEM_CONTEXT = "TopLevelItemContext"
    TERMINAL = "Terminal"

    def error_thereIsNoProgram():
        scriptErrors.showError(
            pos=ScriptErrors.UNKNOWN_POSITION,
            error_type="DEEP ERROR",
            title="No program",
            msg="Tree seems empty. Are you sure you gave me a tree and not just a bark?"
        )

    def error_brokenTree():
        scriptErrors.showError(
            pos=ScriptErrors.UNKNOWN_POSITION,
            error_type="DEEP ERROR",
            title="Broken tree",
            msg="This tree is so broken it looks more like a stick."
        )

    def error_brokenLeaf(node, text=None):
        scriptErrors.showError(
            pos=ScriptErrors.Position.extract(node),
            error_type="DEEP ERROR",
            title="Broken leaf",
            msg="Found a Terminal without a meaning - like a stem without a leaf." 
                if text is None else \
                f"This not a place for '{text}' Terminal, move it somewhere else(including the trash)."            
        )

    def error_brokenBranch(node):
        scriptErrors.showError(
            pos=ScriptErrors.Position.extract(node),
            error_type="DEEP ERROR",
            title="Broken branch",
            msg="Where is the rest of this branch?"
        )

    def error_tooMuchChildren(node):
        scriptErrors.showError(
            pos=ScriptErrors.Position.extract(node),
            error_type="DEEP ERROR",
            title="Too much children",
            msg="You exceeded the child limit"
        )

    def error_placeDeclError(node):
        scriptErrors.showError(
            pos=ScriptErrors.Position.extract(node),
            error_type="SYNTAX ERROR",
            title="Bad structure",
            msg="Place is not structured correctly, it collapsed like an old house."
        )

    def error_placeNameError(node):
        scriptErrors.showError(
            pos=ScriptErrors.Position.extract(node),
            error_type="SYNTAX ERROR",
            title="Bad name",
            msg="Eww, who would want to name their place like that?"
        )

    def error_placeNameRepeat(node):
        scriptErrors.showError(
            pos=ScriptErrors.Position.extract(node),
            error_type="SYNTAX ERROR",
            title="Repeated name",
            msg="This name is already taken, think of something else"
        )

    def is_valid_name(name: str) -> bool:
        """
        Checks if given string contains only a-z A-Z 0-9 _
        and can't be 'global'
        """
        if re.match(r'[a-zA-Z0-9_]+', name) and name != "global":
            return True
        return False

    
    places = {
        # placeID -> code inside
        "global": []
    }


    # Check if there is a 'type' key at the root
    if "type" not in tree:
        log(PLACE, FATAL, "Root node does not contain 'type' key")
        error_thereIsNoProgram()
        exit()

    # Check if root node type is ProgramContext
    if tree["type"] != PROGRAM_CONTEXT:
        log(PLACE, FATAL, f"Root node is not {PROGRAM_CONTEXT}")
        error_thereIsNoProgram()
        exit()

    # Check if root node contains 'children'
    if "children" not in tree:
        log(PLACE, FATAL, "Root node does not contain 'children' key")
        error_thereIsNoProgram()
        exit()

    # Extract second layer -> TopLevelItemContext or Terminal <EOF>
    global_items = tree["children"]

    # Iterate second layer
    for global_item in global_items:
        # Check key 'type' exists
        if "type" not in global_item:
            log(PLACE, FATAL, "Second layer node does not have a 'type' key")
            error_brokenTree()
            exit()

        # Node can be of type Terminal
        if global_item["type"] == TERMINAL:
            # Then it must have a 'text' key
            if "text" not in global_item:
                log(PLACE, FATAL, f"{TERMINAL} does not have a 'text' key")
                error_brokenLeaf(global_item)
                exit()

            # Text can only be a EndOfFile
            if global_item["text"] == "<EOF>":
                break # this is the end of the program
            else:
                log(PLACE, FATAL, f"The only Terminal there should be a <EOF>, but found this: {global_item["text"]}")
                error_brokenLeaf(global_item, text=global_item["text"])
                exit()
        # or a TopLevelItemContext
        elif global_item["type"] == TOP_LEVEL_ITEM_CONTEXT:
            # It needs to have a 'children' key
            if "children" not in global_item:
                log(PLACE, FATAL, f"There is no 'children' key in {TOP_LEVEL_ITEM_CONTEXT}")
                error_brokenBranch(global_item)
                exit()

            # and exactly one child
            top_level_items = global_item["children"]
            if len(top_level_items) != 1:
                log(PLACE, FATAL, f"There is more that one child in {TOP_LEVEL_ITEM_CONTEXT}")
                error_tooMuchChildren(global_item)
                exit()
            
            # Extract the third layer -> PlaceDeclContext or something else
            top_level_item = top_level_items[0]

            # Check 'type' key
            if "type" not in top_level_item:
                log(PLACE, FATAL, f"There is no 'type' key in {TOP_LEVEL_ITEM_CONTEXT} children")
                error_brokenBranch(global_item)
                exit()

            # Type can be PlaceDeclContext
            if top_level_item["type"] == PLACE_DECLARATION_CONTEXT:
                # Check for 'children' key
                if "children" not in top_level_item:
                    log(PLACE, FATAL, f"There is no 'children' key in {TOP_LEVEL_ITEM_CONTEXT}")
                    error_brokenBranch(top_level_item)
                    exit()
                
                place_decl = top_level_item["children"]

                # Children:
                #   [0]    Terminal place       
                #   [1]    Terminal <name>
                #   [2]    Terminal {
                #   [3:-1]    inner block of code
                #   [-1]   Terminal }
                # Empty place = 4 children
                
                child_count = len(place_decl)

                if child_count < 4:
                    log(PLACE, FATAL, "This can't be a correct place, at least 4 Terminals are required")
                    error_placeDeclError(top_level_item)
                    exit()

                # First child must be a Terminal 'place'
                if ("type" not in place_decl[0]) or (place_decl[0]["type"] != "Terminal") or \
                   ("text" not in place_decl[0]) or (place_decl[0]["text"] != "place"):
                    log(PLACE, FATAL, f"There is no 'place' keyword, check the spelling")
                    error_placeDeclError(place_decl[0])
                    exit()

                # Second child must be a Terminal containing the name
                if ("type" not in place_decl[1]) or (place_decl[1]["type"] != "Terminal") or \
                   ("text" not in place_decl[1]):
                    log(PLACE, FATAL, "This place has no name")
                    error_placeDeclError(place_decl[1])
                    exit()
                
                place_name = place_decl[1]["text"]

                # Check if the name is a valid name
                if not is_valid_name(place_name):
                    log(PLACE, FATAL, f"Name '{place_name}' is not a valid name of a place")
                    error_placeNameError(place_decl[1])
                    exit()

                # Check if this name does not already exist
                if place_name in places:
                    log(PLACE, FATAL, f"Place with the same name already defined: '{place_name}'")
                    error_placeNameRepeat(place_decl[1])
                    exit()
                
                # Third child must be a '{' Terminal
                if ("type" not in place_decl[2]) or (place_decl[2]["type"] != "Terminal") or \
                   ("text" not in place_decl[2]) or (place_decl[2]["text"] != "{"):
                    log(PLACE, FATAL, "Where does the place block start? There is no '{'")
                    error_placeDeclError(place_decl[2])
                    exit()
                
                # Last child must be a '}' Terminal
                if ("type" not in place_decl[-1]) or (place_decl[-1]["type"] != "Terminal") or \
                   ("text" not in place_decl[-1]) or (place_decl[-1]["text"] != '}'):
                    log(PLACE, FATAL, "Where does the place block end?, There is no '}'")
                    error_placeDeclError(place_decl[-1])
                    exit()

                # Finally, assign everything inside to the place
                places[place_name] = place_decl[3:-1]
            # Or something else
            else:
                # throw it into 'global' place
                places["global"].append(top_level_item)

        else:
            log(PLACE, WARNING, f"Found a node of type '{global_item["type"]}' in the second layer, why is it here?")


    log(PLACE, SUCCESS, "OK", only_msg=True)
    log(PLACE, DEBUG, f"Got places: {" ".join(places.keys())}")
    return places
