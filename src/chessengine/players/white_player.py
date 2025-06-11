from .player import Player
#from chessboard.board import Board
#from chessboard.alliance import Alliance


class WhitePlayer(Player):
    
    def __init__(self, board, legal_moves=None, opponent_moves=None) -> None:
        super().__init__(board, legal_moves, opponent_moves)


    def can_castle(self):
        if 'K' in self.board.get_castling_rights() or 'Q' in self.board.get_castling_rights():
            return True
        return False
    

    def get_active_pieces(self):
        return self.board.get_white_pieces()
    
    def get_alliance(self):

        from chessengine.chessboard.alliance import Alliance
        
        return Alliance.WHITE
    
    def get_opponent(self):
        return self.board.black_player
    
    def calculate_king_castles(self, player_legals, opponent_legals):
        from chessengine.pieces.piece import Piece 
        from chessengine.chessboard.move import Move, CastleMove, KingSideCastleMove, QueenSideCastleMove

        king_castles = []

        current_player = self.board.get_current_player()
        if current_player is not None and current_player.get_alliance() == self.get_alliance():
            if self.get_player_king().is_first_move and not self.is_in_check:

                # white king side castle calculation
                if self.board.get_white_can_castle_kingside():
                    if (not self.board.get_square(61).is_square_occupied() and not self.board.get_square(62).is_square_occupied()):
                        rook_square = self.board.get_square(63)
                        if (rook_square.is_square_occupied() and rook_square.get_piece().is_first_move):

                            if (not (self.calculate_attacks_on_square(61, self.opponent_moves))
                                and not (self.calculate_attacks_on_square(62, self.opponent_moves)) 
                                and rook_square.get_piece().get_piece_type() == Piece.PieceType.ROOK):
                                king_castles.append(CastleMove(self.board, 
                                self.get_player_king(), 62, rook_square.get_piece(), 
                                rook_square.get_square_coordinate(), 61))


                # white queenside castle calculation
                if self.board.get_white_can_castle_queenside():
                    if (not self.board.get_square(59).is_square_occupied() 
                        and not self.board.get_square(58).is_square_occupied() 
                        and not self.board.get_square(57).is_square_occupied()):
                        rook_square = self.board.get_square(56)
                        if (rook_square.is_square_occupied() and rook_square.get_piece().is_first_move):
                            if (not (self.calculate_attacks_on_square(59, self.opponent_moves)) 
                                and not (self.calculate_attacks_on_square(58, self.opponent_moves)) 
                                and not (self.calculate_attacks_on_square(57, self. opponent_moves)) and rook_square.get_piece().get_piece_type() == Piece.PieceType.ROOK):
                                
                                king_castles.append(CastleMove(self.board, self.get_player_king(), 
                                                                        58, rook_square.get_piece(), 
                                                                        rook_square.get_square_coordinate(), 59))
        return king_castles

            