from typing import Tuple

from discord import Guild
from discord.abc import Messageable

from disc.discord_ai_game_manager import DiscordAIGameManager
from disc.discord_two_player_game_manager import DiscordTwoPlayerGameManager
from game.statuses import Status


class DiscordManager:
    def __init__(self):
        self.two_player_game_manager: DiscordTwoPlayerGameManager = DiscordTwoPlayerGameManager()
        self.ai_game_manager: DiscordAIGameManager = DiscordAIGameManager()

    async def new_game(self, channel: Messageable, guild: Guild, first_player_id: str, second_player_id: str, dims: Tuple[int, int] = (6, 7), winning_length: int = 4) -> Status:
        if first_player_id == 'ai' or second_player_id == 'ai':
            return await self.ai_game_manager.new_game(channel=channel, guild=guild, first_player_id=first_player_id, second_player_id=second_player_id, dims=dims, winning_length=winning_length)
        else:
            return await self.two_player_game_manager.new_game(channel=channel, guild=guild, first_player_id=first_player_id, second_player_id=second_player_id, dims=dims, winning_length=winning_length)

    async def do_move(self, channel: Messageable, player_id: str, column: int) -> Status:
        if channel in self.two_player_game_manager.games:
            return await self.two_player_game_manager.do_move(channel, player_id, column)
        else:
            return await self.ai_game_manager.do_move(channel, player_id, column)

    async def handle_resign(self, channel, player_id) -> Status:
        if channel in self.two_player_game_manager.games:
            return await self.two_player_game_manager.handle_resign(channel, player_id)
        else:
            return await self.ai_game_manager.handle_resign(channel, player_id)


