import warnings

from disc.utils import ping
from game.colors import Color
from game.statuses import Status, StatusError


class DiscordMixin:
    def get_player_color(self, player_id: str) -> Color:
        return self.players[player_id]

    def handle_resign(self, player_id: str):
        super().handle_resign(self.players[player_id])

    def to_message(self) -> str:
        # try to add column numbers
        message = ''
        if self.board.shape[1] > 10:
            warnings.warn('Number of columns is more than 10, so column numbers will not be printed')
        else:
            base = ord('0')
            numbers = {i: chr(base + i) + '\uFE0F' + '\u20e3' for i in range(10)}
            numbers[10] = '\U0001F51F'
            for i in range(self.board.shape[1]):
                message += numbers[i + 1]
            message += '\n'

        emojis = {Color.FIRST: "\U0001F534", Color.SECOND: "\U0001F535", Color.EMPTY: "\u26AA"}
        # flip board upside down
        for i in range(self.board.shape[0] - 1, -1, -1):
            for j in range(self.board.shape[1]):
                message += emojis[self.board[i, j]]
            message += '\n'
        return message

    def color_assignment_to_message(self) -> str:
        message = ''
        for key, value in self.players.items():
            message += f'{ping(key)}: {self.colors[value]}\n'
        return message

    def result_to_message(self) -> str:
        if self.status not in StatusType.GAME_OVER:
            raise StatusError('Game must be over to convert result to message.')
        if self.status == Status.FIRST_WINS_BY_POSITION:
            return f'Game over! {self.colors[Color.FIRST]} wins!'
        elif self.status == Status.SECOND_WINS_BY_POSITION:
            return f'Game over! {self.colors[Color.SECOND]} wins!'
        elif self.status == Status.FIRST_WINS_BY_RESIGNATION:
            return f'Game over! {self.colors[Color.FIRST]} wins by resignation!'
        elif self.status == Status.SECOND_WINS_BY_RESIGNATION:
            return f'Game over! {self.colors[Color.SECOND]} wins by resignation!'
        elif self.status == Status.DRAW_BY_STALEMATE:
            return f'Game over! Draw!'
        raise NotImplementedError()