
from ..script_errors import ScriptErrors

# code: BEV-?

class BuiltinExpectsValueException(Exception):
    def __init__(self, pos: ScriptErrors.Position, func_name: str = "?", expects: str = "?", code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Built-in function Misuse"
        self.msg = f"Built-in function {func_name} expects {expects}."
        self.pos = pos
        self.code = "BEV-" +code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    