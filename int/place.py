from typing import Any


class Place:
    name: str = None
    block: Any = None

    def __init__(self, name: str, block: Any):
        """
        Initializes the place with a name and the block of code within it

        Parametrs:
            name (str): Place name, specified by the code
            block (Any): Block of code inside the place
        """
        self.name = name
        self.block = block

    


