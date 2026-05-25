
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: VR-?

class VariableRedefiniotionException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "SuperpositionError"
        self.msg = "A variable cannot be in superposition. Pick one definition and stick to it."
        self.pos = pos
        self.code = "VR-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    