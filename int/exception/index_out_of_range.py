
from ..script_errors import ScriptErrors
from .exit_exception import ExitException

# code: IOR-?

class IndexOutOfRangeException(ExitException):
    def __init__(self, pos: ScriptErrors.Position, index_value, length, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Index Out of Range"
        self.msg = f"Index {index_value} is out of range for container of size {length}."
        self.pos = pos
        self.code = "IOR-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )
