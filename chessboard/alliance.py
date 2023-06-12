from enum import Enum

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
        return 1 if self == Alliance.BLACK else -1 

    def is_white(self) -> bool:
        return True if self == Alliance.WHITE else False

    def is_black(self) -> bool:
        return True if self == Alliance.BLACK else False