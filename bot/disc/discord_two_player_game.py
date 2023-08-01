import warnings
from typing import Tuple

from disc.utils import ping
from disc.discord_mixin import DiscordMixin
from game.colors import Color
from game.game import Game
from game.statuses import Status, StatusError, StatusType


class DiscordTwoPlayerGame(Game, DiscordMixin):
    def __init__(self, dims: Tuple[int, int] = (6, 7), winning_length: int = 4, guild=None, channel=None, first_player_id: str = None, second_player_id: str = None):
        super().__init__(dims, winning_length)
        self.players = {first_player_id: Color.FIRST, second_player_id: Color.SECOND}
        self.colors = {Color.FIRST: 'RED', Color.SECOND: 'BLUE'}
        self.guild = guild
        self.channel = channel
        self.first_player_id = first_player_id
        self.second_player_id = second_player_id
    
    def handle_resign(self, player_id: str):
        super().handle_resign(self.players[player_id])


        







