from abc import ABC, abstractmethod
from chessboard.board import Board
from pieces.piece import Piece


class Player(ABC):
    def __init__(self, board, legal_moves, opponent_moves) -> None:
        self.board = board
        self.legal_moves = legal_moves
        self.opponent_moves = opponent_moves
        self.player_king = self.establish_king()

    def establish_king(self):
        '''
        This method ensures that there is a king for the player in the board so the board is legal
        '''
        for piece in self.get_active_pieces():
            if piece.get_piece_type() == Piece.PieceType.KING:
                return piece

    @abstractmethod
    def get_active_pieces(self):
        pass

    
