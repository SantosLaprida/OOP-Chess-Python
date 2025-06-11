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
    fen = "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/2N2N2/PPPP1PPP/R1BQK2R w - - 0 11"

    board = BoardUtils.fen_to_board(fen)

    print(board)

    current_player = board.get_current_player()

    
    rook = board.get_square("h1").get_piece()

    moves = rook.calculate_legal_moves(board)

    move = moves[1]

    move_transition = board.get_current_player().make_move(move)

    if move_transition.status == MoveTransition.MoveStatus.DONE:
                        new_board = move_transition.get_transition_board()
                        print("Move done")
                        new_fen = BoardUtils.generate_fen(new_board)
                        print(fen)

                        print(new_board)






    




if __name__ == '__main__':
    main()


# python main4.py