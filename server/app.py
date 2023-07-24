import configparser
import json
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request
from flask_pymongo import PyMongo
from bson import json_util

from db.db import get_game, get_stats, add_game
from security.api_key import require_api_key

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('DB_URI')
app.config['DEBUG'] = True
mongo = PyMongo(app)


@app.route("/add-game", methods=['POST'])
@require_api_key
def add_new_game():
    new_game = request.get_json()
    _id = add_game(new_game['first_player_id'], new_game['second_player_id'], new_game['guild_id'], new_game['channel_id'],
                              new_game['rows'], new_game['columns'], new_game['winning_length'], new_game['moves'], new_game['result'], datetime.fromisoformat(new_game['datetime']))
    return json_util.dumps(get_game(_id.inserted_id))


@app.route("/stats/userid/<string:player_id>", methods=['GET'])
@require_api_key
def get_player_stats(player_id):
    other_player_id = request.args.get('other_player_id')
    guild_id = request.args.get('guild_id')
    channel_id = request.args.get('channel_id')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    from_date = datetime.fromisoformat(from_date) if from_date is not None else None
    to_date = datetime.fromisoformat(to_date) if to_date is not None else None

    stats = get_stats(player_id, other_player_id, guild_id, channel_id, from_date, to_date)

    # process result
    stat_dict = {result: 0 for result in [-2, -1, 0, 1, 2]}
    for stat in stats:
        stat_dict[int(stat["_id"])] = stat["count"]

    return json.dumps(stat_dict)

# app.run(ssl_context='adhoc')
