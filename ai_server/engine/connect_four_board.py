from typing import Tuple, Sequence
from numpy.typing import NDArray
from engine.colors import Color
import numpy as np
from engine.statuses import Status


class ConnectFourBoard:
    def __init__(self, dims: tuple = (6, 7)):
        # TODO: try to optimize by making values in board array ints
        self._board = np.full(shape=dims, fill_value=Color.EMPTY, dtype=object)
        self._envelope = np.zeros(shape=(dims[1],), dtype=int)

    @property
    def shape(self) -> Tuple[int, int]:
        return self._board.shape

    def envelope(self, column):
        if not column >= 0 and column < self.shape[1]:
            raise ValueError('column must be a valid column index')
        return self._envelope[column]

    def do_move(self, column: int, color: Color) -> Status:
        if not column >= 0 and column < self.shape[1]:
            raise ValueError('column must be a valid column index')
        if self._envelope[column] == self.shape[0]:
            return Status.COLUMN_FULL
        self._board[self._envelope[column]][column] = color
        self._envelope[column] += 1
        return Status.OK

    def do_moves(self, moves: Sequence[Tuple[int, Color]]) -> Tuple[int, Status]:
        for i, move in enumerate(moves):
            status = self.do_move(*move)
            if status != Status.OK:
                return i, status
        return len(moves), Status.OK

    def full(self) -> bool:
        # TODO: can be optimized
        return np.min(self._envelope) == self.shape[0]

    def eval_game_state(self, loc: Tuple[int, int], color: Color, winning_length: int = 4) -> bool:
        '''
        Returns true if color wins and false otherwise
        :param loc:
        :param color:
        :param winning_length:
        :return:
        '''

        def eval_max_run_length(arr: NDArray, target) -> int:
            if len(arr.shape) != 1:
                raise ValueError('arr must be a one-dimensional array')

            max_length = 0
            current_length = 0
            in_run = False
            for elem in arr:
                if in_run:
                    if elem == target:
                        current_length += 1
                    else:
                        in_run = False
                        max_length = max(max_length, current_length)
                        current_length = 0

                else:
                    if elem == target:
                        in_run = True
                        current_length = 1
            if in_run:
                max_length = max(current_length, max_length)
            return max_length

        horizontal = self._board[loc[0],
                     max(0, loc[1] - (winning_length - 1)): min(loc[1] + winning_length, self.shape[1])]
        max_run = eval_max_run_length(horizontal, color)
        if max_run >= winning_length:
            return True

        vertical = self._board[max(0, loc[0] - (winning_length - 1)): min(loc[0] + winning_length, self.shape[0]),
                   loc[1]]

        max_run = eval_max_run_length(vertical, color)
        if max_run >= winning_length:
            return True

        # left to right diagonal
        offset = loc[1] - loc[0]

        left_lim = max(0, -offset, loc[0] - (winning_length - 1))
        right_lim = min(self.shape[0], self.shape[1] - offset, loc[0] + winning_length)

        lr_diag = np.array([self._board[i, i + offset] for i in range(left_lim, right_lim)], dtype=Color)

        max_run = eval_max_run_length(lr_diag, color)
        if max_run >= winning_length:
            return True

        # right to left diagonal
        isum = loc[0] + loc[1]
        left_lim = max(0, isum - (self.shape[1] - 1), loc[0] - (winning_length - 1))
        right_lim = min(self.shape[0], isum + 1, loc[0] + winning_length)
        rl_diag = np.array([self._board[i, isum - i] for i in range(left_lim, right_lim)], dtype=Color)
        max_run = eval_max_run_length(rl_diag, color)
        if max_run >= winning_length:
            return True

        return False

    def __getitem__(self, index):
        return self._board[index]

    # ai methods

    def actions(self) -> Sequence[int]:
        return [i for i in range(self.shape[1]) if self._envelope[i] < self.shape[0]]

    @property
    def board(self):
        return self._board

