state q1;
state q2;

// Single-qubit gates
H q1;            // Apply Hadamard to q1
superpose q1;    // Alias for H q1
X q2;            // Apply Pauli-X to q2
not q2;          // Alias for X q2

// Two-qubit gates (control -> target)
CNOT q1 -> q2;       // Entangle: q1 is control, q2 is target
entangle q1 -> q2;   // Alias for CNOT q1 -> q2

// Swap gate
swap q1 q2;          // Swap the states of q1 and q2
