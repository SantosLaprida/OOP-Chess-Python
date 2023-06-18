import pytest
from chessboard.move import NormalMove
from chessboard.board import Board
from pieces.piece import Piece
from pieces.rook import Rook
from chessboard.alliance import Alliance

def test_normal_move_execute():
    # Setup
    board = Board.create_standard_board()
    moved_piece = board.get_square(62).get_piece()
    destination_square = 47
    move = NormalMove(board, moved_piece, destination_square)

    # Execute the move
    new_board = move.execute()

    # Assert that the moved piece is no longer in its original position
    assert not new_board.get_square(62).is_square_occupied()

    # Assert that the moved piece is in its new position

    piece_after_move = new_board.get_square(47).get_piece()
    assert piece_after_move.piece_type == moved_piece.piece_type
    assert piece_after_move.piece_alliance == moved_piece.piece_alliance
    assert piece_after_move.piece_position == destination_square

    # Assert that the next move maker is BLACK
    assert new_board.get_current_player().get_alliance() == Alliance.WHITE


