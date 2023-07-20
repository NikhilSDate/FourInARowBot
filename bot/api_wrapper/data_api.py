import os

from disc.discord_game import DiscordGame
from api_wrapper.config import DATA_SERVER_URL
from game.statuses import Status
import asyncio
import aiohttp
from datetime import datetime


async def save_discord_game(game: DiscordGame):
    API_KEY = os.getenv('DATA_API_KEY')
    url = DATA_SERVER_URL + "/add-game"
    body = {
        "first_player_id": game.first_player_id,
        "second_player_id": game.second_player_id,
        "guild_id": game.guild.id,
        "channel_id": game.channel.id,
        "rows": game.board.shape[0],
        "columns": game.board.shape[1],
        "winning_length": game.winning_length,
        "moves": game.moves,
        "result": status_to_result(game.status),
        "datetime": datetime.now().isoformat()
    }
    header = {"Authorization": API_KEY}
    async with aiohttp.ClientSession() as session:
        # change ssl to true later
        async with session.post(url, json=body, headers=header, ssl=False) as response:
            return await response.text(), response.status


async def get_stats(player_id: str, against: str = None):
    API_KEY = os.getenv('DATA_API_KEY')
    url = DATA_SERVER_URL + f"/stats/userid/{player_id}"
    header = {"Authorization": API_KEY}
    params = {"other_player_id": against}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header, params=params, ssl=False) as response:
            return await response.text(), response.status


def status_to_result(status: Status):
    if status == Status.DRAW_BY_STALEMATE:
        return 0
    elif status == Status.DRAW_BY_AGREEMENT:
        raise NotImplementedError()
    elif status == Status.FIRST_WINS_BY_POSITION:
        return 1
    elif status == Status.FIRST_WINS_BY_RESIGNATION:
        return 2
    elif status == Status.SECOND_WINS_BY_POSITION:
        return -1
    elif status == Status.SECOND_WINS_BY_RESIGNATION:
        return -2
