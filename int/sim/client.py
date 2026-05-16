num_qubits = 1

x = [[0] * num_qubits for _ in range(2 * num_qubits)]
z = [[0] * num_qubits for _ in range(2 * num_qubits)]
phase = [0] * (2 * num_qubits)

for i in range(num_qubits):
    x[i][i] = 1
    z[num_qubits + i][i] = 1

print(x)
print(z)
print(phase)