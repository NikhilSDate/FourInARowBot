from typing import Dict

from discord.abc import Messageable

from disc.discord_game import DiscordGame
from game.statuses import Status


class DiscordGameManager:
    def __init__(self):
        self.games: Dict[Messageable, DiscordGame] = {}

    def new_game(self, channel: Messageable, first_player_id: str, second_player_id: str):
        self.games[channel] = DiscordGame(channel=channel, first_player_id=first_player_id, second_player_id=second_player_id)

    def remove_game(self, channel: Messageable):
        del self.games[channel]

    def do_move(self, channel, player_id, column) -> Status:
        if channel not in self.games or player_id not in self.games[channel].players:
            return Status.NO_ACTIVE_GAME
        return self.games[channel].do_move(column, self.games[channel].get_color(player_id))






DiscordGameManager()
