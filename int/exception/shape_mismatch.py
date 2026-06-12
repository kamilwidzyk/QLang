
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: SM-?

class ShapeMismatchException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, left_shape, right_shape, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Shape Error"
        self.msg = f"Can't assign shape {right_shape} to shape {left_shape}"
        self.pos = pos
        self.code = "SM-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )

    