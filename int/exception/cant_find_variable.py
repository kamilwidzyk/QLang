
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: CFV-?

class CantFindVariableException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, var_name, code: str = "?", suggestion: str = None):
        self.error_type = "RUNTIME ERROR"
        self.title = "ExistenceError"
        self.msg = f"I can't find '{var_name}' in this universe, does it even exist?"
        if suggestion:
            self.msg += f"  Did you mean '{suggestion}'?"
        self.pos = pos
        self.code = "CFV-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )

    