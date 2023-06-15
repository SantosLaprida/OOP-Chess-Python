from abc import ABC, abstractmethod

from players.player import Player




class Move(ABC):

    """
    This class represents a move made in the game. It is abstract, 
    and specific types of moves should be represented by subclasses.
    """

    def __init__(self, board, movedPiece, destinationSquare) -> None:
        
        """
        :param board: The current state of the game board.
        :param movedPiece: The piece that is being moved.
        :param destinationSquare: The square the movedPiece is moving to.
        """

        self.board = board
        self.movedPiece = movedPiece
        self.destinationSquare = destinationSquare

    @abstractmethod
    def execute():
        pass

    def get_destination_coordinate(self):
        return self.destinationSquare
    
    def get_moved_piece(self):
        return self.movedPiece




class NormalMove(Move):
    """
    This class represents a normal move in the game, 
    a move where no piece is captured.
    """
    def __init__(self, board, movedPiece, destinationSquare) -> None:
        super().__init__(board, movedPiece, destinationSquare)

    def execute(self):

        from players.black_player import BlackPlayer
        from players.white_player import WhitePlayer

        from .board import Board
        '''
        When a move is executed, the current board is not mutated. Instead, a new board is created
        '''
        builder = Board.Builder()

        for piece in self.board.get_current_player().get_active_pieces():
            if not self.movedPiece == piece:
                builder.set_piece(piece)
        
        
        print("Set current player pieces")
        
        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            builder.set_piece(piece)

        print("Set opponent player pieces")

        builder.set_piece(self.movedPiece.move_piece(self)) 
        builder.set_move_maker(self.board.get_current_player().get_opponent().get_alliance())
        print("Set move maker")

        new_board = builder.build()
        if new_board is None:
            print("New board is None")
    
        return new_board






class CaptureMove(Move):
    """
    This class represents a capture move in the game, 
    a move where a piece is captured.
    """
    def __init__(self, board, movedPiece, destinationSquare, attackedPiece) -> None:
        super().__init__(board, movedPiece, destinationSquare)
        self.attackedPiece = attackedPiece

    def execute(self):
        pass