
from ..script_errors import ScriptErrors


class InformationLeakException(Exception):
    def __init__(self, pos: ScriptErrors.Position, var_name, new_value, bits):
        self.error_type = "RUNTIME ERROR"
        self.title = "Spillover"
        self.msg = f"Information from '{var_name}' started leaking. {new_value} will not fit in {bits} bits."
        self.pos = pos
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    