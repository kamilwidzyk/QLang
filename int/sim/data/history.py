from .event import QuantumEvent


class QuantumHistory:
    def __init__(self, history: list[QuantumEvent]):
        self.history = history

    def as_str_list(self) -> list[str]:
        return [str(x) for x in self.history]
    
    def as_list(self) -> list[QuantumEvent]:
        return self.history
    
    def __str__(self) -> str:
        return ' > '.join(['[' + x + ']' for x in self.as_str_list()])