
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.king import King
from pieces.queen import Queen
from pieces.knight import Knight
from pieces.pawn import Pawn
from .boardutils import BoardUtils, NUM_SQUARES
from .notation import Notation


class Board:
    '''
    The class represents the game board.

    Attributes:
        game_board (list): The list of squares on the board.
        current_player: 

    '''

    def __init__(self, builder) -> None:
        
        from players.white_player import WhitePlayer
        from players.black_player import BlackPlayer
        from .alliance import Alliance
        from pieces.piece import Piece

        self.game_board = self.create_game_board(builder)
        self.active_white_pieces = self.calculate_active_pieces(self.game_board, Alliance.WHITE)
        self.active_black_pieces = self.calculate_active_pieces(self.game_board, Alliance.BLACK)

        self.white_can_castle_kingside = builder.white_can_castle_kingside
        self.white_can_castle_queenside = builder.white_can_castle_queenside
        self.black_can_castle_kingside = builder.black_can_castle_kingside
        self.black_can_castle_queenside = builder.black_can_castle_queenside
        
        self.en_passant_target = builder.en_passant_target
        self.en_passant = builder.en_passant
        self.fullmove_counter = builder.fullmove_counter

        # Initializing the player objects before using them
        self.white_player = WhitePlayer(self)
        self.black_player = BlackPlayer(self)

        self.current_player = Alliance.choose_player(builder.next_move_maker, self.white_player, self.black_player)
        
        self.white_legal_moves = self.calculate_legal_moves(self.active_white_pieces)
        self.black_legal_moves = self.calculate_legal_moves(self.active_black_pieces)

        self.black_player.set_legal_moves(self.black_legal_moves)
        self.black_player.set_opponent_moves(self.white_legal_moves)

        self.white_player.set_legal_moves(self.white_legal_moves)
        self.white_player.set_opponent_moves(self.black_legal_moves)

        
        

    @staticmethod
    def create_game_board(builder):
        from .square import Square
        '''
        Creates the squares on the board using the builder configuration.

        :param builder: The board builder.
        :type builder: Builder
        :return: The list of squares on the board.
        :rtype: list
        '''
        
        squares = [Square.create_square(i, builder.board_configuration.get(i)) for i in range(NUM_SQUARES)]

        return squares
    
    def get_castling_rights(self):
        string = ""
        if self.white_can_castle_kingside:
            string += "K"
        if self.white_can_castle_queenside:
            string += "Q"
        if self.black_can_castle_kingside:
            string += "k"
        if self.black_can_castle_queenside:
            string += "q"

        if string == "":
            string = "-"

        return string

    def get_fullmove_counter(self):
        return self.fullmove_counter

    def get_current_player(self):
        return self.current_player

    def white_player(self):
        return self.white_player
    
    def black_player(self):
        return self.black_player

    def get_black_pieces(self):
        return self.active_black_pieces
    
    def get_white_pieces(self):
        return self.active_white_pieces

    def calculate_legal_moves(self, pieces):
        from pieces.piece import Piece

        legal_moves = []

        for piece in pieces:

            legal_moves.extend(piece.calculate_legal_moves(self))

        return legal_moves
    
    def get_all_legal_moves(self):

        white_legals = self.white_legal_moves
        black_legals = self.black_legal_moves

        return white_legals + black_legals
    
    
    @staticmethod
    def calculate_active_pieces(game_board, alliance):
        from pieces.piece import Piece
        '''
        Calculates the white or black pieces on a chessboard.
        :param: board, alliance (white or black pieces to return)
        :return: list of active pieces on the board (white or black)
        :rtype: list
        '''
        

        active_pieces = [square.get_piece() for square in game_board if square.is_square_occupied() and square.get_piece().get_piece_alliance() == alliance]
       

        return active_pieces
    
    @staticmethod
    def create_standard_board():
        from pieces.piece import Piece
        from .alliance import Alliance
        '''
        Using the builder class, this method creates the intial position of a chess board
        '''
        builder = Board.Builder()

        #Black layout

        builder.set_piece(Rook(0, Alliance.BLACK))
        builder.set_piece(Knight(1, Alliance.BLACK))
        builder.set_piece(Bishop(2, Alliance.BLACK))
        builder.set_piece(Queen(3, Alliance.BLACK))
        builder.set_piece(King(4, Alliance.BLACK))
        builder.set_piece(Bishop(5, Alliance.BLACK))
        builder.set_piece(Knight(6, Alliance.BLACK))
        builder.set_piece(Rook(7, Alliance.BLACK))
        
        for i in range(8, 16):
            builder.set_piece(Pawn(i, Alliance.BLACK))

        # White layout

        for i in range(48, 56):
            builder.set_piece(Pawn(i, Alliance.WHITE))

        builder.set_piece(Rook(56, Alliance.WHITE))
        builder.set_piece(Knight(57, Alliance.WHITE))
        builder.set_piece(Bishop(58, Alliance.WHITE))
        builder.set_piece(Queen(59, Alliance.WHITE))
        builder.set_piece(King(60, Alliance.WHITE))
        builder.set_piece(Bishop(61, Alliance.WHITE))
        builder.set_piece(Knight(62, Alliance.WHITE))
        builder.set_piece(Rook(63, Alliance.WHITE))

        # Set the initial player to be White
        builder.set_move_maker(Alliance.WHITE)
        builder.set_fullmove_counter(1)

        return builder.build()
        

    def get_square(self, coordinate): 
        '''
        Returns the square object at the given coordinate on the board.
        '''

        if isinstance(coordinate, str):
            coordinate = Notation.notation_to_coordinate(coordinate)

        square = self.game_board[coordinate]
        
        return square
    
    def get_en_passant(self):
        """
        Returns the en passant target square if it exists, otherwise returns None.
        """
        return self.en_passant
    
    def get_en_passant_target(self):
        return self.en_passant_target


    def __str__(self) -> str:
        board_str = ''
        for i in range(NUM_SQUARES):
            if i % 8 == 0 and i != 0:
                board_str += '\n'
            square = self.game_board[i]
            if square.is_square_occupied():
                board_str += str(square.get_piece()) + ' '
            else:
                board_str += '- '
        return board_str

    
    class Builder():
        
        '''
        The builder class for the Board.
        
        Attributes:
            board_configuration (dict): The piece configuration on the board.
            next_move_maker (Alliance): The alliance of the next move maker.
        '''
        def __init__(self) -> None:
            from .alliance import Alliance
            self.board_configuration = {} # Key is int and value is Piece 
            self.next_move_maker = Alliance
            self.en_passant = None # The pawn that can be captured en passant
            self.en_passant_target = "-" # The target square for en passant
            self.fullmove_counter = 1

            # Castling rights
            self.white_can_castle_kingside = True
            self.white_can_castle_queenside = True
            self.black_can_castle_kingside = True
            self.black_can_castle_queenside = True

        def set_piece(self, piece):
            from pieces.piece import Piece
            '''
            Sets a piece on the board.
            '''
            self.board_configuration[piece.get_piece_position()] = piece
            return self
        
        def set_move_maker(self, next_move_maker):
            '''
            Sets the alliance of the next move maker.
            '''
            self.next_move_maker = next_move_maker
            return self
        
        def set_castling_rights(self, white_kingside, white_queenside, black_kingside, black_queenside):
            '''
            Sets the castling rights for the board.
            '''
            self.white_can_castle_kingside = white_kingside
            self.white_can_castle_queenside = white_queenside
            self.black_can_castle_kingside = black_kingside
            self.black_can_castle_queenside = black_queenside
            return self
        
        def set_en_passant_pawn(self, pawn):

            from .alliance import Alliance

            if pawn.get_piece_alliance() == Alliance.WHITE:
                self.en_passant_target = pawn.get_piece_position() + 8
            else:
                self.en_passant_target = pawn.get_piece_position() - 8
            self.en_passant = pawn

        def set_fullmove_counter(self, counter):
            self.fullmove_counter = counter
            return self
        
        def build(self):
            '''
            Constructs a Board object using the builder configuration.
            '''
            return Board(self)
        
        
