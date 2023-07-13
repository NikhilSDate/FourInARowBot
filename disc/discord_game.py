from typing import Tuple

from game.colors import Color
from game.game import Game


class DiscordGame(Game):
    def __init__(self, dims: Tuple[int, int] = (6, 7), channel=None, first_player_id: str = None, second_player_id: str = None):
        super().__init__(dims)
        self.players = {first_player_id: Color.FIRST, second_player_id: Color.SECOND}
        self.channel = channel

    def get_player_color(self, player_id: str) -> Color:
        return self.players[player_id]

    def to_message(self) -> str:
        emojis = {Color.FIRST: "\U0001F534", Color.SECOND: "\U0001F7E1", Color.EMPTY: "\u26AA"}
        message = ''
        # flip board upside down
        for i in range(self.board.shape[0] - 1, -1, -1):
            for j in range(self.board.shape[1]):
                message += emojis[self.board.shape[i][j]]
            message += '\n'
        return message




