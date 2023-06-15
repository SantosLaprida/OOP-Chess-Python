import pytest
from chessboard.move import NormalMove
from chessboard.board import Board
from pieces.piece import Piece
from pieces.rook import Rook
from chessboard.alliance import Alliance

def test_normal_move_execute():
    # Setup
    board = Board.create_standard_board()
    moved_piece = board.get_square(1).get_piece()
    destination_square = board.get_square(2)
    move = NormalMove(board, moved_piece, destination_square)

    # Create a normal move
    moved_piece = board.get_square(1).get_piece()
    destination_square = board.get_square(2)
    move = NormalMove(board, moved_piece, destination_square)

    # Execute the move
    new_board = move.execute()

    # Assert that the moved piece is no longer in its original position
    assert not new_board.get_square(1).is_square_occupied()

    # Assert that the moved piece is in its new position
    assert new_board.get_square(2).get_piece() == moved_piece

    # Assert that the next move maker is BLACK
    assert new_board.get_current_player().get_alliance() == Alliance.BLACK


