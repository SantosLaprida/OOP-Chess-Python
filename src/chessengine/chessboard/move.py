from abc import ABC, abstractmethod
from chessengine.players.player import Player
from chessengine.pieces.piece import Piece
from chessengine.pieces.pawn import Pawn
from chessengine.pieces.rook import Rook
from chessengine.pieces.king import King
from chessengine.chessboard.notation import Notation
from chessengine.chessboard.boardutils import BoardUtils


class Move(ABC):

    """
    This class represents a move made in the game. It is abstract, 
    and specific types of moves should be represented by subclasses.
    """


    def __init__(self, board, movedPiece, destinationSquare) -> None:
        
        """
        :param board: The current state of the game board.
        :param movedPiece: The piece that is being moved.
        :param destinationSquare: The square the movedPiece is moving to.
        """

        self.board = board
        self.movedPiece = movedPiece
        self.destinationSquare = destinationSquare

    def execute(self):

        from chessengine.players.black_player import BlackPlayer
        from chessengine.players.white_player import WhitePlayer
        from chessengine.chessboard.alliance import Alliance

        from chessengine.chessboard.board import Board

        '''
        When a move is executed, the current board is not mutated. Instead, a new board is created
        '''

        builder = Board.Builder()
        for piece in self.board.get_current_player().get_active_pieces():
            
            if not self.movedPiece == piece:
                builder.set_piece(piece)
   
        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            builder.set_piece(piece)

        # if isinstance(self.movedPiece, King):
        #     if self.movedPiece.get_piece_alliance() == Alliance.WHITE:
        #         builder.set_castling_rights(False, False, self.board.get_black_can_castle_kingside(), self.board.get_black_can_castle_queenside())
        #     else:
        #         builder.set_castling_rights(self.board.get_white_can_castle_kingside(), self.board.get_white_can_castle_queenside(), False, False)

        # elif isinstance(self.movedPiece, Rook):
        #     if self.movedPiece.get_piece_alliance() == Alliance.WHITE:
        #         if self.movedPiece.get_piece_position() == 56:
        #             builder.set_castling_rights(self.board.get_white_can_castle_kingside(), 
        #                                         False, self.board.get_black_can_castle_kingside(), 
        #                                         self.board.get_black_can_castle_queenside())
        #         elif self.movedPiece.get_piece_position() == 63:
        #             builder.set_castling_rights(False, self.board.get_white_can_castle_queenside(), 
        #                                         self.board.get_black_can_castle_kingside(), 
        #                                         self.board.get_black_can_castle_queenside())
        #     elif self.movedPiece.get_piece_alliance() == Alliance.BLACK:
        #         if self.movedPiece.get_piece_position() == 0:
        #             builder.set_castling_rights(self.board.get_white_can_castle_kingside(), 
        #                                         self.board.get_white_can_castle_queenside(), 
        #                                         self.board.get_black_can_castle_kingside(), False)
        #         elif self.movedPiece.get_piece_position() == 7:
        #             builder.set_castling_rights(self.board.get_white_can_castle_kingside(), 
        #                                         self.board.get_white_can_castle_queenside(), 
        #                                         False, self.board.get_black_can_castle_queenside())
            

        # else:
        #     builder.set_castling_rights(self.board.get_white_can_castle_kingside(), self.board.get_white_can_castle_queenside(), 
        #                                 self.board.get_black_can_castle_kingside(), self.board.get_black_can_castle_queenside())

        K, Q, k, q = BoardUtils.adjust_castling_rights(self.board, self.movedPiece)
        builder.set_castling_rights(K, Q, k, q)


        builder.set_piece(self.movedPiece.move_piece(self)) 
        builder.set_move_maker(self.board.get_current_player().get_opponent().get_alliance())
        if self.board.get_current_player().get_alliance() == Alliance.BLACK:
            builder.set_fullmove_counter(self.board.get_fullmove_counter() + 1)
        else:
            builder.set_fullmove_counter(self.board.get_fullmove_counter())
        new_board = builder.build()
        
        return new_board

    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + hash(self.board)
        result = prime * result + self.destinationSquare
        result = prime * result + hash(self.movedPiece)
        return result
    
    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return (self.destinationSquare == other.destinationSquare 
                    and self.movedPiece == other.movedPiece 
                    and self.get_current_coordinate() == other.get_current_coordinate())
        return False

    def get_current_coordinate(self):
        return self.get_moved_piece().get_piece_position()

    def get_destination_coordinate(self):
        return self.destinationSquare
    
    def get_moved_piece(self):
        return self.movedPiece
    
    def is_attack(self):
        return False
    
    def is_castling_move(self):
        return False
    
    def get_attacked_piece(self):
        return None

    def __str__(self):
        return f"Move {self.get_moved_piece()} from {Notation.coordinate_to_notation(self.get_current_coordinate())} to {Notation.coordinate_to_notation(self.get_destination_coordinate())}"

    def __repr__(self):
        return self.__str__()



class NormalMove(Move):
    from chessengine.pieces.piece import Piece
    """
    This class represents a normal move in the game, 
    a move where no piece is captured.
    """
    def __init__(self, board, movedPiece, destinationSquare) -> None:
        super().__init__(board, movedPiece, destinationSquare)

    
class CaptureMove(Move):
    """
    This class represents a capture move in the game, 
    a move where a piece is captured.
    """
    def __init__(self, board, movedPiece, destinationSquare, attackedPiece) -> None:
        super().__init__(board, movedPiece, destinationSquare)
        self.attackedPiece = attackedPiece

    def is_attack(self):
        return True
    
    def get_attacked_piece(self):
        return self.attackedPiece
    
    def is_castling_move(self):
        return False
    
    def __hash__(self):
        return self.attackedPiece.__hash__() + super.__hash__()

    def __eq__(self, other):
        if super().__eq__(other) and isinstance(other, self.__class__):
            return self.attackedPiece == other.attackedPiece
        return False



    def execute(self):

        from chessengine.players.black_player import BlackPlayer
        from chessengine.players.white_player import WhitePlayer
        from chessengine.chessboard.alliance import Alliance

        from chessengine.chessboard.board import Board

        '''
        When a move is executed, the current board is not mutated. Instead, a new board is created
        '''

        builder = Board.Builder()

        for piece in self.board.get_current_player().get_active_pieces():
            
            if not self.movedPiece == piece:
                builder.set_piece(piece)
   
        for piece in self.board.get_current_player().get_opponent().get_active_pieces():

            if not self.attackedPiece == piece:
                '''
                Skip the attacked piece
                '''
                builder.set_piece(piece)

        # if isinstance(self.movedPiece, King):
        #     if self.movedPiece.get_piece_alliance() == Alliance.WHITE:
        #         builder.set_castling_rights(False, False, self.board.get_black_can_castle_kingside(), self.board.get_black_can_castle_queenside())
        #     else:
        #         builder.set_castling_rights(self.board.get_white_can_castle_kingside(), self.board.get_white_can_castle_queenside(), False, False)

        # elif isinstance(self.movedPiece, Rook):
        #     if self.movedPiece.get_piece_alliance() == Alliance.WHITE:
        #         if self.movedPiece.get_piece_position() == 56:
        #             builder.set_castling_rights(self.board.get_white_can_castle_kingside(), 
        #                                         False, self.board.get_black_can_castle_kingside(), 
        #                                         self.board.get_black_can_castle_queenside())
        #         elif self.movedPiece.get_piece_position() == 63:
        #             builder.set_castling_rights(False, self.get_board.white_can_castle_queenside(), 
        #                                         self.board.get_black_can_castle_kingside(), 
        #                                         self.board.get_black_can_castle_queenside())
        #     elif self.movedPiece.get_piece_alliance() == Alliance.BLACK:
        #         if self.movedPiece.get_piece_position() == 0:
        #             builder.set_castling_rights(self.board.get_white_can_castle_kingside(), 
        #                                         self.board.get_white_can_castle_queenside(), 
        #                                         self.board.get_black_can_castle_kingside(), False)
        #         elif self.movedPiece.get_piece_position() == 7:
        #             builder.set_castling_rights(self.board.get_white_can_castle_kingside(), 
        #                                         self.board.get_white_can_castle_queenside(), 
        #                                         False, self.board.get_black_can_castle_queenside())

        # else:
        #     builder.set_castling_rights(self.board.get_white_can_castle_kingside(), self.board.get_white_can_castle_queenside(), 
        #                                 self.board.get_black_can_castle_kingside(), self.board.get_black_can_castle_queenside())

        K, Q, k, q = BoardUtils.adjust_castling_rights(self.board, self.movedPiece)
        builder.set_castling_rights(K, Q, k, q)


        builder.set_piece(self.movedPiece.move_piece(self)) 
        builder.set_move_maker(self.board.get_current_player().get_opponent().get_alliance())

        if self.board.get_current_player().get_alliance() == Alliance.BLACK:
            builder.set_fullmove_counter(self.board.get_fullmove_counter() + 1)
        else:
            builder.set_fullmove_counter(self.board.get_fullmove_counter())

        new_board = builder.build()
        
        return new_board

    
class PawnMove(Move):
    def __init__(self, board, movedPiece, destinationSquare) -> None:
        super().__init__(board, movedPiece, destinationSquare)

class PawnAttackMove(CaptureMove):
    def __init__(self, board, movedPiece, destinationSquare, attackedPiece) -> None:
        super().__init__(board, movedPiece, destinationSquare, attackedPiece)

class PawnEnPassantAttack(PawnAttackMove):
    def __init__(self, board, movedPiece, destinationSquare, attackedPiece) -> None:
        super().__init__(board, movedPiece, destinationSquare, attackedPiece)

    def execute(self):
        
        from chessengine.players.black_player import BlackPlayer
        from chessengine.players.white_player import WhitePlayer
        from chessengine.chessboard.alliance import Alliance

        from .board import Board
        '''
        When a move is executed, the current board is not mutated. Instead, a new board is created
        '''
        builder = Board.Builder()
        for piece in self.board.get_current_player().get_active_pieces():
            
            if not self.movedPiece == piece:
                builder.set_piece(piece)
   
        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            if not self.attackedPiece == piece:
                builder.set_piece(piece)

        moved_pawn = self.movedPiece.move_piece(self)
        builder.set_piece(moved_pawn)
        builder.set_move_maker(self.board.get_current_player().get_opponent().get_alliance())

        if self.board.get_current_player().get_alliance() == Alliance.BLACK:
            builder.set_fullmove_counter(self.board.get_fullmove_counter() + 1)
        else:
            builder.set_fullmove_counter(self.board.get_fullmove_counter())

        new_board = builder.build()
        return new_board

class PawnJump(Move):
    def __init__(self, board, movedPiece, destinationSquare) -> None:
        super().__init__(board, movedPiece, destinationSquare)


    def execute(self):

        from chessengine.players.black_player import BlackPlayer
        from chessengine.players.white_player import WhitePlayer
        from chessengine.chessboard.alliance import Alliance

        from .board import Board
        '''
        When a move is executed, the current board is not mutated. Instead, a new board is created
        '''
        builder = Board.Builder()
        for piece in self.board.get_current_player().get_active_pieces():
            
            if not self.movedPiece == piece:
                builder.set_piece(piece)
   
        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            builder.set_piece(piece)

        moved_pawn = self.movedPiece.move_piece(self)
        builder.set_castling_rights(self.board.white_can_castle_kingside, self.board.white_can_castle_queenside, self.board.black_can_castle_kingside, self.board.black_can_castle_queenside)
        builder.set_piece(moved_pawn)
        builder.set_en_passant_pawn(moved_pawn)
        builder.set_move_maker(self.board.get_current_player().get_opponent().get_alliance())

        if self.board.get_current_player().get_alliance() == Alliance.BLACK:
            builder.set_fullmove_counter(self.board.get_fullmove_counter() + 1)
        else:
            builder.set_fullmove_counter(self.board.get_fullmove_counter())

        new_board = builder.build()
        return new_board

class CastleMove(Move, ABC):
    def __init__(self, board, movedPiece, destinationSquare, castle_rook, castle_rook_start, castle_rook_destination) -> None:
        super().__init__(board, movedPiece, destinationSquare)
        self.castle_rook = castle_rook
        self.castle_rook_start = castle_rook_start
        self.castle_rook_destination = castle_rook_destination

    def get_castle_rook(self):
        return self.castle_rook
    
    def is_castling_move(self):
        return True
    
    def execute(self):

        from chessengine.players.black_player import BlackPlayer
        from chessengine.players.white_player import WhitePlayer
        from chessengine.chessboard.alliance import Alliance
        from chessengine.pieces.rook import Rook
        from chessengine.chessboard.board import Board
        '''
        When a move is executed, the current board is not mutated. Instead, a new board is created
        '''

        builder = Board.Builder()
        for piece in self.board.get_current_player().get_active_pieces():
            
            if not self.movedPiece == piece and not self.castle_rook == piece:
                builder.set_piece(piece)
   
        for piece in self.board.get_current_player().get_opponent().get_active_pieces():
            builder.set_piece(piece)

        if self.movedPiece.get_piece_alliance() == Alliance.WHITE:
            builder.set_castling_rights(False, False, self.board.black_can_castle_kingside, self.board.black_can_castle_queenside)
        else:
            builder.set_castling_rights(self.board.white_can_castle_kingside, self.board.white_can_castle_queenside, False, False)

        builder.set_piece(self.movedPiece.move_piece(self)) 
        rook = Rook(self.castle_rook_destination, self.castle_rook.get_piece_alliance())
        builder.set_piece(rook)
        rook.is_first_move = False
        builder.set_move_maker(self.board.get_current_player().get_opponent().get_alliance())

        if self.board.get_current_player().get_alliance() == Alliance.BLACK:
            builder.set_fullmove_counter(self.board.get_fullmove_counter() + 1)
        else:
            builder.set_fullmove_counter(self.board.get_fullmove_counter())
        new_board = builder.build()
        return new_board


class KingSideCastleMove(CastleMove):
    def __init__(self, board, movedPiece, destinationSquare, castle_rook, castle_rook_start, castle_rook_destination) -> None:
        super().__init__(board, movedPiece, destinationSquare, castle_rook, castle_rook_start, castle_rook_destination)

    def __str__(self) -> str:
        return "O-O"


class QueenSideCastleMove(CastleMove):
    def __init__(self, board, movedPiece, destinationSquare, castle_rook, castle_rook_start, castle_rook_destination) -> None:
        super().__init__(board, movedPiece, destinationSquare, castle_rook, castle_rook_start, castle_rook_destination)

    def __str__(self) -> str:
        return "O-O-O"


class NoneMove(Move):
    def __init__(self):
        super().__init__(None, None, -1)

    def execute(self):
        raise RuntimeError("Cannot execute")



class MoveFactory:
    def __init__(self):
        return RuntimeError
    
    @staticmethod
    def create_move(board, current_coordinate, destination_coordinate):

        for move in board.get_all_legal_moves():
            if move.get_current_coordinate() == current_coordinate and move.get_destination_coordinate() == destination_coordinate:
                return move
        
        return NoneMove()
    
