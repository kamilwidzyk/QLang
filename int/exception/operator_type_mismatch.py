
from ..script_errors import ScriptErrors


class OperatorTypeMismatchException(Exception):
    def __init__(self, pos: ScriptErrors.Position, left_type, right_type, operator, operator_worded):
        self.error_type = "RUNTIME ERROR"
        self.title = "Type Error"
        self.msg = f"Operator '{operator}' refuses to work on {operator_worded} {left_type} and {right_type}"
        self.pos = pos
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    