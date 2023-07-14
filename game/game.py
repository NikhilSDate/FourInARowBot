from typing import Tuple, Optional

from game.colors import Color
from game.connect_four_board import ConnectFourBoard
from game.statuses import Status, StatusError


class Game:

    def __init__(self, dims: Tuple[int, int] = (6, 7)):
        self.board = ConnectFourBoard(dims)
        self.moves = []
        self.status: Status = Status.OK

    def do_move(self, column: int, color: Optional[Color] = None) -> Status:
        if self.status != Status.OK:
            raise StatusError('Board must be in a valid state to call do_move()')
        if color is None:
            if len(self.moves) % 2 == 0:
                color = Color.FIRST
            else:
                color = Color.SECOND
        elif color == Color.FIRST and len(self.moves) % 2 != 0 or color == Color.SECOND and len(self.moves) % 2 == 0:
            return Status.WRONG_TURN
        elif not 0 <= column < self.board.shape[1]:
            return Status.INVALID_INDEX

        status = self.board.do_move(column, color)
        if status == Status.OK:
            self.moves.append(column)
        else:
            return status

        if self.board.eval_game_state((self.board.envelope(column) - 1, column), color):
            if color == Color.FIRST:
                self.status = Status.FIRST_WINS_BY_POSITION
                return Status.FIRST_WINS_BY_POSITION
            else:
                self.status = Status.SECOND_WINS_BY_POSITION
                return Status.SECOND_WINS_BY_POSITION
        elif self.board.full():
            self.status = Status.DRAW_BY_STALEMATE
            return Status.DRAW_BY_STALEMATE

        return Status.OK

    def handle_resign(self, color: Color):
        if color == Color.FIRST:
            self.status = Status.SECOND_WINS_BY_RESIGNATION
        elif color == Color.SECOND:
            self.status = Status.FIRST_WINS_BY_RESIGNATION








