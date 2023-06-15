from .player import Player
from chessboard.board import Board


class BlackPlayer(Player):
    def __init__(self, board, legal_moves, opponent_moves) -> None:
        super().__init__(board, legal_moves, opponent_moves)

    def get_active_pieces(self):
        return self.board.get_black_pieces()
    
    def get_alliance(self):
        from chessboard.alliance import Alliance
        return Alliance.BLACK
    
    def get_opponent(self):
        return self.board.white_player()