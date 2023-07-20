import datetime
import pprint

from flask import Flask, g, current_app
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId
from pymongo.cursor import Cursor
from werkzeug.local import LocalProxy


# schema:
# collection games:
# "first_player_id": string (can be 'ai')
# "second_player_id": string (can be 'ai')
# "moves": string
# "result": integer (0 is draw by full board, 1 is first player wins by position, 2 is first player wins by resignation, -1 is second player wins by position, -2 is second player wins by resignation"
# "guild_id": string
# "datetime": date and time object

# collection player
# "player_id": string
# "rating": (somehow store time series)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        print('db is none')
        db = g._database = PyMongo(current_app).db
    return db

db = LocalProxy(get_db)
def add_game(first_player_id: str, second_player_id: str, guild_id: str, channel_id: str, moves: list,
             result: int, dtime: datetime):
    doc = {
        "first_player_id": first_player_id,
        "second_player_id": second_player_id,
        "guild_id": guild_id,
        "channel_id": channel_id,
        "moves": moves,
        "result": result,
        "dtime": dtime
    }

    return db.games.insert_one(doc)

def get_game(game_id) -> Cursor:
    return db.games.find({"_id": ObjectId(game_id)})

def get_stats(player_id: str, other_player_id=None, guild_id: str = None, from_date: datetime = None,
              to_date: datetime = None):

    pipeline = []
    pipeline.extend([
        {
            "$match": {"$or": [{"first_player_id": player_id}, {"second_player_id": player_id}]}
        }
    ]
    )
    if other_player_id is not None:
        pipeline.extend([
            {
                "$match": {"$or": [{"first_player_id": other_player_id}, {"second_player_id": other_player_id}]}
            }
            ]
        )
    if guild_id is not None:
        pipeline.extend([
            {
                "$match": {"guild_id": guild_id}
            }
            ]
        )
    if from_date is not None:
        pipeline.extend([
            {
                "$match": {"datetime": {"$gte": from_date}}
            }
            ]
        )
    if to_date is not None:
        pipeline.extend([
            {
                "$match": {"datetime": {"$lte": to_date}}
            }
            ]
        )
    pipeline.extend([
        {
            "$project":
                {
                    "player_result": {"$cond": [{"$eq": ["$first_player_id", player_id]}, "$result", {"$subtract": [0, "$result"]}]}
                }
        },

        {
            "$group": {"_id": "$player_result", "count": {"$sum": 1}}
        }
    ])
    return db.games.aggregate(pipeline)

def get_api_key_details(hashed_key):
    return db.api_keys.find({"key": hashed_key})
