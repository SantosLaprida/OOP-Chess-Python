from enum import Enum
from players.player import Player
from players.white_player import WhitePlayer
from players.black_player import BlackPlayer

class Alliance(Enum):
    WHITE = -1
    BLACK = 1

    @property
    def get_direction(self):
        """
        The direction of movement associated with an alliance. 
        
        Returns
        -------
        int
            Returns 1 for BLACK and -1 for WHITE.
        """
        direction = 1 if self == Alliance.BLACK else -1
        
        return direction
    
    @staticmethod
    def choose_player(current_alliance, white_player, black_player):
        if current_alliance == Alliance.WHITE:
            return white_player if white_player else None  # Return None if not initialized
        elif current_alliance == Alliance.BLACK:
            return black_player if black_player else None  # Return None if not initialized
        else:
            raise ValueError(f"Invalid alliance: {current_alliance}. Expected Alliance.WHITE or Alliance.BLACK.")


    def is_white(self) -> bool:
        return True if self == Alliance.WHITE else False


    def is_black(self) -> bool:
        return True if self == Alliance.BLACK else False