import pytest

from chessboard.board import Board
from chessboard.move import MoveFactory
from chessboard.alliance import Alliance

from players.move_transition import MoveTransition

from pieces.pawn import Pawn
from pieces.king import King



# Function to create a custom board
def custom_board_with_two_pawns_and_kings():
    # Initialize builder
    builder = Board.Builder()

    # Set the black pawn, king, white pawn, and king
    #builder.set_piece(Pawn(28, Alliance.BLACK))  # e5
    builder.set_piece(Pawn(30, Alliance.BLACK))   # g5
    builder.set_piece(Pawn(37, Alliance.WHITE))  # f4
    builder.set_piece(King(56, Alliance.WHITE))  # a1
    builder.set_piece(King(0, Alliance.BLACK))  # a8

    # Set the move maker. For this example, let's say white starts
    builder.set_move_maker(Alliance.WHITE)

    # Build the board
    return builder.build()

# Function to create a custom board
def custom_board_symmetrical():
    # Initialize builder
    builder = Board.Builder()

    # Set the black pawn, king, white pawn, and king
    
    builder.set_piece(Pawn(12, Alliance.BLACK))   # e7
    builder.set_piece(Pawn(52, Alliance.WHITE))  # e2
    builder.set_piece(King(56, Alliance.WHITE))  # a1
    builder.set_piece(King(0, Alliance.BLACK))  # a8

    # Set the move maker. For this example, let's say white starts
    builder.set_move_maker(Alliance.WHITE)

    # Build the board
    return builder.build()

# Sample test case
def test_pawn_move():
    board = custom_board_with_two_pawns_and_kings()

    print('****************************************')
    print("FIRST TEST")
    print('****************************************')
    print(board)

    legal_moves = board.get_square(37).get_piece().calculate_legal_moves(board)
    print(legal_moves)

    # #Move implementation
    move = MoveFactory.create_move(board, 37, 30)
    move_transition = board.get_current_player().make_move(move)
    if move_transition.status == MoveTransition.MoveStatus.DONE:
      transition_board = move_transition.get_transition_board()
      print(transition_board)

    

    print('****************************************')
    print("SECOND TEST")
    print('****************************************')

    board2 = custom_board_symmetrical()
    print(board2)
    legal_moves = board2.get_square(52).get_piece().calculate_legal_moves(board2)
    print(legal_moves)
    

    assert ...

# ... Add other test cases
