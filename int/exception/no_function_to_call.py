
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: NFTC-?

class NoFunctionToCallException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, func_name, code: str = "?", suggestion: str = None):
        self.error_type = "RUNTIME ERROR"
        self.title = "ExecutionError"
        self.msg = f"Tried calling {func_name} function: No one picked up."
        if suggestion:
            self.msg += f"  Did you mean '{suggestion}'?"
        self.pos = pos
        self.code = "NFTC-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )

    