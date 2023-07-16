from typing import Tuple, Optional


from game.colors import Color
from game.game import Game
from game.statuses import Status, StatusType
from minimax import alpha_beta_search


class AIGame(Game):

    def __init__(self, human_color=Color.FIRST):
        super().__init__((6, 7), 4)
        self.human_color = human_color
        if human_color == Color.FIRST:
            self.ai_color = Color.SECOND
        else:
            self.ai_color = Color.FIRST
        self.status = Status.OK

    def do_move(self, column: int, color: Optional[Color] = None) -> Status:
        if color != self.human_color:
            raise ValueError('color must be equal to self.human_color')

        status = super().do_move(column, color)
        if status != Status.OK:
            return status

        evaluation, best_move = alpha_beta_search(self.board, self.ai_color)
        status = super().do_move(best_move, self.ai_color)
        return status

