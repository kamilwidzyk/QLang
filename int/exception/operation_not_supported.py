
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: ONS-?

class OperationNotSupportedException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, msg: str, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "OperationNotSupported"
        self.msg = msg
        self.pos = pos
        self.code = "ONS-" +code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )

    