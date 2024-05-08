



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
    def generate_fen(board):

        from .alliance import Alliance
        from .board import Board

        '''
        Generates a FEN string from board object
        '''

        fen = ""
        empty_squares = 0

        for i in range(NUM_SQUARES):
            
            if board.get_square(i).is_square_occupied():
                    fen += str(board.get_square(i))

                    # Update empty_squares to 0
                    empty_squares = 0

            else:

                if i == NUM_SQUARES:
                    pass
               
                elif board.get_square(i + 1).is_square_occupied() or BoardUtils.EIGHT_COLUMN[i]:
                    empty_squares += 1
                    fen += str(empty_squares)

                # If the square is not occupied, we update empty_squares
                empty_squares += 1
                
            if BoardUtils.EIGHT_COLUMN[i] == True:

                if i == NUM_SQUARES - 1:
                    pass

                else:
                    empty_squares = 0 
                    fen += "/" 

        if board.get_current_player().get_alliance() == Alliance.BLACK:
            fen += " b"
        else:
            fen += " w"

        for i in range(4):
            fen += ' -'

            
        return fen

                

            

            

            