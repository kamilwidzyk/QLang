from typing import List

from .gates import QuantumGates, QuantumGate
from .state import QuantumID
from .consts import QuantumMeasurement

class EventType:
    SINGLE = "single"
    MULTI = "multi"
    MEASURE = "measure"
    INIT = "init"
    UNKNOWN = "unknown"

class QuantumEvent:
    def __init__(self, 
                 type: EventType, 
                 gate: QuantumGate = None,
                 control: QuantumID = None,
                 target: QuantumID = None,
                 outcome: QuantumMeasurement = None):
        self.type = type
        self.gate = gate
        self.control = control
        self.target = target
        self.outcome = outcome

    def involves(self, id: QuantumID) -> bool:
        return (id == self.control) or (id == self.target)
    
    def __str__(self) -> str:
        if self.type == EventType.MULTI:
            return f"GATE {self.gate}: {self.control} -> {self.target}"
        if self.type == EventType.SINGLE:
            return f"GATE {self.gate}: {self.control}"
        if self.type == EventType.MEASURE:
            return f"MEASURE {self.control} = {self.outcome}"
        if self.type == EventType.INIT:
            return f"INIT {self.control}"
        return "UNKNOWN"
    
    # Add this event when applying a single gate
    @classmethod
    def single_gate(cls, gate: QuantumGate, # which gate was applied
                    id: QuantumID # to which state ID it was applied
                    ) -> QuantumEvent:
        return cls(
            type=EventType.SINGLE,
            gate=gate,
            control=id
        )
    
    # Add this event when applying a multi gate 
    @classmethod
    def multi_gate(cls, gate: QuantumGate, # which gate was applied
                   control: QuantumID, # gate control state ID
                   target: QuantumID # gate target state ID
                   ) -> QuantumEvent:
        return cls(
            type=EventType.MULTI,
            gate=gate,
            control=control,
            target=target
        )
    
    # Add this event when measuring a state
    @classmethod
    def measure(cls, id: QuantumID,  # which state was measured
                outcome: QuantumMeasurement # what was the result
                ) -> QuantumEvent:
        return cls(
            type=EventType.MEASURE,
            control=id,
            outcome=outcome
        )
    
    # Add this event when creating a state
    @classmethod
    def init(cls, id: QuantumID) -> QuantumEvent:
        return cls(
            type=EventType.INIT,
            control=id
        )
    
    


        

    

    
