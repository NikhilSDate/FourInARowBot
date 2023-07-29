import copy
import logging
import sys
import threading
import time
import timeit
from typing import Tuple, Dict

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


# def actions(board: ConnectFourBoard, color: Color):
#     action_list = [i for i in range(board.shape[1]) if board.envelope(i) != board.shape[0]]
# #    return action_list
#     key = {}
#     for action in action_list:
#         result = copy.deepcopy(board)
#         result.do_move(action, color)
#         board_tuple = tuple(result.board.flatten())
#         key[action] = iterative_deepening_search.table.get(board_tuple, 0)
#     sorted_actions = sorted(action_list, key=lambda i: key[i])
#     if color == Color.FIRST:
#         return list(reversed(sorted_actions))
#     else:
#         return sorted_actions


# def terminal(board: ConnectFourBoard, loc) -> bool:
#     return board.full() or board.eval_game_state(loc, Color.FIRST) or board.eval_game_state(loc, Color.SECOND)


# def cutoff_test(board: ConnectFourBoard, loc, depth) -> bool:
#     return loc is not None and terminal(board, loc) or depth > alpha_beta_search.depth


# def iterative_deepening_search(board, color, max_dep=7):
#     iterative_deepening_search.table = {}
#     for depth in range(max_dep):
#         v, action = alpha_beta_search(board, color, depth)
#         print(depth, v, action)
#     return v, action
#
#
# # max_depth = 4
#
#
# def alpha_beta_search(board: ConnectFourBoard, color: Color, depth: int) -> Tuple[float, int]:
#     alpha_beta_search.depth = depth
#     if color == Color.FIRST:
#         v, action = max_value(board, -np.inf, np.inf, None, 0)
#     else:
#         v, action = min_value(board, -np.inf, np.inf, None, 0)
#     return v, action
#
#
# def max_value(board: ConnectFourBoard, alpha: float, beta: float, previous_loc, depth: int) -> Tuple[
#     float, int]:
#     if cutoff_test(board, previous_loc, depth):
#         return evaluation_function(board), -1
#     v = -np.inf
#     legal_actions = actions(board, Color.FIRST)
#     best_action = legal_actions[0]
#     for action in legal_actions:
#         result = copy.deepcopy(board)
#         result.do_move(action, Color.FIRST)
#         loc = (result.envelope(action) - 1, action)
#         min_val = min_value(result, alpha, beta, loc, depth + 1)[0]
#         iterative_deepening_search.table[tuple(result.board.flatten())] = min_val
#
#         if min_val > v:
#             best_action = action
#             v = min_val
#         if v >= beta:
#             return v, action
#         alpha = max(alpha, v)
#     return v, best_action
#
#
# def min_value(board: ConnectFourBoard, alpha: float, beta: float, previous_loc, depth: int) -> Tuple[
#     float, int]:
#     if cutoff_test(board, previous_loc, depth):
#         return evaluation_function(board), -1
#     v = np.inf
#     legal_actions = actions(board, Color.SECOND)
#     best_action = legal_actions[0]
#     for action in legal_actions:
#         result = copy.deepcopy(board)
#         result.do_move(action, Color.SECOND)
#         loc = (result.envelope(action) - 1, action)
#         max_val = max_value(result, alpha, beta, loc, depth + 1)[0]
#         iterative_deepening_search.table[tuple(result.board.flatten())] = max_val
#         if max_val < v:
#             best_action = action
#             v = max_val
#         if v <= alpha:
#             return v, action
#         beta = min(beta, v)
#     return v, best_action

class IterativeDeepeningWithTimeout(threading.Thread):
    def __init__(self, board: ConnectFourBoard, color: Color, max_dep: int, event: threading.Event):
        super().__init__()
        self.board = board
        self.color = color
        self.max_dep = max_dep
        self.event = event
        self.result = (-1, -1)
        self.result_lock = threading.Lock()
        self.table = {}
        self.current_depth = 0

    def run(self):
        self.iterative_deepening_search()

    def iterative_deepening_search(self):
        for depth in range(self.max_dep):
            v, action = self.alpha_beta_search(self.board, self.color, depth)
            self.result_lock.acquire()
            self.result = v, action
            self.result_lock.release()
            logging.getLogger(__name__).error(f'Completed depth {depth}')
#            print(depth, v, action)
        return v, action

    def alpha_beta_search(self, board: ConnectFourBoard, color: Color, depth: int) -> Tuple[float, int]:
        self.current_depth = depth
        if color == Color.FIRST:
            v, action = self.max_value(board, -np.inf, np.inf, None, 0)
        else:
            v, action = self.min_value(board, -np.inf, np.inf, None, 0)
        return v, action

    def cutoff_test(self, board: ConnectFourBoard, loc, depth) -> bool:
        if self.event.is_set():
            sys.exit()
        return loc is not None and self.terminal(board, loc) or depth > self.current_depth

    def max_value(self, board: ConnectFourBoard, alpha: float, beta: float, previous_loc, depth: int) -> Tuple[
        float, int]:
        if self.cutoff_test(board, previous_loc, depth):
            return evaluation_function(board), -1
        v = -np.inf
        legal_actions = self.actions(board, Color.FIRST)
        best_action = legal_actions[0]
        for action in legal_actions:
            result = copy.deepcopy(board)
            result.do_move(action, Color.FIRST)
            loc = (result.envelope(action) - 1, action)
            min_val = self.min_value(result, alpha, beta, loc, depth + 1)[0]
            self.table[tuple(result.board.flatten())] = min_val

            if min_val > v:
                best_action = action
                v = min_val
            if v >= beta:
                return v, action
            alpha = max(alpha, v)
        return v, best_action

    def min_value(self, board: ConnectFourBoard, alpha: float, beta: float, previous_loc, depth: int) -> Tuple[
        float, int]:
        if self.cutoff_test(board, previous_loc, depth):
            return evaluation_function(board), -1
        v = np.inf
        legal_actions = self.actions(board, Color.SECOND)
        best_action = legal_actions[0]
        for action in legal_actions:
            result = copy.deepcopy(board)
            result.do_move(action, Color.SECOND)
            loc = (result.envelope(action) - 1, action)
            max_val = self.max_value(result, alpha, beta, loc, depth + 1)[0]
            self.table[tuple(result.board.flatten())] = max_val
            if max_val < v:
                best_action = action
                v = max_val
            if v <= alpha:
                return v, action
            beta = min(beta, v)
        return v, best_action

    def actions(self, board: ConnectFourBoard, color: Color):
        action_list = [i for i in range(board.shape[1]) if board.envelope(i) != board.shape[0]]
        #    return action_list
        key = {}
        for action in action_list:
            result = copy.deepcopy(board)
            result.do_move(action, color)
            board_tuple = tuple(result.board.flatten())
            key[action] = self.table.get(board_tuple, 0)
        sorted_actions = sorted(action_list, key=lambda i: key[i])
        if color == Color.FIRST:
            return list(reversed(sorted_actions))
        else:
            return sorted_actions


    def terminal(self, board: ConnectFourBoard, loc) -> bool:
        return board.full() or board.eval_game_state(loc, Color.FIRST) or board.eval_game_state(loc, Color.SECOND)



if __name__ == '__main__':
    board = ConnectFourBoard()
    # board.do_move(4, Color.FIRST)
    # board.do_move(3, Color.SECOND)
    # board.do_move(5, Color.FIRST)
    # board.do_move(6, Color.SECOND)
    # board.do_move(4, Color.FIRST)
    # board.do_move(0, Color.SECOND)
    # board.do_move(3, Color.FIRST)
    e = threading.Event()
    t = IterativeDeepeningWithTimeout(board, Color.FIRST, 11, e)
    before = time.perf_counter()
    t.start()
    t.join(9)
    t.result_lock.acquire()
    e.set()
    print(t.result)
    t.result_lock.release()
    t.join()
    after = time.perf_counter()
    print(after-before)
