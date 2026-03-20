from typing import Any, List
from multiprocessing import Process
import time


class Place:
    """
    Represents one place, holds name and inner code
    """
    name: str = None
    block: List[Any] = []

    def __init__(self, name: str):
        """
        Initializes the place with a name

        Parameters:
            name (str): Place name, specified by the code
        """
        self.name = name

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
        print(f"Place {self.name} started!")
        time.sleep(5)
        print(f"Place {self.name} waited")

    def run(self):
        """
        Starts execution of this place inside a separate process
        """
        proc = Process(target=self.process_target)
        proc.start()


    


