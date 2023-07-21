from typing import Optional

from ai.ai_game import AIGame
from disc.DiscordMixin import DiscordMixin
from game.colors import Color
from game.statuses import Status


class DiscordAIGame(AIGame, DiscordMixin):

    def __init__(self, channel=None, player_color=Color.FIRST, player_id: str = None):
        super().__init__(player_color)
        self.player_color = player_color
        self.player_id = player_id
        self.players = {self.player_id: self.player_color}
        self.channel = channel
        self.colors = {Color.FIRST: 'RED', Color.SECOND: 'BLUE'}

    def handle_resign(self, player_id: str):
        super().handle_resign(self.players[player_id])


