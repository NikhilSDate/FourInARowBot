import datetime

from flask import Flask
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId
from pymongo.cursor import Cursor


class DBManager:

    def __init__(self, app: Flask):
        self.db = PyMongo(app).db

    def add_game(self, first_player_id: str, second_player_id: str, moves: list, result: int, dtime: datetime):
        doc = {
            "first_player_id": first_player_id,
            "second_player_id": second_player_id,
            "moves": moves,
            "result": result,
            "dtime": dtime
        }

        return self.db.games.insert_one(doc)

    def get_game(self, game_id) -> Cursor:
        return self.db.games.find({"_id": ObjectId(game_id)})
