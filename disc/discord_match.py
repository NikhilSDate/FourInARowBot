from typing import Tuple

from discord.abc import Messageable

from disc.discord_game import DiscordGame
from disc.utils import ping
from game.statuses import Status, StatusType, StatusError


class DiscordMatch:

    def __init__(self, num_games: int = 3, dims: Tuple[int, int] = (6, 7), winning_length: int = 4, channel=None, first_player_id: str = None, second_player_id: str = None):
        self.num_games = num_games
        self.dims = dims
        self.winning_length = winning_length
        self.channel = channel
        self.first_player_id = first_player_id
        self.second_player_id = second_player_id
        self._games = []
        for i in range(num_games):
            if i % 2 == 0:
                self._games.append(DiscordGame(dims=dims, winning_length=winning_length, channel=channel,
                                               first_player_id=first_player_id, second_player_id=second_player_id))
            else:
                self._games.append(DiscordGame(dims=dims, winning_length=winning_length, channel=channel,
                                               first_player_id=second_player_id, second_player_id=first_player_id))
        self.game_index = 0
        self.status: Status = Status.OK

    @property
    def current_game(self):
        return self._games[self.game_index]

    @property
    def previous_game(self):
        return self._games[self.game_index - 1]

    def calculate_net_score_and_string_score(self) -> Tuple[int, str]:
        first_score = 0
        second_score = 0
        for i in range(self.game_index):
            current_game = self._games[i]
            if current_game.status in StatusType.FIRST_WINS_GAME:
                increments = (1, 0)
            elif current_game.status in StatusType.SECOND_WINS_GAME:
                second_score = (0, 1)
            elif current_game.status in StatusType.DRAW_GAME:
                increments = (0.5, 0.5)
            else:
                raise StatusError('Game not finished')

            if i % 2 == 0:
                first_score += increments[0]
                second_score += increments[1]
            else:
                first_score += increments[1]
                second_score += increments[0]

        return first_score - second_score, f'{first_score: .1} - {second_score: .1}'

    def do_move(self, column: int, player_id: str) -> Status:
        status = self.current_game.do_move(column, self.current_game.players[player_id])
        if status in StatusType.GAME_OVER:
            self.game_index += 1
            if self.game_index == self.num_games:
                if self.calculate_net_score_and_string_score()[0] > 0.25:
                    return Status.FIRST_WINS_MATCH
                elif self.calculate_net_score_and_string_score()[0] < -0.25:
                    return Status.SECOND_WINS_MATCH
                else:
                    return Status.DRAW_MATCH
        return status

    def result_to_message(self) -> str:
        ping_first = ping(self.first_player_id)
        ping_second = ping(self.second_player_id)
        result_str = self.calculate_net_score_and_string_score()
        return f'{ping_first} {result_str} {ping_second}'




