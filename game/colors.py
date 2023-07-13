from enum import Enum


class Color(Enum):
    EMPTY = 0
    FIRST = 1
    SECOND = 2

    def __repr__(self):
        if self == Color.FIRST:
            return 'F'
        elif self == Color.SECOND:
            return 'S'
        elif self == Color.EMPTY:
            return 'E'

