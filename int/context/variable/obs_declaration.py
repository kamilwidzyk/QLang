from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_obs_declaration(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):   
    # (A) OBS obsDef (',' obsDef)*
    # (B) OBS ID ('[' expr ']')? '=' expr

    # Option A: obsDef exists
    if block.obsDef():
        # iterate over every obs definition and handle it(no returned value)
        for definition in block.obsDef():
            self.handle_block(definition, block)
        return
    
    # Option B:
    obs_name = block.ID().getText()
    expressions = [x for x in block.expr()]
    
    obs_size = None
    obs_value = None
    if len(expressions) == 1: # one expr -> no size defined
        obs_value = self.handle_block(expressions[0], block)
    else: # two expr -> size defined
        obs_size = self.handle_block(expressions[0], block)
        obs_value = self.handle_block(expressions[1], block)

    # Create variable instance
    obs = None 

    # Check if variable does not exist
    if self.scopes.exists(obs_name):
        self.script_errors.showError(
            pos=pos,
            error_type="RUNTIME ERROR",
            title="SuperpositionError",
            msg="An observation cannot be in superposition. Pick one definition and stick to it."
        )
        exit()

    # Variable size is specified -> create ObsRegister
    if obs_size is not None: # size specified
        # Check if size is int
        if int(obs_size) != obs_size:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="RealityError", 
                msg="You cannot have half of a bit. Use an integer."
            )
            exit()

        # Check if size > 0
        if obs_size <= 0:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="SizeError", 
                msg="I'm not capable of managing your imaginary, negative-sized registers.")
            exit()
        
        # Create variable instance
        obs = ObsRegister(obs_size)
        obs.name = obs_name

        # Set value of specified
        if obs_value is not None: 
            # Check if value is int
            if int(obs_value) != obs_value:
                parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
                self.script_errors.showError(
                    pos=parent_pos, 
                    error_type="RUNTIME ERROR", 
                    title="RealityError", 
                    msg="You cannot have half of a bit. Use an integer."
                )
                exit()
            # Check if value is >= 0
            if obs_value < 0:
                parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
                self.script_errors.showError(
                    pos=parent_pos, 
                    error_type="RUNTIME ERROR", 
                    title="Anti-bitsDetected", 
                    msg="Making the value positive might help."
                )
                exit()

            # Check if value is <= max_val
            max_val = obs.max_val()
            if obs_value > max_val:
                parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
                self.script_errors.showError(
                    pos=parent_pos, 
                    error_type="RUNTIME ERROR", 
                    title="Spillover", 
                    msg=f"Information from '{obs_name}' started leaking. {obs_value} will not fit in {obs_size} bits."
                )                
                exit()
            obs.set(obs_value) # set value
    else: # one bit obs
        obs = Obs()
        obs.name = obs_name
        # Check if the value is 0 or 1
        if obs_value != 0 and obs_value != 1:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="BinaryViolation", 
                msg="In this universe, bit can only have two states. Please pick one."
            )
            exit()
        obs.set(obs_value)
    
    # Create variable in current scope
    self.scopes.create(obs_name, obs)