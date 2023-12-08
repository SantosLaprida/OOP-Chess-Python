from .piece import Piece
from chessboard.boardutils import BoardUtils
# from chessboard.board import Board



class Queen(Piece):

    CANDIDATE_MOVE_COORDINATES = [-9, -8, -7, -1, 8, 1, 7, 8, 9]

    def __init__(self, piece_position, piece_alliance):
        super().__init__(piece_position, piece_alliance)
        self.piece_type = Piece.PieceType.QUEEN

    def calculate_legal_moves(self, board) -> list:

        from chessboard.move import Move, NormalMove, CaptureMove
        from chessboard.square import Square, EmptySquare, OccupiedSquare
        from chessboard.board import Board

        legalMoves = []

        for currentCandidate in self.CANDIDATE_MOVE_COORDINATES:
            candidateDestinationCoordinate = self.piece_position
            while(True):

                if (self.is_first_column_exclusion(candidateDestinationCoordinate, currentCandidate) 
                    or self.is_eight_column_exclusion(candidateDestinationCoordinate, currentCandidate)):
                    break

                candidateDestinationCoordinate += currentCandidate
                if BoardUtils.isSquareValid(candidateDestinationCoordinate):
                    candidateDestinationSquare = board.get_square(candidateDestinationCoordinate) 
                    if (candidateDestinationSquare.is_square_occupied() == False):
                        legalMoves.append(NormalMove(board, self, candidateDestinationCoordinate))
                        
                    else:
                        pieceAtDestination = candidateDestinationSquare.get_piece()
                        piece_alliance = pieceAtDestination.get_piece_alliance()
                        if self.piece_alliance != piece_alliance:
                            legalMoves.append(CaptureMove(board, self, candidateDestinationCoordinate, pieceAtDestination))
                            break
                        break
                else:
                    break

        return legalMoves
    

    def move_piece(self, move):
        # return Queen(move.get_destination_coordinate(), move.get_moved_piece().get_piece_alliance())
        moved_queen = Queen(move.get_destination_coordinate(), move.get_moved_piece().get_piece_alliance())
        moved_queen.is_first_move = False
        return moved_queen
    

    def get_piece_type(self):
        return self.piece_type

    # def __str__(self) -> str:
    #     return self.piece_type.value
    

    def is_first_column_exclusion(self, currentPosition, candidatePosition):
        
        '''
        This method checks if the Queen's current position is in the first column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the Queen to "wrap around" to the 
        other side of the board. 
        
        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the Queen is in the first column and the candidate move is invalid, False otherwise.
        '''

        return BoardUtils.FIRST_COLUMN[currentPosition] and (candidatePosition == -1 or candidatePosition == -9 or candidatePosition == 7)
    


    def is_eight_column_exclusion(self, currentPosition, candidatePosition):
        
        '''
        This method checks if the Queen's current position is in the eighth column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the Queen to "wrap around" to the 
        other side of the board. 

        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the Wueen is in the eighth column and the candidate move is invalid, False otherwise.
        
        '''
        
        return BoardUtils.EIGHT_COLUMN[currentPosition] and (candidatePosition == 1 or candidatePosition == -7 or candidatePosition == 9)