from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: UTU-?

class UnknownTimeUnitException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, unit: str, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "UnknownUnit"
        self.msg = f"Unknown time unit '{unit}'. Valid units: ms, s, m, h."
        self.pos = pos
        self.code_str = unit
        self.code = "UTU-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code_str
        )
