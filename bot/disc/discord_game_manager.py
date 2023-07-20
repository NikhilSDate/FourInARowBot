from typing import Dict, Tuple

from discord import Guild

from discord.abc import Messageable

from disc.discord_game import DiscordGame
from game.statuses import Status
from api_wrapper.data_api import save_discord_game


class DiscordGameManager:
    def __init__(self):
        self.games: Dict[Messageable, DiscordGame] = {}

    async def new_game(self, channel: Messageable, guild: Guild, first_player_id: str, second_player_id: str, dims: Tuple[int, int] = (6, 7), winning_length: int = 4) -> Status:
        if channel in self.games:
            return Status.CHANNEL_BUSY
        self.games[channel] = DiscordGame(dims=dims, winning_length = winning_length, guild=guild, channel=channel, first_player_id=first_player_id, second_player_id=second_player_id)
        await channel.send(self.games[channel].color_assignment_to_message())
        return Status.OK

    def remove_game(self, channel: Messageable):
        del self.games[channel]

    def do_move(self, channel: Messageable, player_id: str, column: int) -> Status:
        if channel not in self.games or player_id not in self.games[channel].players:
            return Status.NO_ACTIVE_GAME
        return self.games[channel].do_move(column, self.games[channel].get_player_color(player_id))

    async def print_board(self, channel: Messageable):
        await channel.send(self.games[channel].to_message())

    async def handle_game_over(self, channel):
        await channel.send(self.games[channel].result_to_message())
        await save_discord_game(self.games[channel])
        self.remove_game(channel)

    async def handle_resign(self, channel: Messageable, player_id: str) -> Status:
        if channel not in self.games or player_id not in self.games[channel].players:
            return Status.NO_ACTIVE_GAME
        self.games[channel].handle_resign(player_id=player_id)
        await self.handle_game_over(channel)
        return Status.OK


