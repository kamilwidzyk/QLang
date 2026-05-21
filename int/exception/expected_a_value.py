
from ..script_errors import ScriptErrors

# code: EAV-?

class ExpectedAValueException(Exception):
    def __init__(self, pos: ScriptErrors.Position, expected: str, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Value Error"
        self.msg = f"Expected {expected}"
        self.pos = pos
        self.code = "EAV-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    