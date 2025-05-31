from enum import Enum

from .boardutils import BoardUtils
from .boardutils import NUM_SQUARES
from .boardutils import NUM_SQUARES_ROW


class Column(Enum):        
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8

class Notation():
    '''
    Utility class for notation simplification
    '''

    columns = [
        [i % NUM_SQUARES_ROW == 0 for i in range(NUM_SQUARES)],
        [i % NUM_SQUARES_ROW == 1 for i in range(NUM_SQUARES)],
        [i % NUM_SQUARES_ROW == 2 for i in range(NUM_SQUARES)],
        [i % NUM_SQUARES_ROW == 3 for i in range(NUM_SQUARES)],
        [i % NUM_SQUARES_ROW == 4 for i in range(NUM_SQUARES)],
        [i % NUM_SQUARES_ROW == 5 for i in range(NUM_SQUARES)],
        [i % NUM_SQUARES_ROW == 6 for i in range(NUM_SQUARES)],
        [i % NUM_SQUARES_ROW == 7 for i in range(NUM_SQUARES)]
    ]
    
    notation_dict = {}

    @staticmethod
    def generate_dictionary():
        for i in range(len(Notation.columns)):
            Notation.notation_dict[Column(i + 1).name] = [j for j, value in enumerate(Notation.columns[i]) if value]

    @staticmethod
    def coordinate_to_notation(coordinate):

        '''
        Static method that returns a string, first character is column and second character is row
        '''

        for key in Notation.notation_dict:
            if coordinate in Notation.notation_dict[key]:

                for i, value in enumerate(reversed(Notation.notation_dict[key])):

                    if coordinate == value:
                        return str(key) + str(i + 1)
                

        return None

    @staticmethod
    def notation_to_coordinate(notation):
        '''
        Static method that returns a coordinate, given a chess board notation
        '''
        for key in Notation.notation_dict:
            if key == str(notation[0]):
                for i, value in enumerate(reversed(Notation.notation_dict[key])):
                    
                    if i + 1 == int(notation[1]):
                        return int(list(reversed(Notation.notation_dict[key]))[i])


        return None


Notation.generate_dictionary()  # Generate the dictionary


   
