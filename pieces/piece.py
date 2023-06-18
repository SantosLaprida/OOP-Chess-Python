from abc import ABC, abstractmethod
# from chessboard.move import Move

from enum import Enum
#from chessboard.move import Move


class Piece(ABC):
    """
    An abstract base class representing a generic chess piece.
    """
    def __init__(self, piece_position, piece_alliance) -> None:
        self.piece_position = piece_position
        self.piece_alliance = piece_alliance
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

    @abstractmethod
    def move_piece(move):
        pass

    def is_king(self):
        return self.get_piece_type() == Piece.PieceType.KING
    
    def is_rook(self):
        return self.get_piece_type() == Piece.PieceType.ROOK
    
    
    def get_piece_position(self):
        '''
        Returns the coordinate of the piece
        '''
        return self.piece_position

    def __eq__(self, other):
        print(f'Self: {self.piece_type}, {self.piece_alliance}, {self.piece_position}')
        print(f'Other: {other.piece_type}, {other.piece_alliance}, {other.piece_position}')

        if self.piece_type != other.piece_type:
            return False
        if self.piece_alliance != other.piece_alliance:
            return False
        if self.piece_position != other.piece_position:
            return False
        return True

        
    def __hash__(self):
        
        return hash((self.piece_position, self.piece_alliance, self.get_piece_type()))


    def get_piece_alliance(self):
        from chessboard.alliance import Alliance
        """
        Get the alliance (color) of the piece.

        :return: The alliance (color) of the piece, either Alliance.WHITE or Alliance.BLACK.
        """
        return self.piece_alliance

    def is_first_move(self) -> bool:
        """
        Returns true if its the piece's first move, false otherwise.
        """
        return self.first_move_made
    
    def __str__(self):
        from chessboard.alliance import Alliance
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

       
      
