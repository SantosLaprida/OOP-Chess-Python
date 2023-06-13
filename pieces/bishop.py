from .piece import Piece
from chessboard.boardutils import BoardUtils
# from chessboard.board import Board
from chessboard.move import Move, NormalMove, CaptureMove
from chessboard.square import Square, EmptySquare, OccupiedSquare

class Bishop(Piece):

    CANDIDATE_MOVE_COORDINATES = [-7, -9, 7, 9]

    def __init__(self, piecePosition, pieceAlliance):
        super().__init__(piecePosition, pieceAlliance)
        self.piece_type = Piece.PieceType.BISHOP

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
                        legalMoves.append(NormalMove(board, self, candidateDestinationSquare))
                        
                    else:
                        pieceAtDestination = candidateDestinationSquare.get_piece()
                        pieceAlliance = pieceAtDestination.get_piece_alliance()
                        if self.pieceAlliance != pieceAlliance:
                            legalMoves.append(CaptureMove(board, self, candidateDestinationSquare, pieceAtDestination))
                            break
                else:
                    break

        return legalMoves
    
    def get_piece_type(self):
        return self.piece_type
    
    # def __str__(self) -> str:
    #     return self.piece_type.value
    
    def is_first_column_exclusion(self, currentPosition, candidatePosition):
        return BoardUtils.FIRST_COLUMN[currentPosition] and (candidatePosition == -9 or candidatePosition == 7)
    
    def is_eight_column_exclusion(self, currentPosition, candidatePosition):
        return BoardUtils.EIGHT_COLUMN[currentPosition] and (candidatePosition == -7 or candidatePosition == 9)