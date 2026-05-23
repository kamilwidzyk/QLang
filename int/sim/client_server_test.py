import multiprocessing
import random
from multiprocessing import Queue

from .client import QuantumClient
from .data.consts import QuantumID
from .data.gates import QuantumGates
from .server import start_server


def start_quantum_server(place_names: list[str]):
    command_queue = multiprocessing.Queue()
    response_queues = {
        place_name: multiprocessing.Queue()
        for place_name in place_names
    }
    server_process = multiprocessing.Process(
        target=start_server,
        args=(command_queue, response_queues),
    )
    server_process.start()

    return command_queue, response_queues, server_process


def stop_quantum_server(command_queue: Queue, server_process: multiprocessing.Process):
    command_queue.put(None)
    server_process.join(timeout=10.0)

    if server_process.is_alive():
        server_process.terminate()
        server_process.join(timeout=10.0)
        raise AssertionError("Quantum server did not stop cleanly")


def alice_bell_worker(
    command_queue: Queue,
    response_queue: Queue,
    ids_out: Queue,
    target_in: Queue,
    result_out: Queue,
):
    client = QuantumClient("Alice", command_queue, response_queue)
    alice_qubit = client.create_state()
    ids_out.put(alice_qubit)

    bob_qubit = target_in.get(timeout=10.0)
    client.apply_gate(alice_qubit, QuantumGates.H)
    client.apply_gate(alice_qubit, QuantumGates.CNOT, bob_qubit)

    result_out.put(int(client.measure(alice_qubit)))


def bob_bell_worker(
    command_queue: Queue,
    response_queue: Queue,
    ids_out: Queue,
    start_measure: Queue,
    result_out: Queue,
):
    client = QuantumClient("Bob", command_queue, response_queue)
    bob_qubit = client.create_state()
    ids_out.put(bob_qubit)

    start_measure.get(timeout=10.0)
    result_out.put(int(client.measure(bob_qubit)))


def test_single_client_server_roundtrip():
    command_queue, response_queues, server_process = start_quantum_server(["Lab"])

    try:
        client = QuantumClient("Lab", command_queue, response_queues["Lab"])
        qubit = client.create_state()

        assert qubit == "Lab/1"
        assert client.list_states() == [qubit]

        client.apply_gate(qubit, QuantumGates.X)

        assert int(client.measure(qubit)) == 1
        assert client.get_history(qubit).as_str_list() == [
            f"INIT {qubit}",
            f"GATE X: {qubit}",
            f"MEASURE {qubit} = 1",
        ]
    finally:
        stop_quantum_server(command_queue, server_process)


def test_client_server_prefix_seed():
    command_queue, response_queues, server_process = start_quantum_server(["Lab"])

    try:
        client = QuantumClient("Lab", command_queue, response_queues["Lab"])
        assert client.seed(123) is None

        qubit = client.create_state()
        client.apply_gate(qubit, QuantumGates.H)

        assert int(client.measure(qubit)) == 0
    finally:
        stop_quantum_server(command_queue, server_process)


def test_client_server_error_paths():
    command_queue, response_queues, server_process = start_quantum_server(["Lab"])

    try:
        client = QuantumClient("Lab", command_queue, response_queues["Lab"])
        qubit = client.create_state()

        assert client.apply_gate(qubit, QuantumGates.UNKNOWN) == "UnknownQuantumGateException"
        assert client.apply_gate(qubit, QuantumGates.CNOT) == "NoTargetForMultiGateException"
        assert client.measure(QuantumID("missing")) == "UnknownQuantumStateException"
    finally:
        stop_quantum_server(command_queue, server_process)


def test_two_client_processes_bell_pair():
    random.seed(0)
    command_queue, response_queues, server_process = start_quantum_server(["Alice", "Bob"])

    alice_ids = multiprocessing.Queue()
    bob_ids = multiprocessing.Queue()
    alice_target = multiprocessing.Queue()
    bob_start_measure = multiprocessing.Queue()
    results = multiprocessing.Queue()

    alice_process = multiprocessing.Process(
        target=alice_bell_worker,
        args=(command_queue, response_queues["Alice"], alice_ids, alice_target, results),
    )
    bob_process = multiprocessing.Process(
        target=bob_bell_worker,
        args=(command_queue, response_queues["Bob"], bob_ids, bob_start_measure, results),
    )

    try:
        alice_process.start()
        bob_process.start()

        alice_qubit = alice_ids.get(timeout=10.0)
        bob_qubit = bob_ids.get(timeout=10.0)

        assert alice_qubit == "Alice/1"
        assert bob_qubit == "Bob/1"

        alice_target.put(bob_qubit)
        alice_measurement = results.get(timeout=10.0)

        bob_start_measure.put(True)
        bob_measurement = results.get(timeout=10.0)

        alice_process.join(timeout=10.0)
        bob_process.join(timeout=10.0)

        assert alice_process.exitcode == 0
        assert bob_process.exitcode == 0
        assert alice_measurement == bob_measurement
    finally:
        for process in (alice_process, bob_process):
            if process.is_alive():
                process.terminate()
                process.join(timeout=10.0)
        stop_quantum_server(command_queue, server_process)


def run_all_tests():
    tests = [
        test_single_client_server_roundtrip,
        test_client_server_prefix_seed,
        test_client_server_error_paths,
        test_two_client_processes_bell_pair,
    ]

    for test in tests:
        test()
        print(f"PASS {test.__name__}")

    print(f"All {len(tests)} client/server simulation tests passed")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_all_tests()
