import multiprocessing
from multiprocessing import Queue

from .client import QuantumClient
from .data.consts import QuantumID
from .data.gates import QuantumGates
from .server import start_server


def alice_client(
    command_queue: Queue,
    response_queue: Queue,
    ids_out: Queue,
    target_in: Queue,
    result_out: Queue,
):
    client = QuantumClient("Alice", command_queue, response_queue)

    alice_qubit = client.create_state()
    ids_out.put(alice_qubit)

    bob_qubit = target_in.get()
    client.apply_gate(alice_qubit, QuantumGates.H)
    client.apply_gate(alice_qubit, QuantumGates.CNOT, bob_qubit)

    result_out.put(("Alice", alice_qubit, client.measure(alice_qubit)))


def bob_client(
    command_queue: Queue,
    response_queue: Queue,
    ids_out: Queue,
    start_measure: Queue,
    result_out: Queue,
):
    client = QuantumClient("Bob", command_queue, response_queue)

    bob_qubit = client.create_state()
    ids_out.put(bob_qubit)

    start_measure.get()
    result_out.put(("Bob", bob_qubit, client.measure(bob_qubit)))


def run_example():
    command_queue = multiprocessing.Queue()
    alice_response_queue = multiprocessing.Queue()
    bob_response_queue = multiprocessing.Queue()
    response_queues = {
        "Alice": alice_response_queue,
        "Bob": bob_response_queue,
    }

    alice_ids = multiprocessing.Queue()
    bob_ids = multiprocessing.Queue()
    alice_target = multiprocessing.Queue()
    bob_start_measure = multiprocessing.Queue()
    results = multiprocessing.Queue()

    server_process = multiprocessing.Process(
        target=start_server,
        args=(command_queue, response_queues),
        name="QuantumServer",
    )
    alice_process = multiprocessing.Process(
        target=alice_client,
        args=(command_queue, alice_response_queue, alice_ids, alice_target, results),
        name="AliceClient",
    )
    bob_process = multiprocessing.Process(
        target=bob_client,
        args=(command_queue, bob_response_queue, bob_ids, bob_start_measure, results),
        name="BobClient",
    )

    server_process.start()
    alice_process.start()
    bob_process.start()

    alice_qubit = QuantumID(alice_ids.get(timeout=10.0))
    bob_qubit = QuantumID(bob_ids.get(timeout=10.0))

    alice_target.put(bob_qubit)

    alice_result = results.get(timeout=10.0)
    bob_start_measure.put(True)
    bob_result = results.get(timeout=10.0)

    alice_process.join(timeout=10.0)
    bob_process.join(timeout=10.0)

    command_queue.put(None)
    server_process.join(timeout=10.0)

    print("Server process:", server_process.name)
    print("Client processes:", alice_process.name, bob_process.name)
    print("Created qubits:", alice_qubit, bob_qubit)
    print("Measurements:", alice_result, bob_result)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_example()
