from typing import Dict

from discord.abc import Messageable

from disc.discord_game import DiscordGame
from game.game import Game


class DiscordGameManager:
    def __init__(self):
        self.games: Dict[Messageable, DiscordGame] = {}

    def new_game(self, channel: Messageable, first_player_id: str, second_player_id: str):
        self.games[channel] = DiscordGame(channel=channel, first_player_id=first_player_id, second_player_id=second_player_id)

    def remove_game(self, channel: Messageable):
        del self.games[channel]



DiscordGameManager()
