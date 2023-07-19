import configparser
import functools
import hashlib
import json
import os
from datetime import datetime

from flask import Flask, request, jsonify, abort
from flask_pymongo import PyMongo
from bson import json_util

from db.db import DBManager

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))
app = Flask(__name__)
app.config['MONGO_URI'] = config['DEV']['DB_URI']
app.config['DEBUG'] = True
mongo = PyMongo(app)


# @app.route("/")
# def home():
#     return json_util.dumps(mongo.db.games.find({}))


db_manager = DBManager(app)


def check_api_key(key):
    docs = list(db_manager.get_api_key_details(hashlib.sha256(key.encode('utf-8')).hexdigest()))
    return len(docs) == 1


def require_api_key(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get('Authorization')
        if key and check_api_key(key):
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper




@app.route("/add-game", methods=['POST'])
@require_api_key
def add_game():
    new_game = request.get_json()
    _id = db_manager.add_game(new_game['first_player_id'], new_game['second_player_id'], new_game['guild_id'], new_game['channel_id'],
                              new_game['moves'], new_game['result'], datetime.fromisoformat(new_game['datetime']))
    return json_util.dumps(db_manager.get_game(_id.inserted_id))


@app.route("/stats/userid/<string:player_id>", methods=['GET'])
@require_api_key
def get_stats(player_id):
    other_player_id = request.args.get('other_player_id')
    guild_id = request.args.get('guild_id')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    from_date = datetime.fromisoformat(from_date) if from_date is not None else None
    to_date = datetime.fromisoformat(to_date) if to_date is not None else None

    stats = db_manager.get_stats(player_id, other_player_id, guild_id, from_date, to_date)

    # process result
    stat_dict = {result: 0 for result in [-2, -1, 0, 1, 2]}
    for stat in stats:
        stat_dict[int(stat["_id"])] = stat["count"]

    return json.dumps(stat_dict)


app.run(ssl_context='adhoc')
