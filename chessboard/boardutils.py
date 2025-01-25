
NUM_SQUARES = 64
NUM_SQUARES_ROW = 8
COLUMNS = ["A","B","C","D","E","F","G","H"]

class BoardUtils():
    """
    Utility class
    """

    FIRST_COLUMN = [i % NUM_SQUARES_ROW == 0 for i in range(NUM_SQUARES)]
    SECOND_COLUMN = [i % NUM_SQUARES_ROW == 1 for i in range(NUM_SQUARES)]
    THIRD_COLUMN = [i % NUM_SQUARES_ROW == 2 for i in range(NUM_SQUARES)]
    FOURTH_COLUMN = [i % NUM_SQUARES_ROW == 3 for i in range(NUM_SQUARES)]
    FIFTH_COLUMN = [i % NUM_SQUARES_ROW == 4 for i in range(NUM_SQUARES)]
    SIXTH_COLUMN = [i % NUM_SQUARES_ROW == 5 for i in range(NUM_SQUARES)]
    SEVENTH_COLUMN = [i % NUM_SQUARES_ROW == 6 for i in range(NUM_SQUARES)]
    EIGHT_COLUMN = [i % NUM_SQUARES_ROW == 7 for i in range(NUM_SQUARES)]

    SECOND_ROW = [i >= 8 and i <= 15 for i in range(NUM_SQUARES)]
    SEVENTH_ROW = [i >= 48 and i <= 55 for i in range(NUM_SQUARES)]

    
    @staticmethod
    def isSquareValid(coordinate) -> bool:
        '''
        returns true if coordinate is between 0 and 64 (NUM_SQUARES)
        '''
        return coordinate >= 0 and coordinate < NUM_SQUARES
    
    @staticmethod
    def get_en_passant_offsets(coordinate, piece_alliance):
        '''
        Returns the en passant offsets (Coordinates) that a pawn must be in to perform en passant
        '''
        from .alliance import Alliance

        en_passant_offsets = set()
        
        if piece_alliance == Alliance.WHITE:
            if not BoardUtils.EIGHT_COLUMN[coordinate]:  # Not in the 8th column
                en_passant_offsets.add(coordinate - 9)
            if not BoardUtils.FIRST_COLUMN[coordinate]:  # Not in the 1st column
                en_passant_offsets.add(coordinate - 7)
        else:  # Alliance.BLACK
            if not BoardUtils.FIRST_COLUMN[coordinate]:  # Not in the 1st column
                en_passant_offsets.add(coordinate + 9)
            if not BoardUtils.EIGHT_COLUMN[coordinate]:  # Not in the 8th column
                en_passant_offsets.add(coordinate + 7)
        
        return en_passant_offsets


    
    @staticmethod
    def generate_fen(board):

        from .alliance import Alliance
        from .board import Board
        from .notation import Notation

        '''
        Generates a FEN string from board object
        '''

        fen = ""
        empty_squares = 0

        for i in range(NUM_SQUARES):
            if board.get_square(i).is_square_occupied():
                # If we have any accumulated empty squares, add them to the FEN
                if empty_squares > 0:
                    fen += str(empty_squares)
                    empty_squares = 0

                piece = board.get_square(i).get_piece()
                piece_char = piece.get_piece_type().value
                if piece.get_piece_alliance() == Alliance.WHITE:
                    fen += piece_char.upper()
                else:
                    fen += piece_char.lower()
            else:
                # Count empty squares
                empty_squares += 1

            # At the end of each row, append the empty square count if any and add a slash
            if BoardUtils.EIGHT_COLUMN[i]:
                if empty_squares > 0:
                    fen += str(empty_squares)
                    empty_squares = 0
                if i != NUM_SQUARES - 1:

                    fen += "/"

        # Add the active player
        fen += " " + ('w' if board.get_current_player().get_alliance() == Alliance.WHITE else 'b') + " "

        # Add castling rights
        fen += board.get_castling_rights() + " "

        # Add en passant target square
        passant = board.get_en_passant_target()
        if passant == "-":
            fen += "-"
        else:
            fen += Notation.coordinate_to_notation(passant)
        
        # Add halfmove clock, for now 0 until we implement it TODO
        fen += " 0"

        # Add fullmove number
        fen += f" {board.get_fullmove_counter()}"


        return fen

                
    def fen_to_board(fen):
        from .alliance import Alliance
        from .board import Board, Notation
        from pieces.rook import Rook
        from pieces.bishop import Bishop
        from pieces.king import King
        from pieces.queen import Queen
        from pieces.knight import Knight
        from pieces.pawn import Pawn

        # Split the FEN into its components
        try:
            fen_parts = fen.split()
            piece_positions = fen_parts[0]
            active_color = fen_parts[1]
            castling_rights = fen_parts[2]
            en_passant_target = fen_parts[3]
            halfmove_clock = fen_parts[4]
            fullmove_counter = fen_parts[5]
        except IndexError:
            raise ValueError("Invalid FEN string: Not enough components.")

        # Initialize a Board Builder
        builder = Board.Builder()

        # Maps FEN characters to piece classes
        piece_map = {
            'p': Pawn, 'r': Rook, 'n': Knight, 'b': Bishop, 'q': Queen, 'k': King
        }

        # Convert the FEN piece placement into pieces on the board
        row = 0
        col = 0
        for char in piece_positions:
            if char == '/':
                # Move to the next row
                row += 1
                col = 0
            elif char.isdigit():
                # Empty squares; move forward by the number of squares
                col += int(char)
            else:
                is_white = char.isupper()
                piece_class = piece_map.get(char.lower())
                if piece_class is None:
                    raise ValueError(f"Invalid piece character in FEN: {char}")
                alliance = Alliance.WHITE if is_white else Alliance.BLACK
                position = row * 8 + col

                # Place the piece on the board using the builder
                builder.set_piece(piece_class(position, alliance))
                col += 1

        # Set the active player from the FEN
        if active_color == 'w':
            builder.set_move_maker(Alliance.WHITE)
        elif active_color == 'b':
            builder.set_move_maker(Alliance.BLACK)
        else:
            raise ValueError("Invalid FEN active color component; must be 'w' or 'b'.")
        
        # Set castling rights
        if castling_rights == '-':
            builder.set_castling_rights(False, False, False, False)
        else:
            white_kingside, white_queenside, black_kingside, black_queenside = False, False, False, False
            for char in castling_rights:
                if char == 'K':
                    white_kingside = True
                elif char == 'Q':
                    white_queenside = True
                elif char == 'k':
                    black_kingside = True
                elif char == 'q':
                    black_queenside = True
                else:
                    raise ValueError("Invalid FEN castling rights component.")
                
            builder.set_castling_rights(white_kingside, white_queenside, black_kingside, black_queenside)
        
        # Set en passant target square
        if en_passant_target != '-':
            en_passant_target = Notation.notation_to_coordinate(en_passant_target)
            if active_color == 'w':
                pawn = Pawn(en_passant_target - 8, Alliance.BLACK)
            else:
                pawn = Pawn(en_passant_target + 8, Alliance.WHITE)
            builder.set_en_passant_pawn(pawn)

        # Set fullmove counter
        builder.set_fullmove_counter(int(fullmove_counter))

        # Return the constructed board
        return builder.build()
            

            

            