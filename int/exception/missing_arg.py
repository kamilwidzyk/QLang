
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: MA-?

class MissingArgException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, func_name: str = "?", missing_arg: str = "?", code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Missing Argument"
        self.msg = f"{func_name} is missing required argument: {missing_arg}"
        self.pos = pos
        self.code = "MA-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )

    