
from ..script_errors import ScriptErrors


class CantFindVariableException(Exception):
    def __init__(self, pos: ScriptErrors.Position, var_name):
        self.error_type = "RUNTIME ERROR"
        self.title = "ExistenceError"
        self.msg = f"I can't find '{var_name}' in this universe, does it even exist?"
        self.pos = pos
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    