import configparser
import os
from datetime import datetime

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import json_util

from db.db import DBManager

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))
app = Flask(__name__)
app.config['MONGO_URI'] = config['DEV']['DB_URI']
app.config['DEBUG'] = True
mongo = PyMongo(app)


@app.route("/")
def home():
    return json_util.dumps(mongo.db.games.find({}))


# schema:
# collection games:
# "first_player_id": string (can be 'ai')
# "second_player_id": string (can be 'ai')
# "moves": string
# "result": integer (0 is draw by full board, 1 is draw by agreement, 2 is first player wins by position, 3 is first player wins by resignation, 4 is second player wins by position, 5 is second player wins by resignation"
# "guild_id": string
# "datetime": date and time object

# collection player
# "player_id": string
# "rating": (somehow store time series)

db_manager = DBManager(app)

@app.route("/add-game", methods=['POST'])
def add_game():
    new_game = request.get_json()
    _id = db_manager.add_game(new_game['first_player_id'], new_game['second_player_id'], new_game['moves'], new_game['result'], datetime.fromisoformat(new_game['datetime']))
    return json_util.dumps(db_manager.get_game(_id.inserted_id))

app.run(ssl_context='adhoc')
