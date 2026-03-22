from typing import List


class StateRegister:
    """
    Represents a quantum register
    """
    states: List[State]
    type: str = "StateRegister"
    
    def __init__(self, size: int):
        """
        Creates a quantum register with given size
        """
        self.states = [State() for i in range(size)]

    def size(self) -> int:
        return len(self.states)

class State:
    """
    Represents a quantum state
    """
    state = 0 # just a placeholder, there will be something else
    type: str = "State"