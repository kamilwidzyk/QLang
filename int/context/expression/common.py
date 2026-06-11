from typing import Any


def parse_prefix_int(text: str) -> int:
    """
    Parse string to number, hex(0x) and bin(0b) prefix supported, case ignored
    """
    try:
        text = text.lower()
        if text.startswith("0x"):
            return int(text, 16)
        if text.startswith("0b"):
            return int(text, 2)
        return int(text)
    except:
        return 0
    

