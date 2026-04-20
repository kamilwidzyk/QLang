import sys
import json
from typing import List, Dict, Any
import re
import antlr4

from .logger import init_log, log, log_level 
from .logger import INIT, PLACE
from .logger import FATAL, ERROR, WARNING, SUCCESS, INFO, DEBUG, NOTHING

from .load import load_input_files
from .script_errors import ScriptErrors

from .place import Place
from .network import QuantumNetwork

from .QLang.QLangParser import QLangParser
# Aliases for contexts
ProgramCtx = QLangParser.ProgramContext
PlaceDeclCtx = QLangParser.PlaceDeclContext
FunctionDeclCtx = QLangParser.FunctionDeclContext
StatementCtx = QLangParser.StatementContext

def divideIntoPlaces(tree: antlr4.tree.ParseTree, script_errors: ScriptErrors, network: QuantumNetwork, parser: any) -> Places:
    """ 
    Divides original tree into places. 
    Code not in any place ends up in 'global' place.
    Therefore 'global' is not a valid place name.
    
    Place name can only contain a-z A-Z 0-9 _ 

    Parameters:
        tree (Any): parsed tree
        script_errors (ScriptErrors): instace of error displaying class
        network (QuantumNetwork): instace of QuantumNetwork
    
    Returns:
        Instance of Places class with all of the places added along with their code
    """
    def get_place_header_position(position: ScriptErrors.Position, place_name: str):
        return ScriptErrors.Position(
            start_line=position.start_line(),
            start_col=position.start_col() + 6,
            end_line=position.start_line(),
            end_col=position.start_col() + len(place_name) + 6 
        )
    def get_original_text(ctx):
        stream = ctx.parser.getTokenStream()
        start_index = ctx.start.tokenIndex
        end_index = ctx.stop.tokenIndex
        return stream.getText(start_index, end_index)
    


    log(PLACE, INFO, "Dividing into places...", end=False)

    # Create places instance to store the separated places
    places = Places()
    places.create_place("global", script_errors, ScriptErrors.Position(0, 0), network)

    # Get children of topLevelItem
    top_level_items = tree.topLevelItem()

    # Every child can be a placeDecl, functionDecl or statement
    for top_level_item in top_level_items:
        for top_level in top_level_item.getChildren():

            if isinstance(top_level, PlaceDeclCtx):
                place_name = top_level.ID().getText()

                position = ScriptErrors.Position.extract(top_level)

                if not places.is_valid_name(place_name):
                    script_errors.showError(
                        pos=get_place_header_position(position, place_name),
                        error_type="SYNTAX ERROR",
                        title="Bad name",
                        msg="Eww, who would want to name their place like that?"
                    )
                    
                    exit()
                
                if places.is_defined(place_name):
                    script_errors.showError(
                        pos=get_place_header_position(position, place_name), 
                        error_type="RUNTIME ERROR", 
                        title="Repeated name",
                        msg="This name is already taken, think of something else"
                    )
                    exit()

                places.create_place(
                    place_name, 
                    script_errors, 
                    position, 
                    network
                )

                # Add every member to place 
                for member in top_level.placeMember():
                    places.add_code(place_name, 
                                    get_original_text(member.getChild(0)))

            # Add everything else to 'global' place
            elif isinstance(top_level, FunctionDeclCtx) or \
                isinstance(top_level, StatementCtx):
                places.add_code("global", top_level.getText())


    log(PLACE, SUCCESS, "OK", only_msg=True)
    log(PLACE, DEBUG, f"Got places: {" ".join(places.list_names())}")
    return places
    


class Places:
    """
    Represents all places with assigned names and code within them
    """
    places: Dict[str, Place] = {}

    def create_place(self, name: str, script_errors: ScriptErrors, 
                     declared_at: ScriptErrors, network: QuantumNetwork):
        """
        Creates empty place with given name

        Parameters:
            name (str): Name of the place to create
            script_errors (ScriptErrors): instance of class for displaying errors
            network (QuantumNetwork): instance of QuauntumNetwork
        """
        new_place = Place(name, script_errors, declared_at, network)
        self.places[name] = new_place

    def add_code(self, name: str, code: Any):
        """
        Adds code to specified place

        Parameters:
            name (str): Name of the place to add code to
            code (Any): Code to add to the specified place
        """
        self.places[name].add_code(code)

    def is_defined(self, name: str) -> bool:
        """
        Returns True if place with a given name exists

        Parameters:
            name (str): name of the place to check
        """
        return name in self.places.keys()
    

    def list_names(self) -> List[str]:
        """
        Returns a list of all names
        """
        return self.places.keys()
    
    def run(self):
        """
        Starts execution of all places at once
        """
        for place in self.places.values():
            place.run()
        log(PLACE, SUCCESS, "All places running")

    def wait_for_end(self):
        """
        Blocks until all places stop executing
        """
        for place in self.places.values():
            place.wait_for_end()
        log(PLACE, INFO, "All places stopped")

    def is_valid_name(self, name: str) -> bool:
        """
        Checks if given string contains only a-z A-Z 0-9 _
        and can't be 'global'
        """
        if re.match(r'[a-zA-Z0-9_]+', name) and name != "global":
            return True
        return False
        

