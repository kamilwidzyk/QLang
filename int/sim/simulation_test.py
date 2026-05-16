import random
from typing import Callable, Type

from .data.consts import QuantumID
from .exceptions.no_target_for_multi_gate import NoTargetForMultiGateException
from .exceptions.unknown_quantum_gate import UnknownQuantumGateException
from .exceptions.unknown_quantum_state import UnknownQuantumStateException
from .simulator import QuantumGate, QuantumGates, QuantumPrefix, QuantumSimulator


def assert_raises(expected_exception: Type[Exception], action: Callable[[], object]):
    try:
        action()
    except expected_exception:
        return
    except Exception as exc:
        raise AssertionError(
            f"Expected {expected_exception.__name__}, got {type(exc).__name__}: {exc}"
        ) from exc

    raise AssertionError(f"Expected {expected_exception.__name__}, got no exception")


def measure_after(*gates: QuantumGate) -> int:
    sim = QuantumSimulator()
    q = sim.create_qubit(QuantumPrefix("Q"))

    for gate in gates:
        sim.apply_gate(q, gate)

    return int(sim.measure(q))


def test_create_list_and_history():
    sim = QuantumSimulator()
    a = sim.create_qubit(QuantumPrefix("A"))
    b = sim.create_qubit(QuantumPrefix("B"))

    assert sim.list_states() == [a, b]
    assert sim.get_history(a).as_str_list() == [f"INIT {a}"]
    assert sim.get_history(b).as_str_list() == [f"INIT {b}"]


def test_global_tableau_shape():
    sim = QuantumSimulator()
    a = sim.create_qubit(QuantumPrefix("A"))
    sim.create_qubit(QuantumPrefix("B"))
    sim.create_qubit(QuantumPrefix("C"))

    tableau = sim.get_stabilizers(a)

    assert len(tableau) == 6
    assert tableau == [
        "D0: +XII",
        "D1: +IXI",
        "D2: +IIX",
        "S0: +ZII",
        "S1: +IZI",
        "S2: +IIZ",
    ]


def test_x_y_z_h_measurements():
    assert measure_after() == 0
    assert measure_after(QuantumGates.X) == 1
    assert measure_after(QuantumGates.Y) == 1
    assert measure_after(QuantumGates.Z) == 0
    assert measure_after(QuantumGates.H, QuantumGates.H) == 0
    assert measure_after(QuantumGates.X, QuantumGates.Z) == 1


def test_s_gate_stabilizer():
    sim = QuantumSimulator()
    q = sim.create_qubit(QuantumPrefix("Q"))

    sim.apply_gate(q, QuantumGates.H)
    sim.apply_gate(q, QuantumGates.S)

    assert sim.get_stabilizers(q) == ["D0: +Z", "S0: +Y"]


def test_s_gate_period_four():
    assert measure_after(
        QuantumGates.X,
        QuantumGates.S,
        QuantumGates.S,
        QuantumGates.S,
        QuantumGates.S,
    ) == 1


def test_cnot_truth_table():
    for control_value in (0, 1):
        for target_value in (0, 1):
            sim = QuantumSimulator()
            control = sim.create_qubit(QuantumPrefix("C"))
            target = sim.create_qubit(QuantumPrefix("T"))

            if control_value:
                sim.apply_gate(control, QuantumGates.X)
            if target_value:
                sim.apply_gate(target, QuantumGates.X)

            sim.apply_gate(control, QuantumGates.CNOT, target)

            assert int(sim.measure(control)) == control_value
            assert int(sim.measure(target)) == (target_value ^ control_value)


def test_bell_pair_correlation():
    for seed in range(20):
        random.seed(seed)
        sim = QuantumSimulator()
        a = sim.create_qubit(QuantumPrefix("A"))
        b = sim.create_qubit(QuantumPrefix("B"))

        sim.apply_gate(a, QuantumGates.H)
        sim.apply_gate(a, QuantumGates.CNOT, b)

        assert int(sim.measure(a)) == int(sim.measure(b))


def test_cz_graph_state_stabilizers():
    sim = QuantumSimulator()
    a = sim.create_qubit(QuantumPrefix("A"))
    b = sim.create_qubit(QuantumPrefix("B"))

    sim.apply_gate(a, QuantumGates.H)
    sim.apply_gate(b, QuantumGates.H)
    sim.apply_gate(a, QuantumGates.CZ, b)

    assert sim.get_stabilizers(a) == [
        "D0: +ZI",
        "D1: +IZ",
        "S0: +XZ",
        "S1: +ZX",
    ]


def test_measurement_history_and_removal():
    random.seed(0)
    sim = QuantumSimulator()
    a = sim.create_qubit(QuantumPrefix("A"))
    b = sim.create_qubit(QuantumPrefix("B"))

    sim.apply_gate(a, QuantumGates.H)
    sim.apply_gate(a, QuantumGates.CNOT, b)

    assert sim.remove_qubit(a) is False

    result = sim.measure(a)

    assert sim.remove_qubit(a) is True
    assert sim.list_states() == [b]
    assert int(sim.measure(b)) == int(result)

    history = sim.get_history(b).as_str_list()
    assert history[0] == f"INIT {b}"
    assert history[1] == f"GATE CNOT: {a} -> {b}"
    assert history[2].startswith(f"MEASURE {b} = ")


def test_error_paths():
    sim = QuantumSimulator()
    q = sim.create_qubit(QuantumPrefix("Q"))

    assert_raises(
        UnknownQuantumGateException,
        lambda: sim.apply_gate(q, QuantumGates.UNKNOWN),
    )
    assert_raises(
        NoTargetForMultiGateException,
        lambda: sim.apply_gate(q, QuantumGates.CNOT),
    )
    assert_raises(
        UnknownQuantumStateException,
        lambda: sim.measure(QuantumID("missing")),
    )


def run_all_tests():
    tests = [
        test_create_list_and_history,
        test_global_tableau_shape,
        test_x_y_z_h_measurements,
        test_s_gate_stabilizer,
        test_s_gate_period_four,
        test_cnot_truth_table,
        test_bell_pair_correlation,
        test_cz_graph_state_stabilizers,
        test_measurement_history_and_removal,
        test_error_paths,
    ]

    for test in tests:
        test()
        print(f"PASS {test.__name__}")

    print(f"All {len(tests)} simulation tests passed")


if __name__ == "__main__":
    run_all_tests()
