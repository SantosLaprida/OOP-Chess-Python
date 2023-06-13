from .piece import Piece
from chessboard.boardutils import BoardUtils
# from chessboard.board import Board
from chessboard.move import Move, NormalMove, CaptureMove
from chessboard.square import Square, EmptySquare, OccupiedSquare

class Rook(Piece):

    CANDIDATE_MOVE_COORDINATES = [-1, -8, 8, 1]

    def __init__(self, piecePosition, pieceAlliance):
        super().__init__(piecePosition, pieceAlliance)
        self.piece_type = Piece.PieceType.ROOK

    def calculate_legal_moves(self, board) -> list:
        from chessboard.board import Board

        legalMoves = []

        for currentCandidate in self.CANDIDATE_MOVE_COORDINATES:
            candidateDestinationCoordinate = self.piecePosition
            
            while(True):

                if (self.is_first_column_exclusion(candidateDestinationCoordinate, currentCandidate) 
                    or self.is_eight_column_exclusion(candidateDestinationCoordinate, currentCandidate)):
                    break

                candidateDestinationCoordinate += currentCandidate
                if BoardUtils.isSquareValid(candidateDestinationCoordinate):
                    candidateDestinationSquare = board.get_square(candidateDestinationCoordinate) 
                    if (candidateDestinationSquare.is_square_occupied() == False):
                        legalMoves.append(NormalMove(board, self, candidateDestinationSquare)) # Add a non-capture move
                        
                    else:
                        pieceAtDestination = candidateDestinationSquare.get_piece()
                        pieceAlliance = pieceAtDestination.get_piece_alliance()
                        if self.pieceAlliance != pieceAlliance:
                            legalMoves.append(CaptureMove(board, self, candidateDestinationSquare, pieceAtDestination)) # Add a capture move
                            break
                else:
                    break

        return legalMoves
    
    def get_piece_type(self):
        return self.piece_type
    
    
    # def __str__(self) -> str:
    #     return self.piece_type.value
    
    def is_first_column_exclusion(self, currentPosition, candidatePosition):
        '''
        This method checks if the Rook's current position is in the first column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the knight to "wrap around" to the 
        other side of the board. 
        
        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the knight is in the first column and the candidate move is invalid, False otherwise.
        '''
        return BoardUtils.FIRST_COLUMN[currentPosition] and candidatePosition == -1
    
    def is_eight_column_exclusion(self, currentPosition, candidatePosition):
        '''
        This method checks if the Rook's current position is in the eighth column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the knight to "wrap around" to the 
        other side of the board. 

        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the knight is in the eighth column and the candidate move is invalid, False otherwise.
        '''
        return BoardUtils.EIGHT_COLUMN[currentPosition] and candidatePosition == 1