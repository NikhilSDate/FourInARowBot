from api_wrapper.ai_api import AIAPI
from game.colors import Color
from game.game import Game
from game.statuses import Status


class AIGame(Game):

    def __init__(self, human_color=Color.FIRST):
        super().__init__((6, 7), 4) # only support standard dimensions for now
        self.human_color = human_color
        if human_color == Color.FIRST:
            self.ai_color = Color.SECOND
        else:
            self.ai_color = Color.FIRST
        self.status = Status.OK
        self.ai_api = AIAPI()

    def do_move(self, column: int, _: Color = None) -> Status:
        return super().do_move(column, self.human_color)

    async def do_ai_move(self):
        resp = await self.ai_api.evaluation(self.board, self.ai_color)
        evaluation, best_move = resp[0]['v'], resp[0]['action']
        status = super().do_move(best_move, self.ai_color)
        return status

