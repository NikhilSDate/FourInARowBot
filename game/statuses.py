from enum import Enum


class Status(Enum):
    OK = 0
    COLUMN_FULL = 1
    WRONG_TURN = 2
    FIRST_WINS = 3
    SECOND_WINS = 4
    DRAW = 5
