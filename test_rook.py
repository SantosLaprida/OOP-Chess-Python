# test_rook.py

import pytest
from chessboard.board import Board
from pieces.rook import Rook
from chessboard.alliance import Alliance
from chessboard.move import Move
from chessboard.move import CaptureMove
from chessboard.move import NormalMove

def test_rook_initial_position():
    rook = Rook(0, Alliance.WHITE)
    assert rook.piece_position == 0

def test_rook_piece_type():
    rook = Rook(0, Alliance.WHITE)
    assert rook.piece_type == rook.PieceType.ROOK

def test_rook_calculate_legal_moves_empty_board():
    from pieces.king import King

    rook = Rook(40, Alliance.WHITE)  # Placing the rook roughly in the middle of an empty board
    white_king = King(4, Alliance.WHITE)  # Placing a king for the white player
    black_king = King(60, Alliance.BLACK)  # Placing a king for the black player

    builder = Board.Builder()
    builder.set_piece(rook).set_piece(white_king).set_piece(black_king)
    board = builder.build()

    legal_moves = rook.calculate_legal_moves(board)
    # Rook in the center of an empty 8x8 board can move 14 squares
    assert len(legal_moves) == 14  

# def test_rook_cannot_move_past_friendly_piece():
#     rook = Rook(40, Alliance.WHITE)
#     friendly_piece = Rook(41, Alliance.WHITE)
#     builder = Board.Builder()
#     builder.set_piece(rook).set_piece(friendly_piece)
#     board = builder.build()
#     legal_moves = rook.calculate_legal_moves(board)
#     # Rook can't move to the square occupied by a friendly piece
#     assert all(move.destinationSquare != friendly_piece.piecePosition for move in legal_moves)

# def test_rook_can_capture_enemy_piece():
#     rook = Rook(40, Alliance.WHITE)
#     enemy_piece = Rook(41, Alliance.BLACK)
#     builder = Board.Builder()
#     builder.set_piece(rook).set_piece(enemy_piece)
#     board = builder.build()
#     legal_moves = rook.calculate_legal_moves(board)
#     # Rook can move to the square occupied by an enemy piece
#     assert any(isinstance(move, CaptureMove) and move.get_destination_coordinate() == enemy_piece.piecePosition for move in legal_moves)
