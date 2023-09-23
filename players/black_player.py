from .player import Player
from chessboard.board import Board


class BlackPlayer(Player):
    def __init__(self, board, legal_moves=None, opponent_moves=None) -> None:
        super().__init__(board, legal_moves, opponent_moves)

    def get_active_pieces(self):
        return self.board.get_black_pieces()
    
    def get_alliance(self):

        from chessboard.alliance import Alliance

        return Alliance.BLACK
    
    def get_opponent(self):
        return self.board.white_player
    
    def calculate_king_castles(self, player_legals, opponent_legals):
        from pieces.piece import Piece 
        from chessboard.move import Move, CastleMove, KingSideCastleMove, QueenSideCastleMove

        king_castles = []

        if self.player_king.is_first_move and not self.is_in_check():
            # Black king side castle calculation
            if (not self.board.get_square(5).is_square_occupied() and not self.board.get_square(6).is_square_occupied()):
                rook_square = self.board.get_square(7)
                if (rook_square.is_square_occupied() and rook_square.get_piece().is_first_move()):
                    if (not (Player.calculate_attacks_on_square(5, self.opponent_moves)) 
                        and not (Player.calculate_attacks_on_square(6, self.opponent_moves)) 
                        and rook_square.get_piece_type() == Piece.PieceType.ROOK):
                        king_castles.append(KingSideCastleMove(self.board, 
                                                               self.get_player_king(), 
                                                               6, 
                                                               rook_square.get_piece(), 
                                                               rook_square.get_square_coordinate(), 
                                                               5))

            # Black queenside castle calculation
            if (not self.board.get_square(1).is_square_occupied 
                and not self.board.get_square(2).is_square_occupied 
                and not self.board.get_square(3).is_square_occupied):
                rook_square = self.board.get_square(0)
                if (rook_square.is_square_occupied() and rook_square.get_piece().is_first_move()):
                    if (not (Player.calculate_attacks_on_square(1, self.opponent_moves)) 
                        and not (Player.calculate_attacks_on_square(2, self.opponent_moves)) 
                        and not (Player.calculate_attacks_on_square(3, self. opponent_moves)) and rook_square.get_piece_type() == Piece.PieceType.ROOK):
                        #TODO
                        king_castles.append(QueenSideCastleMove(self.board, 
                                                                self.get_player_king(), 
                                                                2, 
                                                                rook_square.get_piece(), 
                                                                rook_square.get_square_coordinate(), 
                                                                3))

        return king_castles