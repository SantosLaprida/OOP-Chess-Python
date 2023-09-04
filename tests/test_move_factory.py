from chessboard.board import Board
from chessboard.move import MoveFactory
from players.player import Player
from players.move_transition import MoveTransition
from pieces.piece import Piece

def test_move_factory_and_transition():
    # Create a board
    board = Board.create_standard_board()

    # Get the initial current_player
    initial_current_player = board.current_player

    # Print the initial board state
    print("Initial board state:")
    print(board)

    # Assume we want to move the pawn from (6, 4) to (5, 4) for white's first move
    current_coordinate = 52  # This corresponds to the tile coordinate (6, 4)
    destination_coordinate = 44  # This corresponds to the tile coordinate (5, 4)

    # Use the MoveFactory to create a move
    move = MoveFactory.create_move(board, current_coordinate, destination_coordinate)
    print("\nMove:")
    print(move)
    print("Move details:")
    print(f"Current Coordinate: {move.get_current_coordinate()}")
    print(f"Destination Coordinate: {move.get_destination_coordinate()}")
    print(f"Moved Piece: {move.get_moved_piece()}")
    print(f"Moved Piece coordinate: {move.get_moved_piece().get_piece_position()}")
    print(type(move))

    assert move is not None, "Move should not be None"

    # Check the current and destination coordinates of the move
    assert move.get_current_coordinate() == current_coordinate, "Current coordinate does not match"
    assert move.get_destination_coordinate() == destination_coordinate, "Destination coordinate does not match"

    # Execute the move and get the transition
    transition = initial_current_player.make_move(move)

    # Ensure the transition was done
    assert transition.move_status == MoveTransition.MoveStatus.DONE, "Move was not done"

    # Update the board to the state after the move
    board = transition.transition_board

    

    # The current player should have changed
    assert board.current_player != initial_current_player, "Current player did not change"

    # Print the board state after the move
    print("\nBoard state after the move:")
    print(board)

if __name__ == "__main__":
    test_move_factory_and_transition()

