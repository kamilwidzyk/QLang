import multiprocessing
from multiprocessing import Queue, Manager
from typing import Any, Dict, List, Optional
import time

from .simulator import QuantumSimulator

from .data.request import QuantumRequest, QuantumCommand
from .data.response import QuantumResponse
from .data.consts import QuantumID, QuantumMeasurement, QuantumPrefix
from .data.gates import QuantumGate, QuantumGates
from .data.event import QuantumEvent
from .data.state import QuantumState
from .data.history import QuantumHistory

from .exceptions.no_target_for_multi_gate import NoTargetForMultiGateException
from .exceptions.quantum_state_already_exists import QuantumStateAlreadyExistsException
from .exceptions.unknown_quantum_gate import UnknownQuantumGateException
from .exceptions.unknown_quantum_state import UnknownQuantumStateException

class QuantumServer:
    def __init__(self, command_queue: Queue, response_queues: Dict[str, Queue]) -> None:
        self.command_queue = command_queue
        self.response_queues = response_queues
        self.sim = QuantumSimulator()
        self.running = True

    def run(self) -> None:
        while self.running:
            try:
                request: QuantumRequest = self.command_queue.get(timeout=1.0)
            except:
                continue

            if request is None:
                self.running = False
                break
            
            # process the request and send the response where it came from
            response: QuantumResponse = self._process_request(request)
            self.response_queues[request.place_name].put(response)

    def _process_request(self, req: QuantumRequest) -> QuantumResponse:
        try:
            if req.command.is_cmd(QuantumCommand.CMD_CREATE):
                prefix = QuantumPrefix(req.place_name)
                id = self.sim.create_qubit(prefix)
                return QuantumResponse.ok(id)
            if req.command.is_cmd(QuantumCommand.CMD_LIST):
                lst = self.sim.list_states()
                return QuantumResponse.ok(lst)
            if req.command.is_cmd(QuantumCommand.CMD_STABILIZERS):
                id = req.command.args[0]
                lst = self.sim.get_stabilizers(id)
                return QuantumResponse.ok(lst)
            if req.command.is_cmd(QuantumCommand.CMD_STATES):
                id = req.command.args[0]
                state = self.sim.get_state(id)
                return QuantumResponse.ok(state)
            if req.command.is_cmd(QuantumCommand.CMD_HISTORY):
                id = req.command.args[0]
                history = self.sim.get_history(id)
                return QuantumResponse.ok(history)
            if req.command.is_cmd(QuantumCommand.CMD_GATE):
                id = req.command.args[0]
                gate = req.command.args[1]
                target = req.command.args[2] if len(req.command.args) > 2 else None
                self.sim.apply_gate(id, gate, target)
                return QuantumResponse.ok(None)
            if req.command.is_cmd(QuantumCommand.CMD_MEASURE):
                id = req.command.args[0]
                result = self.sim.measure(id)
                return QuantumResponse.ok(result)
            if req.command.is_cmd(QuantumCommand.CMD_REMOVE):
                id = req.command.args[0]
                success = self.sim.remove_qubit(id)
                return QuantumResponse.ok(success)
            if req.command.is_cmd(QuantumCommand.CMD_ALIAS):
                id = req.command.args[0]
                new_prefix = req.command.args[1]
                new_id = self.sim.rename_state(id, new_prefix)
                return QuantumResponse.ok(new_id)
            return QuantumResponse.error("UnknownCommand")

        except NoTargetForMultiGateException:
            return QuantumResponse.error("NoTargetForMultiGateException")
        except QuantumStateAlreadyExistsException:
            return QuantumResponse.error("QuantumStateAlreadyExistsException")
        except UnknownQuantumGateException:
            return QuantumResponse.error("UnknownQuantumGateException")
        except UnknownQuantumStateException:
            return QuantumResponse.error("UnknownQuantumStateException")

def start_server(command_queue: Queue, response_queue: Dict[str, Queue]):
    server = QuantumServer(command_queue, response_queue)
    server.run()
