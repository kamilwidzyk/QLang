
from ..script_errors import ScriptErrors

# code: DQA-?

class DirectQuantumAccessException(Exception):
    def __init__(self, pos: ScriptErrors.Position, code: str = "?"):
        self.error_type = "RUNTIME ERROR"
        self.title = "Access Denied"
        self.msg = "Tried to access Quantum state directly, good luck with that."
        self.pos = pos
        self.code = "DQA-" +code
        super().__init__(self.msg)

    def show(self, script_errors: ScriptErrors):
        script_errors.showError(
            pos=self.pos,
            error_type=self.error_type,
            title=self.title,
            msg=self.msg
        )

    