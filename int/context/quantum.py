from typing import Any, TYPE_CHECKING

from ..expression import Expression, TYPE_BOOL, TYPE_LIST, TYPE_STATE
from ..script_errors import ScriptErrors
from ..state import State
from ..sim.data.gates import QuantumGate, QuantumGates
from .variable.assigment import handle_var

if TYPE_CHECKING:
    from place import Place


GATE_BY_TEXT = {
    "H": QuantumGates.H,
    "superpose": QuantumGates.SUPERPOSE,
    "S": QuantumGates.S,
    "shift": QuantumGates.SHIFT,
    "X": QuantumGates.X,
    "not": QuantumGates.NOT,
    "Y": QuantumGates.Y,
    "dual_not": QuantumGates.DUAL_NOT,
    "Z": QuantumGates.Z,
    "phase_not": QuantumGates.PHASE_NOT,
    "CNOT": QuantumGates.CNOT,
    "entangle": QuantumGates.ENTANGLE,
    "CZ": QuantumGates.CZ,
    "entangle_phase": QuantumGates.ENTANGLE_PHASE,
}


def _runtime_error(self: "Place", pos: ScriptErrors.Position, title: str, msg: str):
    self.script_errors.showError(
        pos=pos,
        error_type="RUNTIME ERROR",
        title=title,
        msg=msg,
    )
    exit()


def _resolve_state(self: "Place", var_ctx: Any, pos: ScriptErrors.Position):
    variable = handle_var(self, var_ctx, None)

    if variable.type != TYPE_STATE:
        _runtime_error(self, pos, "Type Error", "Quantum operation requires a state variable.")

    expr = variable.get()
    if expr.type == TYPE_STATE and isinstance(expr.value, State):
        return expr.value

    if isinstance(expr.value, list) and all(isinstance(item, State) for item in expr.value):
        return expr.value

    _runtime_error(self, pos, "Type Error", "Select exactly one state element.")


def _gate_from_text(text: str) -> QuantumGate:
    return GATE_BY_TEXT[text]


def handle_gate_statement(self: "Place", block: Any, parent: Any, pos: ScriptErrors.Position):
    if block.singleQubitGate() is not None:
        gate = _gate_from_text(block.singleQubitGate().getText())
        state = _resolve_state(self, block.var(0), pos)
        if isinstance(state, list):
            for st in state:
                st.apply_gate(gate)
            return None
        state.apply_gate(gate)
        return None

    if block.multiQubitGate() is not None:
        gate = _gate_from_text(block.multiQubitGate().getText())
        control = _resolve_state(self, block.var(0), pos)
        target = _resolve_state(self, block.var(1), pos)
        control.apply_gate(gate, target)
        return None

    left = _resolve_state(self, block.var(0), pos)
    right = _resolve_state(self, block.var(1), pos)
    left.apply_gate(QuantumGates.CNOT, right)
    right.apply_gate(QuantumGates.CNOT, left)
    left.apply_gate(QuantumGates.CNOT, right)
    return None


def handle_measure_expr(self: "Place", block: Any, parent: Any, pos: ScriptErrors.Position) -> Expression:
    state = _resolve_state(self, block.var(), pos)

    if isinstance(state, list):
        if block.MEASUREX() is not None:
            return Expression(TYPE_LIST, [st.measure_x().get_value() for st in state], shape=[len(state)])
        return Expression(TYPE_LIST, [st.measure().get_value() for st in state], shape=[len(state)])

    if block.MEASUREX() is not None:
        return state.measure_x()
    return state.measure()
