from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import Obs, ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_obs_definition(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # obsDef: ID ('[' expr ']')?;

    var_name = block.ID().getText()
    var_size = None
    if block.expr():
        var_size = self.handle_block(block.expr(), block)

    # Check if variable does not exists
    if self.scopes.exists(var_name):
        parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
        self.script_errors.showError(
            pos=pos,
            error_type="RUNTIME ERROR",
            title="SuperpositionError",
            msg="An observation cannot be in superposition. Pick one definition and stick to it."
        )
        exit()

    if var_size is not None:
        # Check if size is int
        if int(var_size) != var_size:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="RealityError", 
                msg="You cannot have half of a bit. Use an integer."
            )
            exit()


        if var_size <= 0:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="SizeError", 
                msg="I'm not capable of managing your imaginary, negative-sized registers.")
            exit()

    variable = None

    # Create obs register if size defined or obs if not
    if var_size is not None:
        variable = ObsRegister(var_size)
    else:
        variable = Obs()

    self.scopes.create(var_name, variable)