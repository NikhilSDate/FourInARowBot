from game.colors import Color
from game.connect_four_board import ConnectFourBoard


def test_eval_game_state():
    # lr diag
    board = ConnectFourBoard(dims=(6, 7))
    board.do_moves([(0, Color.FIRST),
                    (1, Color.SECOND),
                    (1, Color.FIRST),
                    (2, Color.SECOND),
                    (2, Color.FIRST),
                    (3, Color.SECOND),
                    (3, Color.FIRST),
                    (0, Color.SECOND),
                    (2, Color.FIRST),
                    (3, Color.SECOND),
                    (3, Color.FIRST)])
    assert board.eval_game_state((board.envelope(3) -1, 3), Color.FIRST, winning_length=4)

    # rl diag
    board = ConnectFourBoard(dims=(6, 7))
    board.do_moves([(0, Color.FIRST),
                    (0, Color.SECOND),
                    (0, Color.FIRST),
                    (0, Color.SECOND),
                    (2, Color.FIRST),
                    (2, Color.SECOND),
                    (1, Color.FIRST),
                    (3, Color.SECOND),
                    (1, Color.FIRST),
                    (1, Color.SECOND)])
    assert board.eval_game_state((board.envelope(1) - 1, 1), Color.SECOND, winning_length=4)

    # horizontal

    board = ConnectFourBoard(dims=(6, 7))
    board.do_moves([(0, Color.FIRST),
                    (0, Color.SECOND),
                    (1, Color.FIRST),
                    (0, Color.SECOND),
                    (2, Color.FIRST),
                    (0, Color.SECOND),
                    (3, Color.FIRST)
                    ])
    assert board.eval_game_state((board.envelope(3) - 1, 3), Color.FIRST, winning_length=4)

    board = ConnectFourBoard(dims=(6, 7))
    # vertical
    board.do_moves([(0, Color.FIRST),
                    (1, Color.SECOND),
                    (0, Color.FIRST),
                    (1, Color.SECOND),
                    (0, Color.FIRST),
                    (1, Color.SECOND),
                    (0, Color.FIRST)
                    ])
    assert board.eval_game_state((board.envelope(0) - 1, 0), Color.FIRST, winning_length=4)



