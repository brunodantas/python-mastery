from functools import total_ordering


@total_ordering
class MutInt:
    __slots__ = ["value"]

    def __init__(self, value) -> None:
        self.value = value

    def __int__(self):
        return self.value

    __index__ = __int__

    def __float__(self):
        return float(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"MutInt({self.value})"

    def __format__(self, format_spec: str) -> str:
        return format(self.value, format_spec)

    def __add__(self, other):
        if isinstance(other, MutInt):
            return MutInt(self.value + other.value)
        elif isinstance(other, int):
            return MutInt(self.value + other)
        else:
            return NotImplemented

    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, MutInt):
            self.value += other.value
            return self
        elif isinstance(other, int):
            self.value += other
            return self
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MutInt):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, MutInt):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        else:
            return NotImplemented
