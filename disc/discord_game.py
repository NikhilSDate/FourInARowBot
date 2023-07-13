from typing import Tuple

from game.colors import Color
from game.game import Game


class DiscordGame(Game):
    def __init__(self, dims: Tuple[int, int] = (6, 7), channel=None, first_player_id: str = None, second_player_id: str = None):
        super().__init__(dims)
        self.players = {first_player_id: Color.FIRST, second_player_id: Color.SECOND}
        self.channel = channel

    def get_color(self, player_id: str) -> Color:
        return self.players[player_id]
