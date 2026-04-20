from .logger import log,WARNING

class NumVar:
    """
    Represents a variable that can hold an integer value. It is used to store the value of variables in the program. It is not limited to a specific number of bits, but it can be used to represent any integer value.
    """
    type: str = "Num"
    def __init__(self,initial_value: float = 0.0):
        self.value = float(initial_value)

    def set(self,new_value: float):
        self.value = float(new_value)

    def get(self) -> float:
        # If the value is an integer, return it as an int, otherwise return it as a float
        if self.value.is_integer():
            return int(self.value)
        return self.value

# Klasa zrobiona pod obslugiwanie tablic numerycznych
class NumArray:
    """
        Represents an array of classical numerical variables.
        """
    type: str = "NumArray"

    def __init__(self, size: int):
        self.size = size
        self.values = [0.0 for _ in range(size)]

    def set(self, index: int, new_value: float):
        if not (0 <= index < self.size):
            raise IndexError(f"Index {index} is out of bounds for array of size {self.size}.")
        try:
            self.values[index] = float(new_value)
        except ValueError:
            pass

    def get(self, index: int) -> float:
        if not (0 <= index < self.size):
            raise IndexError(f"Index {index} is out of bounds for array of size {self.size}.")
        val = self.values[index]
        return int(val) if val.is_integer() else val