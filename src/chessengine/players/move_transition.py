from enum import Enum


class MoveTransition():
    '''
    Represents the transition from one board to another when a move is executed
    '''
    def __init__(self, transition_board, move, move_status) -> None:
        self.transition_board = transition_board
        self.move = move
        self.move_status = move_status

    def is_done(self):
        return self.move_status == self.MoveStatus.DONE

    @property
    def status(self):
        return self.move_status
    
    def get_transition_board(self):
        return self.transition_board
    

    class MoveStatus(Enum):
        DONE = "DONE"
        ILLEGAL_MOVE = "ILLEGAL_MOVE"
        LEAVES_PLAYER_IN_CHECK = "LEAVES_PLAYER_IN_CHECK"

