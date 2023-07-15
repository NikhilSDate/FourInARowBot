from enum import Enum


class Status(Enum):
    OK = 0
    COLUMN_FULL = 1
    WRONG_TURN = 2
    FIRST_WINS_BY_POSITION = 3
    SECOND_WINS_BY_POSITION = 4
    FIRST_WINS_BY_RESIGNATION = 5
    SECOND_WINS_BY_RESIGNATION = 6
    DRAW_BY_STALEMATE = 5
    DRAW_BY_AGREEMENT = 6
    FIRST_WINS_MATCH = 7
    SECOND_WINS_MATCH = 8
    DRAW_MATCH = 9
    NO_ACTIVE_GAME = 10
    INVALID_INDEX = 11
    CHANNEL_BUSY = 12


class StatusType(set, Enum):
    ERROR = {Status.COLUMN_FULL, Status.WRONG_TURN, Status.WRONG_TURN, Status.NO_ACTIVE_GAME, Status.INVALID_INDEX,
             Status.CHANNEL_BUSY}
    FIRST_WINS_GAME = {Status.FIRST_WINS_BY_POSITION, Status.FIRST_WINS_BY_RESIGNATION}
    SECOND_WINS_GAME = {Status.SECOND_WINS_BY_POSITION, Status.SECOND_WINS_BY_RESIGNATION}
    WIN_GAME = {*FIRST_WINS_GAME, *SECOND_WINS_GAME}
    DRAW_GAME = {Status.DRAW_BY_STALEMATE, Status.DRAW_BY_AGREEMENT}
    GAME_OVER = {*WIN_GAME, *DRAW_GAME}
    WIN_MATCH = {Status.FIRST_WINS_MATCH, Status.SECOND_WINS_MATCH}
    DRAW_MATCH = {Status.DRAW_MATCH}
    MATCH_OVER = {}


class StatusError(Exception):
    pass
