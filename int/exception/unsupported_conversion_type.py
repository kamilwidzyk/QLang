
from ..script_errors import ScriptErrors
from .exit_exception import ExitException
# code: UCT-?

class UnsupportedConversionTypeException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, target_type: str, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "ConversionError"
        self.msg = f"Do you know how to convert to '{target_type}'? I don't."
        self.pos = pos
        self.code = "UCT-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )

    