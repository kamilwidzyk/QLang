
from ..script_errors import ScriptErrors

# code: TMA-?

class TooMuchArgumentsException(Exception):
    def __init__(self, pos: ScriptErrors.Position, func_name: str = "?", taken_args: int = 0, expected_args: int = 0, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Too Many Arguments"
        self.msg = f"{func_name} takes {expected_args} arguments but {taken_args} were given!"   
        self.pos = pos
        self.code = "TMA-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    