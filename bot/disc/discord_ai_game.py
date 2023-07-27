from typing import Optional

from ai.ai_game import AIGame
from disc.discord_mixin import DiscordMixin
from game.colors import Color
from game.statuses import Status


class DiscordAIGame(AIGame, DiscordMixin):

    def __init__(self, guild=None, channel=None, first_player_id: str = None, second_player_id: str = None):
        if first_player_id == 'ai':
            human_color = Color.SECOND
            self.players = {second_player_id: Color.SECOND}
        else:
            human_color = Color.FIRST
            self.players = {first_player_id: Color.FIRST}

        super().__init__(human_color)
        self.colors = {Color.FIRST: 'RED', Color.SECOND: 'BLUE'}
        self.guild = guild
        self.channel = channel
        self.first_player_id = first_player_id
        self.second_player_id = second_player_id

    def handle_resign(self, player_id: str):
        super().handle_resign(self.players[player_id])


