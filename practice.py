from chessboard.board import Board
from chessboard.alliance import Alliance

board = Board.create_standard_board()

board_data = {}

for piece in board.get_white_pieces() + board.get_black_pieces():
    piece_type = piece.get_piece_type().value
    alliance = 'WHITE' if piece.get_piece_alliance() == Alliance.WHITE else 'BLACK'
    board_data[piece.get_piece_position()] = [piece_type, alliance]

print(board_data)