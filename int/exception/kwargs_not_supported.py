
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: KANS-?

class KeywordArgumentsNotSupportedException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, func_name: str = "?", code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Keyword Arguments Not Supported"
        self.msg = f"'{func_name}' does not take any keyword arguments."
        self.pos = pos
        self.code = "KANS-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    