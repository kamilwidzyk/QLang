
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: NPS-?

class NoParentScopeException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "No Parent Scope"
        self.msg = "You are already at the top. Can't go higher."
        self.pos = pos
        self.code = "NPS-" +code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    