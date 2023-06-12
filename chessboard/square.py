import sys
print(sys.path)
from pieces.piece import Piece
from abc import ABC, abstractmethod
from types import MappingProxyType
from .boardutils import NUM_SQUARES, NUM_SQUARES_ROW
from .alliance import Alliance

class Square(ABC):
    """
    An abstract base class that represents a square on a chess board. 
    It requires subclasses to implement 'isSquareOccupied' and 'get_piece' methods. 
    The class also provides a method to create all possible empty squares on the board.
    """

    def __init__(self, square_coordinate):
        self.square_coordinate = square_coordinate

    @classmethod        
    def create_all_possible_empty_squares(cls):
        emptySquareDict = {}

        for i in range(NUM_SQUARES):
            emptySquareDict[i] = EmptySquare(i)

        return MappingProxyType(emptySquareDict)
    
    @classmethod
    def create_square(cls, square_coordinate, piece):
        if piece is not None:
            if not isinstance(piece, Piece):
                raise TypeError("Piece should be an instance of the Piece class")
            return OccupiedSquare(square_coordinate, piece)
        else:
            return EMPTY_SQUARES_CACHE[square_coordinate]
    

    @abstractmethod
    def is_square_occupied(self):
        pass

    @abstractmethod
    def get_piece(self):
        pass

    
    

class EmptySquare(Square):
    """
    Represents an empty square on the chess board. Inherits from the abstract class 'Square'. 
    An empty square is not occupied and does not hold a piece.
    """

    def __init__(self, square_coordinate):
        super().__init__(square_coordinate)

    def is_square_occupied(self):
        return False
    
    def get_piece(self):
        return None
    
    def __str__(self) -> str:
        return "-"
    
class OccupiedSquare(Square):
    """
    Represents an occupied square on the chess board. Inherits from the abstract class 'Square'.
    An occupied square is occupied and holds a piece.
    """

    def __init__(self, square_coordinate, piece_on_square):
        super().__init__(square_coordinate)
        self.piece_on_square = piece_on_square

    def is_square_occupied(self):
        return True
    
    def get_piece(self):
        return self.piece_on_square
    
    def __str__(self) -> str:
        piece_name = str(self.piece_on_square)
        return piece_name.lower() if self.piece_on_square.get_piece_alliance() == Alliance.BLACK else piece_name.upper()
    
# Create EMPTY_SQUARES after EmptySquare is defined
EMPTY_SQUARES_CACHE = Square.create_all_possible_empty_squares()
