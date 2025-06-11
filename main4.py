import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from chessengine.chessboard.square import Square
from chessengine.chessboard.board import Board
from chessengine.chessboard.boardutils import BoardUtils, NUM_SQUARES
from chessengine.chessboard.notation import Notation
from chessengine.chessboard.move import MoveFactory, NoneMove
from chessengine.players.move_transition import MoveTransition
from chessengine.chessboard.alliance import Alliance


def main():
    fen = "r1bq1rk1/1ppp1ppp/p1n2n2/2b1p3/2B1P3/P1N2N2/1PPP1PPP/R1BQ1RK1 w - - 0 7"

    board = BoardUtils.fen_to_board(fen)

    print(board)

    rook = board.get_square("f1").get_piece()

    moves = rook.calculate_legal_moves(board)

    print(f"Legal moves for {rook.get_piece_type()} at f1:")
    print(moves[0])

    move_transition = board.get_current_player().make_move(moves[0])

    if move_transition.status == MoveTransition.MoveStatus.DONE:
        new_board = move_transition.get_transition_board()
    #                     self.board_panel.assign_all_square_piece_icons()
        print("Move done")
    #                     fen = BoardUtils.generate_fen(self.board_panel.board)
    #                     print(fen)

        print(new_board)
    #                     current_player = self.board_panel.board.get_current_player()

    #                     print(f"Current player is: {current_player.get_alliance()}")

    #                     print(f"Is {current_player.get_alliance()} in check?")
    #                     print(current_player.is_in_check)




if __name__ == '__main__':
    main()


# python main4.py