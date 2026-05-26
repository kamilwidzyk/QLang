from ..script_errors import ScriptErrors
from .exit_exception import ExitException
# code: TTMC-?

class TryingToModifyConstException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, var_name: str, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "TryingToModifyConst"
        self.msg = f"Cannot modify constant '{var_name}' after declaration."
        self.pos = pos
        self.code = "TTMC-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )
