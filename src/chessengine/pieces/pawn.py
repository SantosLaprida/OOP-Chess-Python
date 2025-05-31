from .piece import Piece
from chessengine.chessboard.boardutils import BoardUtils
from chessengine.chessboard.notation import Notation
# from chessboard.board import Board



class Pawn(Piece):

    CANDIDATE_MOVE_COORDINATES = [7 ,8 ,9, 16]

    def __init__(self, piece_position, piece_alliance):
        super().__init__(piece_position, piece_alliance)
        self.piece_type = Piece.PieceType.PAWN


    def calculate_legal_moves(self, board) -> list:

        from chessengine.chessboard.move import Move, NormalMove, CaptureMove, PawnJump, PawnEnPassantAttack
        from chessengine.chessboard.board import Board
        from chessengine.chessboard.square import Square, EmptySquare, OccupiedSquare
        from chessengine.chessboard.alliance import Alliance

        legalMoves = []
        en_passant = board.get_en_passant()
        en_passant_target = board.get_en_passant_target()

        for currentCandidate in self.CANDIDATE_MOVE_COORDINATES:

            candidateDestinationCoordinate = self.piece_position + (self.piece_alliance.get_direction * currentCandidate)
            if BoardUtils.isSquareValid(candidateDestinationCoordinate) == False:
                continue

            if currentCandidate == 8 and (board.get_square(candidateDestinationCoordinate)).is_square_occupied() == False:
                '''
                This handles the pawn move one square up if white, and one square down if black
                '''
                # TODO (DEAL WITH PROMOTIONS)


                legalMoves.append(NormalMove(board, self, candidateDestinationCoordinate))

            elif (currentCandidate == 16 and self.is_first_move and 
                ((BoardUtils.SECOND_ROW[self.piece_position] and self.piece_alliance.is_black()) or 
                (BoardUtils.SEVENTH_ROW[self.piece_position] and self.piece_alliance.is_white()))): # First move of a pawn can be two squares
                '''
                This handles the two square jump of a pawn when it is it's first move
                '''
                behind_candidate_destination_coordinate = self.piece_position + (self.piece_alliance.get_direction * 8)
                if board.get_square(behind_candidate_destination_coordinate).is_square_occupied() == False and board.get_square(candidateDestinationCoordinate).is_square_occupied() == False:
                    

                    legalMoves.append(PawnJump(board, self, candidateDestinationCoordinate))

            elif currentCandidate == 7:

                if BoardUtils.EIGHT_COLUMN[self.piece_position] and self.piece_alliance.is_white():
                    '''
                    Exceptional condition
                    '''
                    continue
                if BoardUtils.FIRST_COLUMN[self.piece_position] and self.piece_alliance.is_black():
                    '''
                    Exceptional condition
                    '''
                    continue
                
                if en_passant and en_passant_target == candidateDestinationCoordinate:
                    legalMoves.append(PawnEnPassantAttack(board, self, candidateDestinationCoordinate, en_passant))

                if board.get_square(candidateDestinationCoordinate).is_square_occupied():
                    piece_on_candidate = board.get_square(candidateDestinationCoordinate).get_piece()
                    
                    if self.piece_alliance != piece_on_candidate.get_piece_alliance():

                        #TODO !!!! (HANDLE ATTACKING INTO A PROMOTION)
                
                        legalMoves.append(CaptureMove(board, self, candidateDestinationCoordinate, piece_on_candidate))


            elif currentCandidate == 9:
                if BoardUtils.EIGHT_COLUMN[self.piece_position] and self.piece_alliance.is_black():
                    '''
                    Exceptional condition
                    '''
                    continue
                if BoardUtils.FIRST_COLUMN[self.piece_position] and self.piece_alliance.is_white():
                    '''
                    Exceptional condition
                    '''
                    continue

                if en_passant and en_passant_target == candidateDestinationCoordinate:
                    legalMoves.append(PawnEnPassantAttack(board, self, candidateDestinationCoordinate, en_passant))

                if board.get_square(candidateDestinationCoordinate).is_square_occupied():
                    piece_on_candidate = board.get_square(candidateDestinationCoordinate).get_piece()
                    if self.piece_alliance != piece_on_candidate.get_piece_alliance():
                        #TODO !!!! (HANDLE ATTACKING INTO A PROMOTION)
                        
                        legalMoves.append(CaptureMove(board, self, candidateDestinationCoordinate, piece_on_candidate))


        return legalMoves
    

    def move_piece(self, move):
        moved_pawn = Pawn(move.get_destination_coordinate(), move.get_moved_piece().get_piece_alliance())
        moved_pawn.is_first_move = False
        return moved_pawn
    
    def get_piece_type(self):
        return self.piece_type

    # def __str__(self) -> str:
    #     return self.piece_type.value