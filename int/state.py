from __future__ import annotations

from typing import List

from .expression import Expression, TYPE_BOOL, TYPE_STATE
from .sim.data.consts import QuantumID
from .sim.data.gates import QuantumGate, QuantumGates


class State:
    """
    Runtime handle for a simulator-backed quantum state.

    The value is intentionally opaque: user code can pass it to gates and
    measure it, but it cannot read or assign the underlying simulator UID.
    """
    type: str = TYPE_STATE

    def __init__(self, client=None, uid: QuantumID | None = None):
        if client is None and uid is None:
            raise RuntimeError("State requires a quantum simulator client")

        self.client = client
        self.uid = uid if uid is not None else client.create_state()

        if isinstance(self.uid, str) and self.uid.endswith("Exception"):
            raise RuntimeError(self.uid)

    def set(self, _new_value):
        raise TypeError("Quantum state cannot be assigned directly")

    def get(self):
        raise TypeError("Quantum state cannot be accessed directly")

    def get_value(self):
        raise TypeError("Quantum state cannot be accessed directly")

    def __deepcopy__(self, memo):
        return self

    def apply_gate(self, gate: QuantumGate, target: State | None = None):
        target_uid = target.uid if target is not None else None
        error = self.client.apply_gate(self.uid, gate, target_uid)
        if error is not None:
            raise RuntimeError(error)

    def measure(self) -> Expression:
        result = self.client.measure(self.uid)
        if isinstance(result, str):
            raise RuntimeError(result)
        return Expression(TYPE_BOOL, bool(int(result)))

    def measure_x(self) -> Expression:
        self.apply_gate(QuantumGates.H)
        return self.measure()

    def get_history(self):
        """Get the quantum operation history for this state from the server."""
        if self.client is None:
            raise RuntimeError("Cannot query server: no client available")
        history = self.client.get_history(self.uid)
        if isinstance(history, str):
            raise RuntimeError(f"Failed to get history: {history}")
        return history

    def get_stabilizers(self):
        """Get the stabilizer group for this state from the server."""
        if self.client is None:
            raise RuntimeError("Cannot query server: no client available")
        stabilizers = self.client.get_stabilizers(self.uid)
        if isinstance(stabilizers, str):
            raise RuntimeError(f"Failed to get stabilizers: {stabilizers}")
        return stabilizers

    def get_state_info(self):
        """Get the quantum state information from the server."""
        if self.client is None:
            raise RuntimeError("Cannot query server: no client available")
        state_info = self.client.get_state(self.uid)
        if isinstance(state_info, str):
            raise RuntimeError(f"Failed to get state info: {state_info}")
        return state_info

    def __len__(self):
        return 1

    def __getitem__(self, _key):
        raise TypeError("State object is not subscriptable")

    def __str__(self):
        return "<state>"


class StateRegister:
    """
    Represents a quantum register.
    """
    states: List[State]
    type: str = "StateRegister"
    
    def __init__(self, size: int, client=None):
        self.states = [State(client=client) for _ in range(size)]

    def size(self) -> int:
        return len(self.states)
