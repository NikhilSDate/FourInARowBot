import copy
from typing import Tuple

import numpy as np
from numpy._typing import NDArray

from engine.colors import Color
from engine.connect_four_board import ConnectFourBoard


def run_evaluation(run_length, num_open):
    if run_length >= 4:
        return np.inf

    if num_open == 0:
        return 0
    if num_open == 1 or num_open == 2:
        if run_length == 1:
            return 1
        elif run_length == 2:
            return 4
        elif run_length == 3:
            return 16
    elif num_open == 2:
        if run_length == 1:
            return 2
        elif run_length == 2:
            return 8
        elif run_length == 3:
            return 32


def evaluation_function(board: ConnectFourBoard):
    def array_evaluation(arr: NDArray[Color], target) -> float:
        if len(arr.shape) != 1:
            raise ValueError('arr must be a one-dimensional array')

        current_length = 0
        evaluation = 0
        in_run = False
        run_start = -1
        for i, elem in enumerate(arr):
            if in_run:
                if elem == target:
                    current_length += 1
                else:
                    left_open = run_start != 0 and arr[run_start - 1] == Color.EMPTY
                    right_open = i != arr.shape[0] and arr[i] == Color.EMPTY
                    num_open = int(left_open) + int(right_open)
                    evaluation += run_evaluation(current_length, num_open)
                    in_run = False
                    run_start = -1
                    current_length = 0


            else:
                if elem == target:
                    in_run = True
                    run_start = i
                    current_length = 1

        if in_run:
            left_open = run_start != 0 and arr[run_start - 1] == Color.EMPTY
            num_open = int(left_open)
            evaluation += run_evaluation(current_length, num_open)
        return evaluation

    def color_evaluation(color: Color):
        evaluation = 0
        for horizontal in board.board:
            evaluation += array_evaluation(horizontal, color)
        for vertical in np.transpose(board.board):
            evaluation += array_evaluation(vertical, color)
        for i in range(-(board.shape[0] - 1), board.shape[1]):
            lr_diag = np.diagonal(board.board, offset=i)
            evaluation += array_evaluation(lr_diag, color)
        flipped_board = np.fliplr(board.board)
        for i in range(-(flipped_board.shape[0] - 1), flipped_board.shape[1]):
            rl_diag = np.diagonal(flipped_board, offset=i)
            evaluation += array_evaluation(rl_diag, color)
        return evaluation

    return color_evaluation(Color.FIRST) - color_evaluation(Color.SECOND)


def actions(board: ConnectFourBoard):
    action_list = [i for i in range(board.shape[1]) if board.envelope(i) != board.shape[0]]
    return action_list
    # key = {}
    # for action in action_list:
    #     result = copy.deepcopy(board)
    #     result.do_move(action, color)
    #     key[action] = evaluation_function(result)
    # return sorted(action_list, key=lambda i: key[i])


def terminal(board: ConnectFourBoard, loc) -> bool:
    return board.full() or board.eval_game_state(loc, Color.FIRST) or board.eval_game_state(loc, Color.SECOND)


def cutoff_test(board: ConnectFourBoard, loc, depth) -> bool:
    return loc is not None and terminal(board, loc) or depth > 5


def alpha_beta_search(board: ConnectFourBoard, color: Color) -> Tuple[float, int]:
    if color == Color.FIRST:
        v, action = max_value(board, -np.inf, np.inf, None, 0)
    else:
        v, action = min_value(board, -np.inf, np.inf, None, 0)
    return v, action


def max_value(board: ConnectFourBoard, alpha: float, beta: float, previous_loc, depth: int) -> Tuple[float, int]:
    if cutoff_test(board, previous_loc, depth):
        return evaluation_function(board), -1
    v = -np.inf
    legal_actions = actions(board)
    best_action = legal_actions[0]
    for action in legal_actions:
        result = copy.deepcopy(board)
        result.do_move(action, Color.FIRST)
        loc = (result.envelope(action) - 1, action)
        min_val = min_value(result, alpha, beta, loc, depth + 1)[0]

        if min_val > v:
            best_action = action
            v = min_val
        if v >= beta:
            return v, action
        alpha = max(alpha, v)
    return v, best_action


def min_value(board: ConnectFourBoard, alpha: float, beta: float, previous_loc, depth: int) -> Tuple[float, int]:
    if cutoff_test(board, previous_loc, depth):
        return evaluation_function(board), -1
    v = np.inf
    legal_actions = actions(board)
    best_action = legal_actions[0]
    for action in legal_actions:
        result = copy.deepcopy(board)
        result.do_move(action, Color.SECOND)
        loc = (result.envelope(action) - 1, action)
        max_val = max_value(result, alpha, beta, loc, depth + 1)[0]
        if max_val < v:
            best_action = action
            v = max_val
        if v <= alpha:
            return v, action
        beta = min(beta, v)
    return v, best_action


