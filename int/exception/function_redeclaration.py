
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: FR-?

class FunctionRedeclarationException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, func_name, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "You Error"
        self.msg = f"The function '{func_name}' already exists, whether you remember it or not."
        self.pos = pos
        self.code = "FR-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    