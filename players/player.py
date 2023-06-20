from abc import ABC, abstractmethod
from chessboard.board import Board
from pieces.piece import Piece
#from chessboard.alliance import Alliance
from .move_transition import MoveTransition


class Player(ABC):
    def __init__(self, board, legal_moves, opponent_moves) -> None:
        
        self.board = board
        self.player_king = self.establish_king()
        self.legal_moves = legal_moves + self.calculate_king_castles(legal_moves, opponent_moves)
        self.opponent_moves = opponent_moves
        self.is_king_on_check = not bool(self.calculate_attacks_on_square(self.player_king.get_piece_position(), self.opponent_moves))


    @abstractmethod
    def get_active_pieces():
        pass

    @abstractmethod
    def get_alliance():
        pass

    @abstractmethod
    def get_opponent():
        pass

    @abstractmethod
    def calculate_king_castles(player_legals, opponent_legals):
        pass

    def calculate_attacks_on_square(self, square_coordinate, opponent_moves):

        from chessboard.move import Move

        attack_moves = []
        for move in opponent_moves:
            if square_coordinate == move.get_destination_coordinate():
                attack_moves.append(move)

        return attack_moves


    def establish_king(self):
        '''
        This method ensures that there is a king for the player in the board so the board is legal
        '''
        for piece in self.get_active_pieces():
            
            if piece.get_piece_type() == Piece.PieceType.KING:
                
                return piece
            
        
        raise ValueError("Invalid Board")
        
    def get_legal_moves(self):
        from chessboard.move import Move
        return self.legal_moves

    def get_player_king(self):
        return self.player_king

    def is_move_legal(self, move):
        return move in self.legal_moves

    def is_in_check(self):
        return self.is_king_on_check
    
    def is_in_checkmate(self):
        return self.is_in_check and not self.has_escape_moves()
    
    def is_in_stalemate(self):
        return not self.is_in_check and not self.has_escape_moves()
    
    def has_castled(self):
        return None
    
    def has_escape_moves(self):
        '''
        This method loops through all the player's legal moves, and performs the move in a another board.
        If one of the moves is succesful then we return True
        '''
        for move in self.legal_moves:
            transition = self.make_move(move)
            if transition.is_done():
                return True
        return False
    
    def make_move(self, move):
        '''
        This method returns a move_transition if the move is valid. 
        Move_transition contains the new board after the move is executed
        '''
        if not self.is_move_legal(move):
            return MoveTransition(self.board, move, MoveTransition.MoveStatus.ILLEGAL_MOVE)
        
        transition_board = move.execute()

        
        king_attacks = self.calculate_attacks_on_square(transition_board.get_current_player().get_opponent().get_player_king().get_piece_position(), 
                                                        transition_board.get_current_player().get_legal_moves())
        
        if king_attacks:
            ''' If in the new board (transition_board), 
            the current player king's position is being attacked by any of the opponent's pieces, the move is not legal
            '''
            return MoveTransition(transition_board, move, MoveTransition.MoveStatus.LEAVES_PLAYER_IN_CHECK)
        

        return MoveTransition(transition_board, move, MoveTransition.MoveStatus.DONE)