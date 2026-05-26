
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: NNV-?

class NetworkNotVariableException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Network Error"
        self.msg = "Network supports only variables as packet payload."
        self.pos = pos
        self.code = "NNV-" +code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )

    