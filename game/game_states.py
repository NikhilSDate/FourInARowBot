from enum import Enum


class GameState(Enum):
    CONTINUE = 0
    FIRST_PLAYER_WINS = 1
    SECOND_PLAYER_WINS = 2
    DRAW = 3
