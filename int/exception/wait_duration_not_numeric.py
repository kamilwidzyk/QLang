from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: WDNN-?

class WaitDurationNotNumericException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, received_type: str, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "TypeError"
        self.msg = f"Expected numeric expression for wait duration, got {received_type}."
        self.pos = pos
        self.code_str = "" # Can be filled if needed, but not required
        self.code = "WDNN-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code_str
        )
