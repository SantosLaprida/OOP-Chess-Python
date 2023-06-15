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
        return self.board.black_player()