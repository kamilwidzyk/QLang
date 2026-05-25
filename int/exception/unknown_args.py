
from ..script_errors import ScriptErrors
from .exit_exception import ExitException
# code: UA-?

class UnknownArgException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, func_name: str = "?", unknown_arg: str = "?", code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Unknown Argument"
        self.msg = f"Where did you get '{unknown_arg}'? '{func_name}' does not take that."
        self.pos = pos
        self.code = "UA-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    