from typing import Dict, Tuple

from discord.abc import Messageable

from disc.discord_game import DiscordGame
from disc.discord_match import DiscordMatch
from game.statuses import Status


class DiscordManager:
    def __init__(self):
        self.games: Dict[Messageable, DiscordGame] = {}
        self.matches: Dict[Messageable, DiscordMatch] = {}

    async def new_game(self, channel: Messageable, first_player_id: str, second_player_id: str, dims: Tuple[int, int] = (6, 7), winning_length: int = 4) -> Status:
        if channel in self.games:
            return Status.CHANNEL_BUSY
        self.games[channel] = DiscordGame(dims=dims, winning_length = winning_length, channel=channel, first_player_id=first_player_id, second_player_id=second_player_id)
        await channel.send(self.games[channel].color_assignment_to_message())
        return Status.OK

    async def new_match(self, channel: Messageable, first_player_id: str, second_player_id: str, dims: Tuple[int, int] = (6, 7), winning_length: int = 4):
        pass


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
        self.remove_game(channel)

    async def handle_resign(self, channel: Messageable, player_id: str) -> Status:
        if channel not in self.games or player_id not in self.games[channel].players:
            return Status.NO_ACTIVE_GAME
        self.games[channel].handle_resign(player_id=player_id)
        await self.handle_game_over(channel)
        return Status.OK


