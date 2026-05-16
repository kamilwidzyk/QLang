from typing import Tuple, List

from .consts import QuantumID
from .event import QuantumEvent


class QuantumState:
    def _set_initial_state(self):
        self.x = [1, 0]
        self.z = [0, 1]
        self.phase = [0, 0]


    def __init__(self, name: QuantumID):
        self._set_initial_state()
        self.name = name
        self.history: list[QuantumEvent] = []

    def get(self) -> Tuple[List, List, List]:
        return self.x, self.z, self.phase
    
    def record(self, event: QuantumEvent):
        self.history.append(event)

    def get_history(self) -> list[QuantumEvent]:
        return list(self.history)
    
