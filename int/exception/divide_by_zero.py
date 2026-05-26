
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: DBZ-?

class DivideByZeroException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Math Error"
        self.msg = "I don't do division by zero. Nobody does."
        self.pos = pos
        self.code = "DBZ-" +code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )

    