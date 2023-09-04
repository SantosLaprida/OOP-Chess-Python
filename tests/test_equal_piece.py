import pytest
from pieces.piece import Piece
from pieces.rook import Rook
from pieces.bishop import Bishop
from chessboard.alliance import Alliance

def test_piece_equality():
    piece1 = Rook(1, Alliance.BLACK)
    piece2 = Rook(1, Alliance.BLACK)

    assert piece1 == piece2

def test_piece_inequality():
    piece1 = Rook(1, Alliance.BLACK)
    piece2 = Bishop(2, Alliance.WHITE)

    assert piece1 != piece2

# def test_piece_equality_after_movement():
#     piece1 = Piece(1, Alliance.BLACK)
#     piece2 = Piece(1, Alliance.BLACK)
    
#     #piece1.move_piece()  
#     assert piece1 != piece2
