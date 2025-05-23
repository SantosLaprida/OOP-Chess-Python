from chessboard.square import Square
from chessboard.board import Board
from chessboard.boardutils import BoardUtils, NUM_SQUARES
from chessboard.notation import Notation
from chessboard.move import MoveFactory, NoneMove
from players.move_transition import MoveTransition
from chessboard.alliance import Alliance


def main():

    initial_board = Board.create_standard_board()
    print(initial_board)
    
    current_player = initial_board.get_current_player()
    print(f"Current player is {current_player.get_alliance()}")

    active_pieces = Board.calculate_active_pieces(initial_board.game_board, current_player.get_alliance())
    
    for piece in active_pieces:
        square = initial_board.get_square(piece.get_piece_position())
        square_id = square.get_square_id_by_coordinate(piece.get_piece_position())
        print(f"Piece {piece.get_piece_type()} at {square_id}")

    # python main3.py


if __name__ == '__main__':
    main()
    #ChessApp().run()
