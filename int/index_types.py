"""
Index types for QLang variable indexing.

SimpleIndex: standard single-element index (supports negative values)
RangeIndex:  slice [start..end) — start inclusive, end exclusive
ListIndex:   selection by list of indices [[a, b, c]]
"""


class SimpleIndex:
    """Standard single index, supports negative values for counting from end."""
    def __init__(self, value: int):
        self.value = int(value)

    def resolve(self, length: int) -> int:
        """Resolve negative indices against container length."""
        idx = self.value
        if idx < 0:
            idx += length
        return idx

    def __repr__(self):
        return f"SimpleIndex({self.value})"


class RangeIndex:
    """Range index [start..end), inclusive start, exclusive end."""
    def __init__(self, start: int, end: int):
        self.start = int(start)
        self.end = int(end)

    def resolve(self, length: int) -> tuple[int, int]:
        """Resolve negative indices against container length."""
        start = self.start
        end = self.end
        if start < 0:
            start += length
        if end < 0:
            end += length
        return start, end

    def __repr__(self):
        return f"RangeIndex({self.start}..{self.end})"


class ListIndex:
    """Index list [[a, b, c]] — selects elements at given positions."""
    def __init__(self, indices: list[int]):
        self.indices = [int(i) for i in indices]

    def resolve(self, length: int) -> list[int]:
        """Resolve negative indices against container length."""
        result = []
        for idx in self.indices:
            if idx < 0:
                idx += length
            result.append(idx)
        return result

    def __repr__(self):
        return f"ListIndex({self.indices})"
