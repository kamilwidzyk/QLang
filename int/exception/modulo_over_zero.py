
from ..script_errors import ScriptErrors


# code: MOZ-?

class ModuloOverZeroException(Exception):
    def __init__(self, pos: ScriptErrors.Position, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Math Error"
        self.msg = "Modulo over zero? Bold of you to assume I'd allow that.."
        self.pos = pos
        self.code = "MOZ-" + code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    