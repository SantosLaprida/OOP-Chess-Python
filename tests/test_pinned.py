
from chessboard.board import Board
from chessboard.boardutils import BoardUtils, NUM_SQUARES
from chessboard.notation import Notation
from chessboard.move import MoveFactory, NoneMove
from players.move_transition import MoveTransition
from chessboard.alliance import Alliance
from players import player, white_player, black_player


def main():

    fen = "r2q1rk1/pppb2pp/2n2P2/2bnp3/2B5/2PP1N2/PP3P1P/RNBQ1RK1 b KQkq - 0 10"

    board = BoardUtils.fen_to_board(fen)

    print(board)

    moves = board.get_all_legal_moves()

    for move in moves:
        print(move)

# python tests/test_pinned.py

if __name__ == '__main__':
    main()
