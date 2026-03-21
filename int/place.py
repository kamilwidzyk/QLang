from typing import Any, List
from multiprocessing import Process
import time
from network import QuantumNetwork
from script_errors import ScriptErrors

class Place:
    """
    Represents one place, holds name and inner code
    """
    name: str = None
    block: List[Any] = []
    network: QuantumNetwork
    script_errors: ScriptErrors

    def __init__(self, name: str, script_errors: ScriptErrors, network: QuantumNetwork):
        """
        Initializes the place with a name

        Parameters:
            name (str): Place name, specified by the code
            script_errors (ScriptErrors): instance of class for displaying errors
            network (QuauntumNetwork): instance of QuantumNetwork
        """
        self.name = name
        self.script_errors = script_errors
        self.network = network

    def add_code(self, code: Any):
        """
        Adds code to this place

        Parameters:
            code (Any): code to add to this place, type depends on code
        """
        self.block.append(code)

    def process_target(self):
        """
        Place execution entry point
        """
        print(f"[{self.name}] Started!")

        if(self.name == "global"):
            time.sleep(3)
            print("[global] Wait over, sending to ClassicalSystem")
            self.network.send("global", "hello", "ClassicalSystem", False, 2, [False, True])
        elif(self.name == "ClassicalSystem"):
            time.sleep(1)
            print("[ClassicalSystem] Wait over, receiving...")
            data = self.network.wait_for("ClassicalSystem", "global", "hello", False, 2)
            print("[ClassicalSystem] Received packet: " + str(data))
        

    def run(self):
        """
        Starts execution of this place inside a separate process
        """
        self.proc = Process(target=self.process_target)
        self.proc.start()

    def wait_for_end(self):
        """
        Waits for execution to finish
        """
        self.proc.join()


    


