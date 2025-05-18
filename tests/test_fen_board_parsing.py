from chessboard.board import Board, BoardUtils
from chessboard.move import MoveFactory
from chessboard.alliance import Alliance

fen = "r4rk1/1p1b2pp/4p3/pPq2pN1/2P5/4P2P/P4QB1/5RK1 w - - 0 24"

board = BoardUtils.fen_to_board(fen)

print(board)

print(board.get_castling_rights())


board = Board.create_standard_board()

print(board.get_castling_rights())


# python tests/test_fen_board_parsing.py