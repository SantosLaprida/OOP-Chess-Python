from .piece import Piece
from chessboard.boardutils import BoardUtils
# from chessboard.board import Board
from chessboard.move import Move, NormalMove, CaptureMove
from chessboard.square import Square, EmptySquare, OccupiedSquare

class Pawn(Piece):

    CANDIDATE_MOVE_COORDINATES = [7 ,8 ,9, 16]

    def __init__(self, piecePosition, pieceAlliance):
        super().__init__(piecePosition, pieceAlliance)
        self.piece_type = Piece.PieceType.PAWN


    def calculate_legal_moves(self, board) -> list:

        from chessboard.board import Board

        legalMoves = []

        for currentCandidate in self.CANDIDATE_MOVE_COORDINATES:
            candidateDestinationCoordinate = self.piecePosition + (self.pieceAlliance.get_direction * currentCandidate)
            if BoardUtils.isSquareValid(candidateDestinationCoordinate) == False:
                continue

            if currentCandidate == 8 and (board.get_square(candidateDestinationCoordinate)).is_square_occupied() == False:
                '''
                This handles the pawn move one square up if white, and one square down if black
                '''
                # TODO (DEAL WITH PROMOTIONS)
                legalMoves.append(NormalMove(board, self, candidateDestinationCoordinate))
            elif (currentCandidate == 16 and self.is_first_move() and 
            (BoardUtils.SECOND_ROW[self.piecePosition] and self.pieceAlliance.is_black()) or 
            (BoardUtils.SEVENTH_ROW[self.piecePosition] and self.pieceAlliance.is_white())): # First move of a pawn can be two squares
                '''
                This handles the two square jump of a pawn when it is it's first move
                '''
                behind_candidate_destination_coordinate = self.piecePosition + (self.pieceAlliance.get_direction * 8)
                if board.get_square(behind_candidate_destination_coordinate).is_square_occupied() == False and board.get_square(candidateDestinationCoordinate).is_square_occupied() == False:
                    legalMoves.append(NormalMove(board, self, candidateDestinationCoordinate))

            elif currentCandidate == 7:
                if BoardUtils.EIGHT_COLUMN[self.piecePosition] and self.pieceAlliance.is_white():
                    '''
                    Exceptional condition
                    '''
                    continue
                if BoardUtils.FIRST_COLUMN[self.piecePosition] and self.pieceAlliance.is_black():
                    '''
                    Exceptional condition
                    '''
                    continue
                
                if board.get_square(candidateDestinationCoordinate).is_square_occupied():
                    piece_on_candidate = board.get_square().get_piece()
                    if self.pieceAlliance != piece_on_candidate.get_piece_alliance():
                        #TODO !!!! (HANDLE ATTACKING INTO A PROMOTION)
                        legalMoves.append(CaptureMove(board, self, candidateDestinationCoordinate, piece_on_candidate))

            elif currentCandidate == 9:
                if BoardUtils.EIGHT_COLUMN[self.piecePosition] and self.pieceAlliance.is_black():
                    '''
                    Exceptional condition
                    '''
                    continue
                if BoardUtils.FIRST_COLUMN[self.piecePosition] and self.pieceAlliance.is_white():
                    '''
                    Exceptional condition
                    '''
                    continue


        return legalMoves
    
    def get_piece_type(self):
        return self.piece_type

    # def __str__(self) -> str:
    #     return self.piece_type.value