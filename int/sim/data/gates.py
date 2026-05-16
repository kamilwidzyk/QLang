class QuantumGate(str):
    def __new__(cls, name: str):
        return super().__new__(cls, name)
    
    SINGLE_GATES = ["H", "S", "X", "Y", "Z"]
    MULTI_GATES = ["CNOT", "CZ"]
    VALID_GATES = SINGLE_GATES + MULTI_GATES

    @property
    def valid(self) -> bool:
        return self in self.VALID_GATES
    
    @property
    def single(self) -> bool:
        return self in self.SINGLE_GATES
    
    @property
    def multi(self) -> bool:
        return self in self.MULTI_GATES



class QuantumGates:
    # gate enum with two names for each gate
    H = QuantumGate("H")
    SUPERPOSE = QuantumGate("H")

    S = QuantumGate("S")
    SHIFT = QuantumGate("S")

    X = QuantumGate("X")
    NOT = QuantumGate("X")

    Y = QuantumGate("Y")
    DUAL_NOT = QuantumGate("Y")

    Z = QuantumGate("Z")
    PHASE_NOT = QuantumGate("Z")

    CNOT = QuantumGate("CNOT")
    ENTANGLE = QuantumGate("CNOT")

    CZ = QuantumGate("CZ")
    ENTANGLE_PHASE = QuantumGate("CZ")


    UNKNOWN = QuantumGate("UNKNOWN")
    INVALID = QuantumGate("INVALID")