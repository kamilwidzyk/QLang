
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: ONI-?

class ObsNotIndexedException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, var_name: str, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "IndexError"
        self.msg = f"You are looking too deep into '{var_name}' - it can only be 0 or 1."
        self.pos = pos
        self.code = "ONI-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )

    