import random
import threading
from typing import Dict, List, Optional

from ..logger import log, SIMULATOR, INFO, DEBUG, ERROR, WARNING, FATAL, SUCCESS

from .data.consts import _pauli_from_bits, _pauli_to_bits
from .data.consts import PAULI_MUL
from .data.consts import QuantumID, QuantumMeasurement, QuantumPrefix

from .data.gates import QuantumGate, QuantumGates
from .data.uid import QuantumUIDGenerator
from .data.state import QuantumState
from .data.event import QuantumEvent
from .data.graph import EntaglementGraph
from .data.history import QuantumHistory

from .exceptions.unknown_quantum_gate import UnknownQuantumGateException
from .exceptions.unknown_quantum_state import UnknownQuantumStateException
from .exceptions.no_target_for_multi_gate import NoTargetForMultiGateException
from .exceptions.quantum_state_already_exists import QuantumStateAlreadyExistsException
















    



class QuantumSimulator:
    """
    Quantum Simulator based on stabilizers model

    Works together with QuantumServer and QuantumClient to allow access to simulation
    from multiple processes 

    Supported operations:
        create_qubit(prefix) -> ID
            Creates a quantum state named: prefix + '/' + UID
            Returns the full ID of the created state
        list_states() -> List[ID]
            Returns a list of all created state's IDs
        get_stabilizers(ID) -> List[str]
            Returns internal stabilizers for a given state ID
        get_state(ID) -> state
            Returns internal state for a given state ID
        get_history(ID) -> history
            Returns a list of all events tied to state ID
        apply_gate(ID, gate, target|None)
            Applies the specified gate to state with given ID
            Multi gates required also the target state ID
        measure(ID) -> measurement
            Measures state with the given ID and returns the result
        remove_qubit(ID) -> bool
            Tries to remove a qubit. Call this when state went out of scope 
            and is no longer directly accesible. When the qubit was removed the method 
            will return True. Return of False means the removal of the qubit is not 
            possible as it might be in some relation with other qubits and
            removing it might mess up the simulation

    
    
    
    """
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.states: Dict[QuantumID, QuantumState] = {}
        # alias -> canonical original id
        self.aliases: Dict[QuantumID, QuantumID] = {}
        # canonical original id -> list of aliases (new names)
        self.canonical_aliases: Dict[QuantumID, List[QuantumID]] = {}
        self._prefix_rngs: Dict[QuantumPrefix, random.Random] = {}
        self._x: List[List[int]] = []
        self._z: List[List[int]] = []
        self._phase: List[int] = []
        self._qubit_order: List[QuantumID] = []
        self._qubit_index: Dict[QuantumID, int] = {}
        self.uid_generator = QuantumUIDGenerator()
        self.entanglement = EntaglementGraph()
        log(SIMULATOR, SUCCESS, "Simulator running")

    # Creates quantum state with a prefix and unique ID
    # Returns: the ID of created state(prefix + '/' + UID)
    def create_qubit(self, prefix: QuantumPrefix) -> QuantumID:
        with self._lock:
            id = self.uid_generator.next(prefix)

            # Make sure the state does not exist already
            if id in self.states:
                raise QuantumStateAlreadyExistsException(str(id))

            state = QuantumState(id)
            state.record(QuantumEvent.init(id))    
            self.states[id] = state
            self._add_tableau_qubit(id)
            self.entanglement.add(id)

            log(SIMULATOR, DEBUG, f"Created state: {id}")
            return id
        
    def list_states(self) -> List[QuantumID]:
        with self._lock:
            return [self.states[key].name for key in self.states]
        
    def get_stabilizers(self, id: QuantumID) -> List[str]:
        self._get_state(id)
        return self._format_tableau()
    
    def get_state(self, id: QuantumID) -> QuantumState:
        return self._get_state(id)
    
    def get_history(self, id: QuantumID) -> QuantumHistory:
        state = self._get_state(id)
        return QuantumHistory(state.get_history())
    


    def apply_gate(self, id: QuantumID, gate: QuantumGate, target: QuantumID | None = None):
        if not gate.valid:
            raise UnknownQuantumGateException(str(gate))

        with self._lock:
            if gate.single:
                if target is not None:
                    log(SIMULATOR, WARNING, f"apply_gate: target {target} was provided for a single gate {gate} on {id}!")
                state = self._get_state(id)
                self._apply_single_gate(id, gate)
                state.record(QuantumEvent.single_gate(gate, state.name))
                log(SIMULATOR, DEBUG, f"Applying single gate {gate} on {state.name}")
            elif gate.multi:
                if target is None:
                    raise NoTargetForMultiGateException(f"{gate} on {id}")
                controlState = self._get_state(id)
                targetState = self._get_state(target)
                self._apply_multi_gate(controlState.name, targetState.name, gate)
                controlState.record(QuantumEvent.multi_gate(gate, controlState.name, targetState.name))
                targetState.record(QuantumEvent.multi_gate(gate, controlState.name, targetState.name))
                log(SIMULATOR, DEBUG, f"Applying multi gate {gate} control {controlState.name} target {targetState.name}")
            else:
                log(SIMULATOR, ERROR, f"apply_gate: Gate {gate} is not sigle and not multi")
                exit()

    def measure(self, id: QuantumID) -> QuantumMeasurement:
        with self._lock:
            
            state = self._get_state(id)
            column = self._get_qubit_index(id)
            row_index = self._find_random_measurement_row(column)
            
            if row_index is None:
                result = self._deterministic_measure(column)
            else:
                prefix = self._extract_prefix(id)
                rng = self._prefix_rngs.get(prefix)
                if rng is not None:
                    result = QuantumMeasurement(rng.randrange(2))
                else:
                    result = QuantumMeasurement(random.randrange(2))
                self._random_measure(column, row_index, result)

            self.entanglement.split(id)

            state.record(QuantumEvent.measure(id, result))
            log(SIMULATOR, DEBUG, f"Measuring {id} -> {result}")
            return result

    def remove_qubit(self, id: QuantumID) -> bool:
        with self._lock:
            if id not in self.states:
                return False
            
            root = self.entanglement.find(id)
            for other in self.states:
                if other == id:
                    continue
                if self.entanglement.find(other) == root:
                    # cannot remove -> state is entangled
                    return False

            if not self._can_remove_tableau_qubit(id):
                return False
            
            self._remove_tableau_qubit(id)
            del self.states[id]
            self.entanglement.remove(id)

            return True

    def rename_state(self, old_id: QuantumID, new_prefix: QuantumPrefix) -> QuantumID:
        """Create an additional name for an existing state.

        The original state's canonical id remains unchanged. This method
        generates a new full id using the `QuantumUIDGenerator` and records it
        as an alias mapping so the simulator accepts the new id as referring
        to the same underlying state. Returns the new generated full id.
        """
        with self._lock:
            if old_id not in self.states:
                raise UnknownQuantumStateException(str(old_id))

            new_id = self.uid_generator.next(new_prefix)

            if new_id in self.states or new_id in self.aliases:
                raise QuantumStateAlreadyExistsException(str(new_id))

            # register alias -> canonical and canonical -> aliases
            self.aliases[new_id] = old_id
            self.canonical_aliases.setdefault(old_id, []).append(new_id)

            # record alias event in the canonical state's history
            canonical_state = self.states[old_id]
            canonical_state.record(QuantumEvent.alias(old_id, new_id))

            log(SIMULATOR, DEBUG, f"Added alias for state: {old_id} -> {new_id}")
            return new_id

    
    def _apply_single_gate(self, id: QuantumID, gate: QuantumGate):
        column = self._get_qubit_index(id)

        for row in range(self._row_count()):
            x_bit = self._x[row][column]
            z_bit = self._z[row][column]
            if gate == QuantumGates.H:
                if x_bit and z_bit:
                    self._phase[row] ^= 2
                self._x[row][column], self._z[row][column] = z_bit, x_bit
            elif gate == QuantumGates.S:
                if x_bit and z_bit:
                    self._phase[row] ^= 2
                self._z[row][column] ^= x_bit
            elif gate == QuantumGates.X:
                if z_bit:
                    self._phase[row] ^= 2
            elif gate == QuantumGates.Z:
                if x_bit:
                    self._phase[row] ^= 2
            elif gate == QuantumGates.Y:
                if x_bit ^ z_bit:
                    self._phase[row] ^= 2
            else:
                raise UnknownQuantumGateException(str(gate))


    def _apply_multi_gate(self, control: QuantumID, target: QuantumID, gate: QuantumGate):
        if gate == QuantumGates.CNOT:
            self._apply_cnot(control, target)
        elif gate == QuantumGates.CZ:
            self._apply_cz(control, target)
        else:
            raise UnknownQuantumGateException(str(gate))
        
        self.entanglement.union(control, target)


    def _apply_cnot(self, control: QuantumID, target: QuantumID):
        control_column = self._get_qubit_index(control)
        target_column = self._get_qubit_index(target)

        for row in range(self._row_count()):
            x_c = self._x[row][control_column]
            z_c = self._z[row][control_column]

            x_t = self._x[row][target_column]
            z_t = self._z[row][target_column]

            if x_c and z_t and (x_t ^ z_c ^ 1):
                self._phase[row] ^= 2
            
            self._x[row][target_column] ^= x_c
            self._z[row][control_column] ^= z_t

    def _apply_cz(self, control: QuantumID, target: QuantumID):
        self._apply_single_gate(target, QuantumGates.H)
        self._apply_cnot(control, target)
        self._apply_single_gate(target, QuantumGates.H)


    def _find_random_measurement_row(self, column: int) -> Optional[int]:
        n = self._qubit_count()
        for row in range(n, 2 * n):
            if self._x[row][column] == 1:
                return row
            
        return None

    def _deterministic_measure(self, column: int) -> QuantumMeasurement:
        n = self._qubit_count()
        scratch_x = [0] * n
        scratch_z = [0] * n
        scratch_phase = 0

        for row in range(n):
            if self._x[row][column]:
                scratch_x, scratch_z, scratch_phase = self._multiply_rows(
                    scratch_x,
                    scratch_z,
                    scratch_phase,
                    self._x[row + n],
                    self._z[row + n],
                    self._phase[row + n],
                )

        return QuantumMeasurement((scratch_phase // 2) & 1)

    def _random_measure(self, column: int, row_index: int, outcome: QuantumMeasurement):
        n = self._qubit_count()
        destabilizer_row = row_index - n

        for row in range(2 * n):
            if row != row_index and self._x[row][column]:
                self._row_multiply(row, row_index)

        self._x[row_index] = [0] * n
        self._z[row_index] = [0] * n
        self._z[row_index][column] = 1
        self._phase[row_index] = 2 if outcome else 0

        for row in range(2 * n):
            if row not in (destabilizer_row, row_index) and self._z[row][column]:
                self._row_multiply(row, row_index)

        self._x[destabilizer_row] = [0] * n
        self._z[destabilizer_row] = [0] * n
        self._x[destabilizer_row][column] = 1
        self._phase[destabilizer_row] = 0

    def _row_multiply(self, dest_row: int, src_row: int):
        self._x[dest_row], self._z[dest_row], self._phase[dest_row] = self._multiply_rows(
            self._x[dest_row],
            self._z[dest_row],
            self._phase[dest_row],
            self._x[src_row],
            self._z[src_row],
            self._phase[src_row],
        )

    def _multiply_rows(
        self,
        dest_x: List[int],
        dest_z: List[int],
        dest_phase: int,
        src_x: List[int],
        src_z: List[int],
        src_phase: int,
    ) -> tuple[List[int], List[int], int]:
        result_x = []
        result_z = []
        result_phase = (dest_phase + src_phase) % 4

        for dx, dz, sx, sz in zip(dest_x, dest_z, src_x, src_z):
            result_pauli, phase_delta = PAULI_MUL[(
                _pauli_from_bits(dx, dz),
                _pauli_from_bits(sx, sz),
            )]
            rx, rz = _pauli_to_bits(result_pauli)
            result_x.append(rx)
            result_z.append(rz)
            result_phase = (result_phase + phase_delta) % 4

        return result_x, result_z, result_phase

    def _row_symplectic_product(self, row_a: int, row_b: int) -> int:
        product = 0
        for xa, za, xb, zb in zip(self._x[row_a], self._z[row_a], self._x[row_b], self._z[row_b]):
            product ^= (xa and zb) ^ (za and xb)
        return product
    

    def _format_tableau(self) -> List[str]:
        rows = []
        n = self._qubit_count()
        for row in range(self._row_count()):
            paulis = []
            for column in range(n):
                p = _pauli_from_bits(self._x[row][column], self._z[row][column])
                paulis.append({
                    0: "I", 1: "X", 2: "Y", 3: "Z"
                }[p])

            ph = self._phase[row]
            sign = (
                "+" if ph == 0 else 
                "-" if ph == 2 else
                f"i^{ph}"
            )
            kind = "D" if row < n else "S"

            rows.append(f"{kind}{row % n}: {sign}{''.join(paulis)}")
        return rows
    
    def set_seed(self, prefix: QuantumPrefix, seed: int) -> None:
        self._prefix_rngs[prefix] = random.Random(seed)

    def _extract_prefix(self, id: QuantumID) -> QuantumPrefix:
        full_id = str(id)
        if "/" in full_id:
            return QuantumPrefix(full_id.split("/", 1)[0])
        return QuantumPrefix(full_id)

    def _get_state(self, id: QuantumID):
        # resolve aliases first
        canonical = id
        if id not in self.states:
            if id in self.aliases:
                canonical = self.aliases[id]
            else:
                raise UnknownQuantumStateException(str(id))
        return self.states[canonical]

    def _get_qubit_index(self, id: QuantumID) -> int:
        # resolve aliases that point to canonical ids
        canonical = id
        if id not in self._qubit_index:
            if id in self.aliases:
                canonical = self.aliases[id]
            else:
                raise UnknownQuantumStateException(str(id))
        if canonical not in self._qubit_index:
            raise UnknownQuantumStateException(str(id))
        return self._qubit_index[canonical]

    def _qubit_count(self) -> int:
        return len(self._qubit_order)

    def _row_count(self) -> int:
        return len(self._phase)

    def _add_tableau_qubit(self, id: QuantumID):
        n = self._qubit_count()
        new_n = n + 1

        for row in range(self._row_count()):
            self._x[row].append(0)
            self._z[row].append(0)

        destabilizer = [0] * new_n
        stabilizer = [0] * new_n
        destabilizer[n] = 1
        stabilizer[n] = 1

        self._x.insert(n, destabilizer)
        self._z.insert(n, [0] * new_n)
        self._phase.insert(n, 0)

        self._x.append([0] * new_n)
        self._z.append(stabilizer)
        self._phase.append(0)

        self._qubit_order.append(id)
        self._rebuild_qubit_index()

    def _remove_tableau_qubit(self, id: QuantumID):
        index = self._get_qubit_index(id)
        n = self._qubit_count()

        del self._x[n + index]
        del self._z[n + index]
        del self._phase[n + index]
        del self._x[index]
        del self._z[index]
        del self._phase[index]

        for row in range(self._row_count()):
            del self._x[row][index]
            del self._z[row][index]

        del self._qubit_order[index]
        self._rebuild_qubit_index()

    def _can_remove_tableau_qubit(self, id: QuantumID) -> bool:
        index = self._get_qubit_index(id)

        for row in range(self._row_count()):
            touches_removed = self._x[row][index] or self._z[row][index]
            touches_other = any(
                column != index and (self._x[row][column] or self._z[row][column])
                for column in range(self._qubit_count())
            )
            if touches_removed and touches_other:
                return False

        return True

    def _rebuild_qubit_index(self):
        self._qubit_index = {id: index for index, id in enumerate(self._qubit_order)}



