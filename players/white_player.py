from .player import Player
from chessboard.board import Board
#from chessboard.alliance import Alliance


class WhitePlayer(Player):
    def __init__(self, board, legal_moves, opponent_moves) -> None:
        super().__init__(board, legal_moves, opponent_moves)


    def get_active_pieces(self):
        return self.board.get_white_pieces()
    
    def get_alliance(self):

        from chessboard.alliance import Alliance
        
        return Alliance.WHITE
    
    def get_opponent(self):
        return self.board.black_player
    
    def calculate_king_castles(self, player_legals, opponent_legals):
        from pieces.piece import Piece 

        king_castles = []

        if self.player_king.is_first_move() and not self.is_in_check():
            # white king side castle calculation
            if (not self.board.get_square(63).is_square_occupied() and not self.board.get_square(62).is_square_occupied()):
                rook_square = self.board.get_square(63)
                if (rook_square.is_square_occupied() and rook_square.get_piece().is_first_move()):
                    if (not (Player.calculate_attacks_on_square(61, self.opponent_moves)) 
                        and not (Player.calculate_attacks_on_square(62, self.opponent_moves)) 
                        and rook_square.get_piece_type() == Piece.PieceType.ROOK):
                        king_castles.append(None) # TODO

            # white queenside castle calculation
            if (not self.board.get_square(59).is_square_occupied 
                and not self.board.get_square(58).is_square_occupied 
                and not self.board.get_square(57).is_square_occupied):
                rook_square = self.board.get_square(56)
                if (rook_square.is_square_occupied() and rook_square.get_piece().is_first_move()):
                    if (not (Player.calculate_attacks_on_square(59, self.opponent_moves)) 
                        and not (Player.calculate_attacks_on_square(58, self.opponent_moves)) 
                        and not (Player.calculate_attacks_on_square(57, self. opponent_moves)) and rook_square.get_piece_type() == Piece.PieceType.ROOK):
                        #TODO
                        king_castles.append(None)


            return king_castles

            