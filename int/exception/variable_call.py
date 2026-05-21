
from ..script_errors import ScriptErrors

# code: VC-?

class VariableCallException(Exception):
    def __init__(self, pos: ScriptErrors.Position, func_name, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "ExecutionError"
        self.msg = f"I tried to call '{func_name}' but a variable picked up."
        self.pos = pos
        self.code = "VC-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    