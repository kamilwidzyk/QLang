from typing import Dict
from .consts import QuantumPrefix, QuantumID

class QuantumCounter:
    """ Makes sure every generated ID is unique """
    def __init__(self):
        self.value = 1
    
    @property
    def next(self):
        current = self.value
        self.value += 1
        return current
    
class QuantumUIDGenerator:
    """ Generates UID for a given prefix, separate counters for each prefix """
    def __init__(self):
        self.counters: Dict[QuantumPrefix, QuantumCounter] = {}

    def next(self, prefix: QuantumPrefix) -> QuantumID:
        if prefix not in self.counters:
            self.counters[prefix] = QuantumCounter()
        
        next_value = self.counters[prefix].next
        return QuantumID(f"{prefix}/{next_value}")