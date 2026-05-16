from typing import Tuple, NewType

PAULI_MAP = {
    (0, 0): 0,  # I
    (1, 0): 1,  # X
    (1, 1): 2,  # Y
    (0, 1): 3,  # Z
}

BITS_FROM_PAULI = {
    0: (0, 0),
    1: (1, 0),
    2: (1, 1),
    3: (0, 1),
}

PAULI_MUL = {
    (0, 0): (0, 0),
    (0, 1): (1, 0),
    (0, 2): (2, 0),
    (0, 3): (3, 0),
    (1, 0): (1, 0),
    (1, 1): (0, 0),
    (1, 2): (3, 1),
    (1, 3): (2, 3),
    (2, 0): (2, 0),
    (2, 1): (3, 3),
    (2, 2): (0, 0),
    (2, 3): (1, 1),
    (3, 0): (3, 0),
    (3, 1): (2, 1),
    (3, 2): (1, 3),
    (3, 3): (0, 0),
}

GATE_NAMES = {"H", "S", "X", "Y", "Z", "CNOT", "CZ"}

def _pauli_from_bits(x: int, z: int) -> int:
    return PAULI_MAP[(x, z)]

def _pauli_to_bits(p: int) -> Tuple[int, int]:
    return BITS_FROM_PAULI[p]

# ID of quantum state
QuantumID = NewType("QuantumID", str)

# Prefix of quantum state
QuantumPrefix = NewType("QuantumPrefix", str)

QuantumMeasurement = NewType("QuantumMeasurement", int)