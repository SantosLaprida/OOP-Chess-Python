from abc import ABC, abstractmethod
# from pieces.piece import Piece


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


class NormalMove(Move):
    """
    This class represents a normal move in the game, 
    a move where no piece is captured.
    """
    def __init__(self, board, movedPiece, destinationSquare) -> None:
        super().__init__(board, movedPiece, destinationSquare)


class CaptureMove(Move):
    """
    This class represents a capture move in the game, 
    a move where a piece is captured.
    """
    def __init__(self, board, movedPiece, destinationSquare, attackedPiece) -> None:
        super().__init__(board, movedPiece, destinationSquare)
        self.attackedPiece = attackedPiece