import numpy as np
from flask import Flask, request

from engine.connect_four_board import ConnectFourBoard

app = Flask(__name__)


@app.route('/evaluate')
def evaluate():
    board_txt = request.args.get('board')
    turn = request.args.get('turn')


def decode(board_txt: str, shape=(6, 7)) -> ConnectFourBoard:
    board = np.array([int(cell) for cell in board_txt])
    board = board.reshape(shape=shape)
    game_board = ConnectFourBoard()
    game_board._board = board
    game_board._envelope = np.argmax(np.append(board, np.zeros((1, board.shape[1])), axis=0).T == 0, axis=1)
    return game_board

