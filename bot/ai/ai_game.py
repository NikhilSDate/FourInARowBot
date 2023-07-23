from typing import Tuple, Optional

from api_wrapper.ai_api import AIApi
from game.colors import Color
from game.game import Game
from game.statuses import Status


class AIGame(Game):

    def __init__(self, human_color=Color.FIRST):
        super().__init__((6, 7), 4)
        self.human_color = human_color
        if human_color == Color.FIRST:
            self.ai_color = Color.SECOND
        else:
            self.ai_color = Color.FIRST
        self.status = Status.OK
        self.ai_api = AIApi()

    def do_move(self, column: int, color: Optional[Color] = None) -> Status:
        if color != self.human_color:
            raise ValueError('color must be equal to self.human_color')

        status = super().do_move(column, color)
        if status != Status.OK:
            return status

    async def do_ai_move(self):
        resp = await self.ai_api.evaluation(self.board, self.ai_color)
        evaluation, best_move = resp[0]['v'], resp[0]['action']
        status = super().do_move(best_move, self.ai_color)
        return status

