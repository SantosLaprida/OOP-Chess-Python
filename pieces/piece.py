from abc import ABC, abstractmethod
# from chessboard.move import Move
from chessboard.alliance import Alliance
from enum import Enum


class Piece(ABC):
    """
    An abstract base class representing a generic chess piece.
    """
    def __init__(self, piecePosition, pieceAlliance) -> None:
        self.piecePosition = piecePosition
        self.pieceAlliance = pieceAlliance
        self.first_move_made = False

    @abstractmethod
    def calculate_legal_moves(self, board) -> list:
        """
        Calculate the legal moves for the piece.

        :param board: The current state of the board.
        :return: A list of legal moves for the piece.
        """
        pass


    @abstractmethod
    def get_piece_type():
        """
        Get the piece type of the piece.

        :return: The piece type of the piece, one of the PieceType Enum values.
        """
        pass

    def get_piece_position(self):
        '''
        Returns the coordinate of the piece
        '''
        return self.piecePosition


    def get_piece_alliance(self) -> Alliance:
        """
    Get the alliance (color) of the piece.

    :return: The alliance (color) of the piece, either Alliance.WHITE or Alliance.BLACK.
    """
        return self.pieceAlliance

    def is_first_move(self) -> bool:
        """
        Returns true if its the piece's first move, false otherwise.
        """
        return self.first_move_made
    
    def __str__(self):
        piece_type = self.get_piece_type().value
        if self.get_piece_alliance() == Alliance.BLACK:
            return piece_type.lower()
        else:
            return piece_type.upper()
    
    class PieceType(Enum):
        PAWN = "P"
        KNIGHT = "N"
        BISHOP = "B"
        ROOK = "R"
        QUEEN = "Q"
        KING = "K"


      
