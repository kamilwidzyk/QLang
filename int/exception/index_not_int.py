
from ..script_errors import ScriptErrors

# code: INI-?

class IndexNotIntException(Exception):
    def __init__(self, pos: ScriptErrors.Position, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Index Error"
        self.msg = "You can't have half of a bit. Using integer might help."
        self.pos = pos
        self.code = "INI-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    