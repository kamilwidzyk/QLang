
from ..script_errors import ScriptErrors


class IndexNotIntException(Exception):
    def __init__(self, pos: ScriptErrors.Position):
        self.error_type = "RUNTIME ERROR"
        self.title = "Index Error"
        self.msg = "You can't have half of a bit. Using integer might help."
        self.pos = pos
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    