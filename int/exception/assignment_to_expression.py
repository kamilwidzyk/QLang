
from ..script_errors import ScriptErrors

# code: ATE-?

class AssignmentToExpressionException(Exception):
    def __init__(self, pos: ScriptErrors.Position, code: str = "?"):
        self.error_type = "SYNTAX ERROR"
        self.title = "Can't assign to expression"
        self.msg = "You can only assign values to variables, not to expressions."
        self.pos = pos
        self.code = "ATE-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    