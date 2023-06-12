from .piece import Piece
from chessboard.boardutils import BoardUtils
# from chessboard.board import Board
from chessboard.move import Move, NormalMove, CaptureMove
from chessboard.square import Square, EmptySquare, OccupiedSquare
from chessboard.alliance import Alliance

class Knight(Piece):

    CANDIDATE_MOVE_COORDINATES = [-17, -15, -10, -6, 6, 10, 15, 17]

    def __init__(self, piecePosition, pieceAlliance):
        super().__init__(piecePosition, pieceAlliance)
        self.piece_type = Piece.PieceType.KNIGHT
        
    def calculate_legal_moves(self, board) -> list:

        from chessboard.board import Board

        legalMoves = []

        for currentCandidate in self.CANDIDATE_MOVE_COORDINATES:
            candidateDestinationCoordinate = self.piecePosition + currentCandidate

            if BoardUtils.isSquareValid(candidateDestinationCoordinate): 

                if (self.is_first_column_exclusion(self.piecePosition, currentCandidate) or (self.is_second_column_exclusion(self.piecePosition, currentCandidate))
                    or (self.is_seventh_column_exclusion(self.piecePosition, currentCandidate)) or (self.is_eight_column_exclusion(self.piecePosition, currentCandidate))):
                    continue

                candidateDestinationSquare = board.get_square(candidateDestinationCoordinate) # get_square is yet to be implemented in board

                if (candidateDestinationSquare.is_square_occupied() == False):
                    legalMoves.append(NormalMove(board, self, candidateDestinationSquare)) # Move class is yet to be implemented
                else:
                    pieceAtDestination = candidateDestinationSquare.get_piece()
                    pieceAlliance = pieceAtDestination.get_piece_alliance()

                    if self.pieceAlliance != pieceAlliance:
                        legalMoves.append(CaptureMove())


        return legalMoves
    
    def is_first_column_exclusion(self, currentPosition, candidatePosition):
        '''
        This method checks if the knight's current position is in the first column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the knight to "wrap around" to the 
        other side of the board. 
        
        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the knight is in the first column and the candidate move is invalid, False otherwise.
        '''
        return BoardUtils.FIRST_COLUMN[currentPosition] and (candidatePosition == -17 or 
                                                             candidatePosition == -10 or 
                                                             candidatePosition == 6 or 
                                                             candidatePosition == 15)


    def is_second_column_exclusion(self, currentPosition, candidatePosition):
        '''
        This method checks if the knight's current position is in the second column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the knight to "wrap around" to the 
        other side of the board. 

        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the knight is in the second column and the candidate move is invalid, False otherwise.
        '''
        return BoardUtils.SECOND_COLUMN[currentPosition] and (candidatePosition == -10 or 
                                                             candidatePosition == 6)
    

    def get_piece_type(self):
        return self.piece_type


    # def __str__(self) -> str:
    #     if self.pieceAlliance == Alliance.is_black(self):
    #         return str(self.piece_type.value).lower()
    #     else:
    #         return str(self.piece_type.value)
    


    def is_seventh_column_exclusion(self, currentPosition, candidatePosition):
        '''
        This method checks if the knight's current position is in the seventh column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the knight to "wrap around" to the 
        other side of the board. 

        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the knight is in the seventh column and the candidate move is invalid, False otherwise.
        '''
        return BoardUtils.SEVENTH_COLUMN[currentPosition] and (candidatePosition == -6 or candidatePosition == 10)
    


    def is_eight_column_exclusion(self, currentPosition, candidatePosition):
        '''
        This method checks if the knight's current position is in the eighth column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the knight to "wrap around" to the 
        other side of the board. 

        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the knight is in the eighth column and the candidate move is invalid, False otherwise.
        '''
        return BoardUtils.EIGHT_COLUMN[currentPosition] and (candidatePosition == -15 or 
                                                             candidatePosition == -6 or 
                                                             candidatePosition == 10 or 
                                                             candidatePosition == 17)