
from ..script_errors import ScriptErrors
from .exit_exception import ExitException
# code: PDNA-?

class PlaceDeclarationNotAllowedException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, file_name: str, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "IndexError"
        self.msg = f"Place declaration not allowed in imported file '{file_name}'"
        self.pos = pos
        self.code = "PDNA-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    