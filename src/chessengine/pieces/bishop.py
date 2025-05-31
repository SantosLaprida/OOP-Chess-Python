from .piece import Piece
from chessengine.chessboard.boardutils import BoardUtils
# from chessboard.board import Board



class Bishop(Piece):

    CANDIDATE_MOVE_COORDINATES = [-7, -9, 7, 9]

    def __init__(self, piece_position, piece_alliance):
        super().__init__(piece_position, piece_alliance)
        self.piece_type = Piece.PieceType.BISHOP

    def calculate_legal_moves(self, board) -> list:

        from chessengine.chessboard.square import Square, EmptySquare, OccupiedSquare
        from chessengine.chessboard.move import Move, NormalMove, CaptureMove
        from chessengine.chessboard.board import Board
        from chessengine.chessboard.alliance import Alliance

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
                    if (not candidateDestinationSquare.is_square_occupied()):
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
        # return Bishop(move.get_destination_coordinate(), move.get_moved_piece().get_piece_alliance())
        moved_bishop = Bishop(move.get_destination_coordinate(), move.get_moved_piece().get_piece_alliance())
        moved_bishop.is_first_move = False
        return moved_bishop
        
    
    def get_piece_type(self):
        return self.piece_type
    
    # def __str__(self) -> str:
    #     return self.piece_type.value
    
    def is_first_column_exclusion(self, currentPosition, candidatePosition):
        return BoardUtils.FIRST_COLUMN[currentPosition] and (candidatePosition == -9 or candidatePosition == 7)
    
    def is_eight_column_exclusion(self, currentPosition, candidatePosition):
        return BoardUtils.EIGHT_COLUMN[currentPosition] and (candidatePosition == -7 or candidatePosition == 9)