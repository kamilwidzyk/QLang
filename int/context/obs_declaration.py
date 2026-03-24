from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import Obs, ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_obs_declaration(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):   
    # this block is a obs variable declaration
    # new scope: no

    # children should be:
    # OPTION A
    # 1. Terminal 'obs'
    # 2. Terminal <variable_name>
    # If size defined:
    #   3a. Terminal '['
    #   3b. NumExprContext -> handle to get the size
    #   3c. Terminal ']'
    # If init with value:
    #   4a. Terminal '='
    #   4b. NumExprContext or measure(TODO!!!) -> handle to get value

    # OR (OPTION B)
    # 1. Terminal 'obs'
    # 2. ObsDefContext
    # Until end:
    #   3a. Terminal ','
    #   3b. ObsDefContext

    

    # Combinations:
    #         (CHILD INDEX)
    # (0) (1) (2)  (3)  (4)  (5)  (6)
    # [1] [2]                          -> obs name
    # [1] [2] [3a] [3b] [3c]           -> obs name[<size>]
    # [1] [2] [4a] [4b]                -> obs name = <val>
    # [1] [2] [3a] [3b] [3c] [4a] [4b] -> obs name[<size>] = <val>

    print("Parsing obs declaration")

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: 'children' key missing or no children")
        exit()

    children = block["children"]

    if len(children) < 2:                
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: at least 2 children required")
        exit()

    
    if self.is_type(children[1], type=OBS_DEF_CONTEXT, parent=block):
        # OPTION B
        # ...
        expect_block = True

        for child in children[1:]: # ignore the first
            if expect_block:
                if not self.is_type(child, type=OBS_DEF_CONTEXT, parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: optionB: expected ObsDefContext block")
                    exit()
                self.handle_block(child, block)
                expect_block = False
            else:
                if not self.is_terminal(child, text=",", parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: optionB: expected Terminal ','")
                    exit()
                expect_block = True


        return

    # OPTION A

    size_defined = False
    init_value_defined = False
    obs_size = None
    obs_value = None
    obs_name = None

    for child_index in range(len(children)):
        child = children[child_index]
        if child_index == 0: # 1. Terminal 'obs'
            if not self.is_terminal(child, text="obs", parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ObsDeclContext: first child is not terminal 'obs'")
                exit()
            print("1. Terminal 'obs' OK")
        elif child_index == 1: # 2. Terminal <variable_name> or ObsDefContext
            obs_name = self.extract_text(child, parent=block)
            if not self.is_valid_name(obs_name):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: name is not valid: " + obs_name)
                exit()
            print("2. Terminal <variable_name> = " + obs_name)
        elif child_index == 2: # can be '[' or '='
            text = self.extract_text(child, parent=block)
            if text == '[': # size definition
                size_defined = True
                print("3a. Size definition")
            elif text == '=': # value assigment
                init_value_defined = True
                print("4a. Terminal '='")
            else:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: unexpected terminal: " + text)
                exit()
        elif child_index == 3: # can be size num or assigment val
            if size_defined:
                if not self.is_type(child, NUM_EXPR_CONTEXT, parent=block):
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: expected block of type numExprContext")
                    exit()
                # handle numExprContext to get size
                obs_size = self.handle_block(child, parent=block)
                print("3b. size = " + str(obs_size))
            elif init_value_defined:
                obs_value = self.handle_block(child, parent=block)
                # handle to get init value
                print("4b. init value = " + str(obs_value))
            else:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: unexpected block at child index 3")
                exit()
        elif child_index == 4: # must be ']'
            if not self.is_terminal(child, text="]", parent=block):
                if size_defined:
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: child index 4, expected ']'")
                else:
                    self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: child index 4, unexpected block")
                exit()
        elif child_index == 5: # must be '='
            if not self.is_terminal(child, text='=', parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext: child index 5, expected '='")
                exit()
            init_value_defined = True
        elif child_index == 6: # must be val 
            if init_value_defined:
                # handle to get init value
                obs_value = self.handle_block(child, parent=block)
                print("4b. init value = " + str(obs_value))
            else:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext, child index 6, unexpected block")                        
                exit()
        else:
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "obsDeclContext, child index > 6, unexpected block")                        
            exit()

    print("Parsing done: ")
    print("Name: " + str(obs_name))
    print("Value: " + str(obs_value))
    print("Size: " + str(obs_size))

    # Create variable instance
    obs = None 

    if obs_size is not None: # size specified
        if int(obs_size) != obs_size or obs_size <= 0:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Value Error", "obsDeclContext: obs_size is not int or <= 0")
            exit()
        obs = ObsRegister(obs_size)
        if obs_value is not None: # value specified
            if int(obs_value) != obs_value or obs_value < 0:
                parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
                self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Value Error", "obsDeclContext: obs_value is not int or < 0")
                exit()
            max_val = obs.max_val()
            if obs_value > max_val:
                parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
                self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Value Error", f"obsDeclContext: obs_value is too large to fit in {obs_size} bits")                
                exit()
            obs.set(obs_value) # set value
    else: # one bit obs
        obs = Obs()
        if obs_value != 0 and obs_value != 1:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Value Error", "obsDeclContext: no size specified -> value can only be 0 or 1")
            exit()
        obs.set(obs_value)
    
    self.scopes.create(obs_name, obs)
    print(f"Observation with name '{obs_name}' created")