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

    print(f"Current player is {initial_board.get_current_player().get_alliance()}")

    print("***********************************")
    initial_fen = BoardUtils.generate_fen(initial_board)
    print(f"\nInitial FEN: {initial_fen}")
    print("***********************************")


    print("Testing fen_to_board with the initial FEN...")
    reconstructed_board = BoardUtils.fen_to_board(initial_fen)
    print(reconstructed_board)
    print(f"Current player is {initial_board.get_current_player().get_alliance()}")

    initial_square = Notation.notation_to_coordinate("e2")
    destination_square = Notation.notation_to_coordinate("e4")

    move = MoveFactory.create_move(initial_board, initial_square, destination_square)

    if isinstance(move, NoneMove):
        print("Move is NoneMove")

    else:
        move_transition = initial_board.get_current_player().make_move(move)

        if move_transition.status == MoveTransition.MoveStatus.DONE:
                        initial_board = move_transition.get_transition_board()
                        
                        
                        print(f"Board after move with")
                        print(initial_board)
                        print("***********************************")
                        board_fen = BoardUtils.generate_fen(initial_board)
                        print(f"Board after move with fen notation")
                        print(board_fen)
                        print(f"Current player is {initial_board.get_current_player().get_alliance()}")
                        initial_board_fen = BoardUtils.fen_to_board(board_fen)
                        print("*******************************")
                        print("*******************************")
                        print(initial_board_fen)
                        piece = initial_board.get_square(destination_square).get_piece()
                        print(piece)
                        print(piece.is_first_move)

                        piece = initial_board.get_square(10).get_piece()
                        print(piece)
                        print(piece.is_first_move)


    

    

    print(BoardUtils.generate_fen(initial_board))


if __name__ == '__main__':
    main()
    #ChessApp().run()
