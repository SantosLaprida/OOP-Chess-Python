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
    BoardUtils.generate_fen(initial_board)
    print("***********************************")

    initial_square = Notation.notation_to_coordinate("e2")
    destination_square = Notation.notation_to_coordinate("e4")

    move = MoveFactory.create_move(initial_board, initial_square, destination_square)

    if isinstance(move, NoneMove):
        print("Move is NoneMove")

    else:
        move_transition = initial_board.get_current_player().make_move(move)

        if move_transition.status == MoveTransition.MoveStatus.DONE:
                        initial_board = move_transition.get_transition_board()
                        
                        print(initial_board)
                        print("***********************************")

                        print(f"Current player is {initial_board.get_current_player().get_alliance()}")


    

    print(BoardUtils.generate_fen(initial_board))


if __name__ == '__main__':
    main()
    #ChessApp().run()
