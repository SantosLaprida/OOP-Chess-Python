from chessboard.square import Square
from chessboard.board import Board
from chessboard.boardutils import BoardUtils, NUM_SQUARES
from chessboard.notation import Notation
from chessboard.move import MoveFactory
from players.move_transition import MoveTransition


def main():

    initial_board = Board.create_standard_board()
    print(initial_board)

    print("Printing legal moves for the pawn on h2")
    my_square = initial_board.get_square("h2")
    print("Printing if the piece before its move is first move variable")
    

    piece_on_h2 = my_square.get_piece()
    piece_on_h2_moves = piece_on_h2.calculate_legal_moves(initial_board)

    print(piece_on_h2.is_first_move)

    print(piece_on_h2_moves)

    print(my_square.get_square_coordinate())

    move = MoveFactory.create_move(initial_board, 
                                    my_square.get_square_coordinate(), 
                                    initial_board.get_square("h4").get_square_coordinate())
    move_transition = initial_board.get_current_player().make_move(move)

    if move_transition.status == MoveTransition.MoveStatus.DONE:
        after_move_board = move_transition.get_transition_board()

        print(after_move_board)

        print(after_move_board.get_current_player())
        print("Printing moves for the e7 pawn")

        piece_on_square = after_move_board.get_square("e7").get_piece()
        print(f'Piece {piece_on_square} on {piece_on_square.get_piece_position()}')
        print("E7 pawn if first move variable")
        print(piece_on_square.is_first_move)
        legal_moves = piece_on_square.calculate_legal_moves(after_move_board)
    

    # #Move implementation
    #         move = MoveFactory.create_move(self.board_panel.board,
    #                                        self.board_panel.source_square.get_square_coordinate(), 
    #                                        self.board_panel.destination_square.get_square_coordinate())
    #         move_transition = self.board_panel.board.get_current_player().make_move(move)
    #         if move_transition.status == MoveTransition.MoveStatus.DONE:
    #             self.board_panel.board = move_transition.get_transition_board()

    

if __name__ == '__main__':
    main()
    #ChessApp().run()
