from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: FNF-?

class FileNotFoundException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, file_path: str = "?", code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "FileNotFound"
        self.msg = f"Cannot find file or directory at the specified path: {file_path}"
        self.pos = pos
        self.code = "FNF-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg,
            code=self.code
        )
