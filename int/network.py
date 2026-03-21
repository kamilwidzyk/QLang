import multiprocessing
import time
import uuid
from typing import List, Any, Tuple
from dataclasses import dataclass
from logger import log, DEBUG, QNET, SUCCESS, FATAL, STYLE_DEBUG, STYLE_DEBUG_CYAN, STYLE_DEBUG_MAGENTA, STYLE_DEBUG_YELLOW
from script_errors import ScriptErrors
import colorama

@dataclass
class Packet:
    """
    Represents a packet inside the QuantumNetwork
    """
    msg_id: str
    src_id: str
    target_id: str
    data: Any
    quantum: bool
    size: int
    seq_id: int = 0

class QuantumNetwork:
    """
    Controls a Quantum Network used by places to send and receive data.
    Each packet is represented by Packet instance.
    
    When sending a packet you need to provide:
        > src_id - name the of your place
        > quantum - qubits/classis bits
        > size - data size in bits
        > data - the data to send, most likely a class instance
        Optionally:
            > msg_id - name of the packet
            > target_id - only place with this name can receive it

    How packets are selected for receivers:
        To receive a packet you need to specify:
            > target_id - name of your place
            > quantum - is the data qubits or classic bits?
            > size - how many bits your receiving state/obs is
        Optionally specify:
            > msg_id - name of packet you want, eg. 'selection', 'result'
            > src_id - name of the place packet was sent from
            
        1. quantum and size must match
        2. If sender specified target_id -> target_id must match
        3. If received specified src_id -> src_id must match
        4. msg_id matching:
            a. sender and receiver specified a msg_id: they must match
            b. sender and receiver not specified a msg_id: condition satisfied (None == None)
            c. sender specified, receiver did not: condition satisfied
            d. sender did not specify, receiver did: condition failed
        All conditions satisfied -> packet can be received

    """


    def __init__(self, packet_pool, global_counter, condition):
        """
        Starts the quantum network. Do it before starting places.
        """
        self.packet_pool = packet_pool
        self.global_counter = global_counter
        self.condition = condition

        log(QNET, SUCCESS, "Network is up")

    def send(self, src_id: str, msg_id: str | None, target_id: str | None, 
             quantum: bool, size: int, data: Any):
        """
        Sends a packet from one place to another. 
        
        Parameters:
            src_id (str): Name of the place from where the packet is being sent
                          Needs to be in valid_places
            msg_id (str|None): Optional packet type, give None if not used
            target_id (str|None): Optional receiving place name, give None of not used
                                  Needs to be in valid_places
            quantum (bool): type of data sent, True=qubit False=classic
            size (int): data size in bits, used to match the packets to receiver sizes
        """
        seq_val = None

        with self.condition:
            self.global_counter.value += 1
            seq_val = self.global_counter.value

            packet = Packet(
                src_id=src_id,
                msg_id=msg_id,
                target_id=target_id,
                quantum=quantum,
                size=size,
                data=data,
                seq_id=seq_val
            )

            self.packet_pool.append(packet)
            self.condition.notify_all()
        
        info = "Unnamed packet " if msg_id is None else f"Packet named {STYLE_DEBUG_MAGENTA}{msg_id}{STYLE_DEBUG} "
        info += f"sent from {STYLE_DEBUG_MAGENTA}{src_id}{STYLE_DEBUG} containing {STYLE_DEBUG_YELLOW}{size}{STYLE_DEBUG} "
        info += "quantum " if quantum else "classical "
        info += "bits"
        info += " " if target_id is None else f" to {STYLE_DEBUG_MAGENTA}{target_id}{STYLE_DEBUG} "
        info += f"({STYLE_DEBUG_CYAN}ID {seq_val}{STYLE_DEBUG})"
        log(QNET, DEBUG, info)

    
    def wait_for(self, target_id: str, src_id: str | None, msg_id: str | None, quantum: bool, size: int) -> Any:
        """
        Waits for specified packet to arrive

        Parameters:
            target_id (str): Name of the place waiting for packet
            src_id (str|None): Optional name of the place that sent the packet
            msg_id (str|None): Optional packet type
            quantum (bool): type of data sent, True=qubit False=classic
            size (int): data size in bits, used to match the packet 
        Returns:
            Content of the mathing packet
        """
        info = "Waiting for "
        info += "an unnamed packet " if msg_id is None else f"a packet named {STYLE_DEBUG_MAGENTA}{msg_id}{STYLE_DEBUG} "
        info += f"sent from {STYLE_DEBUG_MAGENTA}{src_id}{STYLE_DEBUG} containing {STYLE_DEBUG_YELLOW}{size}{STYLE_DEBUG} "
        info += "quantum " if quantum else "classical "
        info += "bits"
        info += " " if target_id is None else f" to {STYLE_DEBUG_MAGENTA}{target_id}{STYLE_DEBUG} "
        log(QNET, DEBUG, info)

        with self.condition:
            while True:
                match_index = -1

                for i, packet in enumerate(self.packet_pool):

                    # check size and quantum/classical
                    if packet.size != size:
                        continue
                    if packet.quantum != quantum:
                        continue
                    # check packet destination
                    if packet.target_id is not None and packet.target_id != target_id:
                        continue
                    # check packet source
                    if src_id is not None and packet.src_id != src_id:
                        continue
                    # msg_id, both specified -> must match
                    if msg_id is not None and packet.msg_id is not None and msg_id != packet.msg_id:
                        continue
                    # sender specified, receiver did not: condition satisfied
                    if msg_id is not None and packet.msg_id is None:
                        continue
                    # sender did not specify, receiver did: condition failed
                    if packet.msg_id is None and msg_id is not None:
                        continue
                    # sender and receiver did not specify msg_id (nothing to check)
                    
                    # all conditions satisfied, receive this packet
                    match_index = i
                    break

                if match_index != -1:
                    # log info
                    packet: Packet = self.packet_pool.pop(match_index)

                    info = "Unnamed packet " if packet.msg_id is None else f"Packet named {STYLE_DEBUG_MAGENTA}{packet.msg_id}{STYLE_DEBUG} "
                    info += f"received from {STYLE_DEBUG_MAGENTA}{packet.src_id}{STYLE_DEBUG} containing {STYLE_DEBUG_YELLOW}{packet.size}{STYLE_DEBUG} "
                    info += "quantum " if packet.quantum else "classical "
                    info += "bits"
                    info += " " if packet.target_id is None else f" by {STYLE_DEBUG_MAGENTA}{packet.target_id}{STYLE_DEBUG} "
                    info += f"({STYLE_DEBUG_CYAN} ID {packet.seq_id}{STYLE_DEBUG})"
                    log(QNET, DEBUG, info)

                    return packet.data
                
                self.condition.wait()





def create_quantum_network() -> Tuple:
    """
    Returns instance of QuantumNetwork and manager.
    Do not create QuantumNetwork instace direcly
    """
    manager = multiprocessing.Manager()
    packet_pool = manager.list()
    condition = manager.Condition(manager.Lock())
    global_counter = manager.Value('i', 0)

    return QuantumNetwork(packet_pool, global_counter, condition), manager