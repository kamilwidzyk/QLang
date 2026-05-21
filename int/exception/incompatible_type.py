
from ..script_errors import ScriptErrors

# code: IT-?

class IncompatibleTypeException(Exception):
    def __init__(self, pos: ScriptErrors.Position, func_name, param_name, param_type, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Type Error"
        self.msg = f"Argument '{param_name}' in '{func_name}' expects '{param_type}'."
        self.pos = pos
        self.code = "IT-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    