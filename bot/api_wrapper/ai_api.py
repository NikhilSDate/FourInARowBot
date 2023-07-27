import asyncio
import json

import aiohttp
from numpy import vectorize

from api_wrapper.utils import Singleton
from game.colors import Color
from game.connect_four_board import ConnectFourBoard


class AIApi(metaclass=Singleton):
    def __init__(self):
        with open('config.json', 'r') as config_file:
            content = config_file.read()
        self.AI_API_URL = json.loads(content).get('AI_API_URL', 'http://127.0.0.1:5000')

    async def evaluation(self, board: ConnectFourBoard, color: Color):
        url = self.AI_API_URL + "/evaluate"
        params = {"board": AIApi.encode_board(board), "color": AIApi.encode_color(color)}
        async with aiohttp.ClientSession() as session:
            for depth in range(5, -1, -1):
                params.update({"depth": depth})
                async with session.get(url=url, params=params) as response:
                    txt, status = json.loads(await response.text()), response.status
                    if status == 200:
                        return txt, status


    @staticmethod
    def encode_board(board: ConnectFourBoard):
        @vectorize
        def color_to_int(color: Color) -> str:
            if color == Color.EMPTY:
                return '0'
            elif color == Color.FIRST:
                return '1'
            elif color == Color.SECOND:
                return '2'
        return ''.join((color_to_int(board._board)).flatten())

    @staticmethod
    def encode_color(color: Color):
        if color == Color.FIRST:
            return '1'
        elif color == Color.SECOND:
            return '2'


if __name__ == '__main__':
    ai_api = AIApi()
    board = ConnectFourBoard()
    color = Color.FIRST
    print(asyncio.run(ai_api.evaluation(board, color)))

