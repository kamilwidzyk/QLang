import multiprocessing
from multiprocessing import Queue
from typing import Any, Dict, List, Optional
import time

from .data.request import QuantumRequest, QuantumCommand
from .data.response import QuantumResponse
from .data.consts import QuantumID
from .data.consts import QuantumPrefix
from .data.state import QuantumState
from .data.event import QuantumEvent
from .data.gates import QuantumGate
from .data.consts import QuantumMeasurement
from .data.history import QuantumHistory

class QuantumClient:
    def __init__(self, place_name: str, command_queue: Queue, response_queue: Queue):
        self.place_name = place_name
        self.command_queue = command_queue
        self.response_queue = response_queue
        self.timeout = 10.0

    def _send_command(self, cmd: QuantumCommand) -> QuantumResponse:
        request = QuantumRequest(self.place_name, cmd)
        self.command_queue.put(request)

        try:
            response = self.response_queue.get(timeout=self.timeout)
            return response
        except:
            raise TimeoutError(f"QuantumClient({self.place_name}): Response timeout after {self.timeout}s")
        
    # If any command method returns a 'str' -> it's error

    # Creates a new quantum state,
    # Prefix is fixed to place name(isolation)
    # Returned QuantumID is unique(store this value as a handle for later)
    def create_state(self) -> QuantumID | str:
        cmd = QuantumCommand.create_qubit()
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()
        return response.get_content()
        
    # Returns list of all created states
    # Filters result to include only states with this 
    # place's prefix(isolation)
    def list_states(self) -> List[QuantumID] | str:
        cmd = QuantumCommand.list_states()
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()
        
        return [
            id for id in
            response.get_content()
            if id.startswith(self.place_name + "/")
        ]

    def get_stabilizers(self, id: QuantumID) -> List[str] | str:
        cmd = QuantumCommand.get_stabilizers(id)
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()

        return response.get_content()

    def get_state(self, id: QuantumID) -> QuantumState:
        cmd = QuantumCommand.get_state(id)
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()
        
        return response.get_content()
    
    def get_history(self, id: QuantumID) -> QuantumHistory | str:
        cmd = QuantumCommand.get_history(id)
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()
        
        return response.get_content()
    
    def apply_gate(self, id: QuantumID, gate: QuantumGate, target: QuantumID | None = None) -> str | None:
        cmd = QuantumCommand.apply_gate(id, gate, target)
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()
        
    
    def measure(self, id: QuantumID) -> QuantumMeasurement | str:
        cmd = QuantumCommand.measure(id)
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()
        
        return response.get_content()
    
    def seed(self, seed_value: int) -> None | str:
        cmd = QuantumCommand.seed(seed_value)
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()

        return None

    def remove_qubit(self, id: QuantumID) -> bool | str:
        cmd = QuantumCommand.remove(id)
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()
        
        return response.get_content()

    def rename_state(self, id: QuantumID, new_prefix: QuantumPrefix) -> QuantumID | str:
        cmd = QuantumCommand.alias(id, new_prefix)
        response = self._send_command(cmd)
        if response.is_error():
            return response.get_error()

        return response.get_content()
    

        
        

    
    


        
    


