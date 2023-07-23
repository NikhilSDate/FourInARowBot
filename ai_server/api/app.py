import numpy as np
from flask import Flask, request, jsonify
from numpy import vectorize

from engine.colors import Color
from engine.connect_four_board import ConnectFourBoard
from engine.minimax import alpha_beta_search

app = Flask(__name__)


@app.route('/evaluate', methods=['GET'])
def evaluate():
    board = request.args.get('board')
    color = request.args.get('color')
    board = decode_board(board)
    color = decode_color(color)
    v, action = alpha_beta_search(board, color)
    return jsonify({"v": v, "action": action})


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
