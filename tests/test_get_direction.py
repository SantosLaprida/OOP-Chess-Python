
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

    square = Notation.notation_to_coordinate('d5')
    knight_pos = board.get_square(square).get_piece().get_piece_position()
    king_pos = board.get_current_player().get_player_king().get_piece_position()


    direction = BoardUtils.get_direction(king_pos, knight_pos)
    print(direction)

    print(king_pos)
    print(knight_pos)

    direction = BoardUtils.get_direction(62, king_pos)
    print(direction)

# python tests/test_get_direction.py

if __name__ == '__main__':
    main()
