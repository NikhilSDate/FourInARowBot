import os

from api_wrapper.utils import Singleton
from disc.discord_game import DiscordGame
from game.statuses import Status
import json
import aiohttp
from datetime import datetime


class DataAPI(metaclass=Singleton):

    def __init__(self):
        self.api_key = os.getenv('DATA_API_KEY')
        if self.api_key is None:
            raise ValueError('API key must not be None')
        with open('config.json', 'r') as config_file:
            content = config_file.read()
        self.DATA_API_URL = json.loads(content).get('DATA_API_URL', '127.0.0.1:5000')


    @property
    def authorization_header(self):
        return {'Authorization': self.api_key}

    async def save_discord_game(self, game: DiscordGame):

        url = self.DATA_API_URL + "/add-game"
        body = {
            "first_player_id": game.first_player_id,
            "second_player_id": game.second_player_id,
            "guild_id": str(game.guild.id),
            "channel_id": str(game.channel.id),
            "rows": game.board.shape[0],
            "columns": game.board.shape[1],
            "winning_length": game.winning_length,
            "moves": game.moves,
            "result": DataAPI.status_to_result(game.status),
            "datetime": datetime.now().isoformat()
        }
        async with aiohttp.ClientSession() as session:
            # change ssl to true later
            async with session.post(url, json=body, headers=self.authorization_header, ssl=False) as response:
                return await response.text(), response.status

    async def get_stats(self, player_id: str, other_player_id: str = None,
                        guild_id: str = None, channel_id: str = None, from_date: datetime = None,
                        to_date: datetime = None):

        url = self.DATA_API_URL + f"/stats/userid/{player_id}"
        from_date = from_date.isoformat() if from_date is not None else from_date
        to_date = to_date.isoformat() if to_date is not None else to_date
        params = {"other_player_id": other_player_id, "guild_id": guild_id, "channel_id": channel_id,
                  "from_date": from_date, "to_date": to_date}
        params = {k: v for k, v in params.items() if v is not None}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.authorization_header, params=params, ssl=False) as response:
                return await response.text(), response.status

    @staticmethod
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
