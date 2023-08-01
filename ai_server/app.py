import logging
import threading

import numpy as np
from flask import Flask, request, jsonify
import json
from numpy import vectorize

from engine.colors import Color
from engine.connect_four_board import ConnectFourBoard
from engine.minimax import IterativeDeepeningWithTimeout

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

with open('config.json', 'r') as f:
    content = f.read()
    config = json.loads(content)
    app.config['engine'] = config['engine']


@app.route('/evaluate', methods=['GET'])
def evaluate():
    board = request.args.get('board')
    color = request.args.get('color')
    board = decode_board(board)
    color = decode_color(color)
    time_limit = app.config['engine']['TIME_LIMIT']
    max_depth = app.config['engine']['MAX_DEPTH']
    v, action = evaluate_helper(board, color, time_limit, max_depth)
    return jsonify({"v": v, "action": action})


def evaluate_helper(board, color, time_limit, max_depth):
    e = threading.Event()
    t = IterativeDeepeningWithTimeout(board, color, max_depth, e)
    t.start()
    t.join(time_limit)
    t.result_lock.acquire()
    v, action = t.result
    e.set()
    t.result_lock.release()
    t.join()
    return v, action


def decode_board(board: str, shape=(6, 7)) -> ConnectFourBoard:
    @vectorize
    def int_to_color(x: int) -> Color:
        assert x == 0 or x == 1 or x == 2
        if x == 0:
            return Color.EMPTY
        elif x == 1:
            return Color.FIRST
        elif x == 2:
            return Color.SECOND
    board = np.array([int(cell) for cell in board])
    board = board.reshape(shape)
    connect_four_board = ConnectFourBoard()
    connect_four_board._board = int_to_color(board)
    connect_four_board._envelope = np.argmax(np.append(board, np.zeros((1, board.shape[1])), axis=0).T == 0, axis=1)
    return connect_four_board


def decode_color(color: str) -> Color:
    assert color == '1' or color == '2'
    return Color.FIRST if color == '1' else Color.SECOND



