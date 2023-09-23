from .piece import Piece
from chessboard.boardutils import BoardUtils
# from chessboard.board import Board


class King(Piece):

    CANDIDATE_MOVE_COORDINATES = [-1, -7, -8, -9, 1, 7, 8, 9]

    def __init__(self, piece_position, piece_alliance) -> None:
        super().__init__(piece_position, piece_alliance)
        self.piece_type = Piece.PieceType.KING


    def calculate_legal_moves(self, board) -> list:

        from chessboard.square import Square, EmptySquare, OccupiedSquare
        from chessboard.move import Move, NormalMove, CaptureMove
        from chessboard.board import Board
        from chessboard.alliance import Alliance
        from players import player, white_player, black_player

        legalMoves = []

        for currentCandidate in self.CANDIDATE_MOVE_COORDINATES:
            candidateDestinationCoordinate = self.piece_position + currentCandidate

            if self.is_first_column_exclusion(self.piece_position, currentCandidate) or self.is_eight_column_exclusion(self.piece_position, currentCandidate):
                continue

            if BoardUtils.isSquareValid(candidateDestinationCoordinate):
                candidateDestinationSquare = board.get_square(candidateDestinationCoordinate)

                if (candidateDestinationSquare.is_square_occupied() == False):
                    legalMoves.append(NormalMove(board, self, candidateDestinationSquare)) 
                else:
                    pieceAtDestination = candidateDestinationSquare.get_piece()
                    piece_alliance = pieceAtDestination.get_piece_alliance()

                    if self.piece_alliance != piece_alliance:
                        legalMoves.append(CaptureMove(board, self, candidateDestinationSquare, pieceAtDestination))


        # print(board.get_current_player())
        # print(type(board.get_current_player()))
        castling_moves = board.get_current_player().calculate_king_castles(board.get_current_player().get_legal_moves(), board.get_current_player().get_opponent_moves())
        legalMoves.extend(castling_moves)

        return legalMoves
    
    def move_piece(self, move):
        
        from chessboard.square import Square, EmptySquare, OccupiedSquare
        from chessboard.move import Move, NormalMove, CaptureMove
        from chessboard.board import Board
        from chessboard.alliance import Alliance

        #return King(move.get_destination_coordinate(), move.get_moved_piece().get_piece_alliance())
        moved_king = King(move.get_destination_coordinate(), move.get_moved_piece().get_piece_alliance())
        moved_king.is_first_move = False
        return moved_king


    def get_piece_type(self):
        return self.piece_type
    
    # def __str__(self) -> str:
    #     return self.piece_type.value



    def is_first_column_exclusion(self, currentPosition, candidatePosition):
        '''
        This method checks if the King's current position is in the first column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the King to "wrap around" to the 
        other side of the board. 
        
        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the King is in the first column and the candidate move is invalid, False otherwise.
        '''
        return BoardUtils.FIRST_COLUMN[currentPosition] and (candidatePosition == -1 or candidatePosition == -9 or candidatePosition == 7)

    def is_eight_column_exclusion(self, currentPosition, candidatePosition):
        '''
        This method checks if the King's current position is in the eighth column of the board. If it is, certain moves
        (represented by the candidatePosition) are not valid as they would cause the King to "wrap around" to the 
        other side of the board. 

        Args:
            currentPosition (int): The current position of the knight.
            candidatePosition (int): The candidate position that the knight wants to move to.

        Returns:
            bool: True if the King is in the eighth column and the candidate move is invalid, False otherwise.
        '''
        return BoardUtils.EIGHT_COLUMN[currentPosition] and (candidatePosition == -7 or candidatePosition == 1 or candidatePosition == 9)