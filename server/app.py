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


db_manager = DBManager(app)


@app.route("/add-game", methods=['POST'])
def add_game():
    new_game = request.get_json()
    _id = db_manager.add_game(new_game['first_player_id'], new_game['second_player_id'], new_game['moves'],
                              new_game['result'], datetime.fromisoformat(new_game['datetime']))
    return json_util.dumps(db_manager.get_game(_id.inserted_id))


@app.route("/stats/<player_id: string>", methods=['GET'])
def get_stats(player_id):
    other_player_id = request.args.get('other_player_id')
    guild_id = request.args.get('guild_id')
    from_date = datetime.fromisoformat(request.args.get('from_date'))
    to_date = datetime.fromisoformat(request.args.get('to_date'))
    return json_util.dumps(db_manager.get_stats(player_id, other_player_id, guild_id, from_date, to_date))


app.run(ssl_context='adhoc')
