from typing import Tuple

from game.game import Game


class DiscordGame(Game):
    def __init__(self, dims: Tuple[int, int] = (6, 7), channel=None, first_player_id: str = None, second_player_id: str = None):
        super().__init__(dims)
        self.first_player_id = first_player_id
        self.second_player_id = second_player_id
        self.channel = channel
