
from ..script_errors import ScriptErrors
from .exit_exception import ExitException
# code: RKA-?

class RepeatedKeywordArgException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, func_name: str = "?", code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Repeated Keyword Argument"
        self.msg = f"{func_name} has too many options. I can't decide which one to choose."
        self.pos = pos
        self.code = "RKA-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    