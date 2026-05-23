from typing import List
from .consts import QuantumID, QuantumPrefix
from .gates import QuantumGate, QuantumGates

class QuantumCommand:
    def __init__(self, cmd: str, args: List[str]):
        self.cmd = cmd
        self.args = args

    CMD_CREATE = "CREATE"
    CMD_LIST = "LIST"
    CMD_STABILIZERS = "STAB"
    CMD_STATES = "STATES"
    CMD_HISTORY = "HISTORY"
    CMD_GATE = "GATE"
    CMD_MEASURE = "MEASURE"
    CMD_REMOVE = "REMOVE"
    CMD_ALIAS = "ALIAS"
    CMD_SEED = "SEED"

    def is_cmd(self, cmd: str):
        return self.cmd == cmd

    NO_ARGS = []

    @classmethod
    def create_qubit(cls) -> QuantumCommand:
        return QuantumCommand(QuantumCommand.CMD_CREATE, QuantumCommand.NO_ARGS)

    @classmethod
    def list_states(cls) -> QuantumCommand:
        return QuantumCommand(QuantumCommand.CMD_LIST, QuantumCommand.NO_ARGS)

    @classmethod
    def get_stabilizers(cls, id: QuantumID) -> QuantumCommand:
        return QuantumCommand(QuantumCommand.CMD_STABILIZERS, [id])
    
    @classmethod
    def get_state(cls, id: QuantumID) -> QuantumCommand:
        return QuantumCommand(QuantumCommand.CMD_STATES, [id])
    
    @classmethod
    def get_history(cls, id: QuantumID) -> QuantumCommand:
        return QuantumCommand(QuantumCommand.CMD_HISTORY, [id])
    
    @classmethod
    def apply_gate(cls, id: QuantumID, gate: QuantumGate, target: QuantumID | None) -> QuantumCommand:
        if target is None:
            return QuantumCommand(QuantumCommand.CMD_GATE, [id, gate])
        return QuantumCommand(QuantumCommand.CMD_GATE, [id, gate, target])

    @classmethod
    def measure(cls, id: QuantumID) -> QuantumCommand:
        return QuantumCommand(QuantumCommand.CMD_MEASURE, [id])
    
    @classmethod
    def remove(cls, id: QuantumID) -> QuantumCommand:
        return QuantumCommand(QuantumCommand.CMD_REMOVE, [id])

    @classmethod
    def alias(cls, id: QuantumID, prefix: QuantumPrefix) -> QuantumCommand:
        return QuantumCommand(QuantumCommand.CMD_ALIAS, [id, prefix])

    @classmethod
    def seed(cls, seed_value: int) -> QuantumCommand:
        return QuantumCommand(QuantumCommand.CMD_SEED, [seed_value])



class QuantumRequest:
    def __init__(self, place_name: str, command: QuantumCommand):
        self.place_name = place_name
        self.command = command

