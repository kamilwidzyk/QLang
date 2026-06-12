from typing import Any, TYPE_CHECKING

from ..expression import Expression, TYPE_LIST, TYPE_STATE
from ..script_errors import ScriptErrors
from ..state import State
from ..sim.data.gates import QuantumGate, QuantumGates
from .expression.variable_expression import handle_variable_expression, is_variable_expression
from .variable.assigment import handle_var
from ..exception.internal import InternalException

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
    # to be removed...
    self.script_errors.showError(
        pos=pos,
        error_type="RUNTIME ERROR",
        title=title,
        msg=msg,
    )
    exit()


def _resolve_state(self: "Place", var_ctx: Any, pos: ScriptErrors.Position):
    """
    Returns a quantum state(normally not accessible)
    """
    variable = handle_var(self, var_ctx, None)

    if variable.type != TYPE_STATE:
        # code I-4
        raise InternalException(pos, "Quantum operation requires a state variable.", code="4")

    expr = variable.get()
    if expr.type == TYPE_STATE and isinstance(expr.value, State):
        return expr.value

    if isinstance(expr.value, list) and all(isinstance(item, State) for item in expr.value):
        return expr.value

    # code I-5
    raise InternalException(pos, "Select exactly one state element.", code="5")


def _resolve_state_value(self: "Place", value: Any, pos: ScriptErrors.Position):
    """
    Return value of quantum state(this not accessible in the language)
    """
    if isinstance(value, Expression):
        if value.type == TYPE_STATE and isinstance(value.value, State):
            return value.value
        if value.type == TYPE_LIST:
            return [_resolve_state_value(self, item, pos) for item in value.value]

    if isinstance(value, State):
        return value

    if isinstance(value, list):
        return [_resolve_state_value(self, item, pos) for item in value]

    # code I-6
    raise InternalException(pos, "Quantum operation required a state or list of states.")


def _gate_from_text(text: str) -> QuantumGate:
    return GATE_BY_TEXT[text]


def handle_gate_statement(self: "Place", block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles applying gates to quantum states
    """
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
    """
    Handles collapsing and measuring quantum state
    """
    if block.list_() is not None:
        expr_block = block.list_()
        values = []

        for expr_ctx in expr_block.expr():
            if is_variable_expression(expr_ctx):
                var_or_expr = handle_variable_expression(self, expr_ctx, block, pos, return_variable=True)
                if isinstance(var_or_expr, Expression):
                    values.append(var_or_expr)
                elif hasattr(var_or_expr, "type") and var_or_expr.type == TYPE_STATE:
                    values.append(var_or_expr.get())
                else:
                    values.append(var_or_expr)
            else:
                values.append(self.handle_block(expr_ctx, block))

        state = _resolve_state_value(self, Expression(TYPE_LIST, values, shape=[len(values)]), pos)
    else:
        state = _resolve_state(self, block.var(), pos)

    if isinstance(state, list):
        if block.MEASUREX() is not None:
            return Expression(TYPE_LIST, [st.measure_x().get_value() for st in state], shape=[len(state)])
        return Expression(TYPE_LIST, [st.measure().get_value() for st in state], shape=[len(state)])

    if block.MEASUREX() is not None:
        return state.measure_x()
    return state.measure()
