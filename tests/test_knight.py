import pytest

from chessboard.board import Board
from chessboard.move import MoveFactory
from chessboard.alliance import Alliance

from players.move_transition import MoveTransition

from pieces.knight import Knight
from pieces.king import King



# Function to create a custom board
def custom_board_with_two_pawns_and_kings():
    # Initialize builder
    builder = Board.Builder()

    # Set the black pawn, king, white pawn, and king
    #builder.set_piece(Pawn(28, Alliance.BLACK))  # e5
    builder.set_piece(Knight(30, Alliance.BLACK))   # g5
    builder.set_piece(Knight(37, Alliance.WHITE))  # f4
    builder.set_piece(King(56, Alliance.WHITE))  # a1
    builder.set_piece(King(0, Alliance.BLACK))  # a8

    # Set the move maker. For this example, let's say white starts
    builder.set_move_maker(Alliance.WHITE)

    # Build the board
    return builder.build()

# Sample test case
def test_knight_move():

    board = custom_board_with_two_pawns_and_kings()

    print(board)

    legal_moves = board.get_square(37).get_piece().calculate_legal_moves(board)
    print(legal_moves)

    # #Move implementation
    move = MoveFactory.create_move(board, 37, 30)
    move_transition = board.get_current_player().make_move(move)
    if move_transition.status == MoveTransition.MoveStatus.DONE:
      transition_board = move_transition.get_transition_board()
      print(transition_board)

    assert ...

# ... Add other test cases