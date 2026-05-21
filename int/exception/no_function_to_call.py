
from ..script_errors import ScriptErrors

# code: NFTC-?

class NoFunctionToCallException(Exception):
    def __init__(self, pos: ScriptErrors.Position, func_name, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "ExecutionError"
        self.msg = f"Tried calling {func_name} function: No one picked up."
        self.pos = pos
        self.code = "NFTC-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    