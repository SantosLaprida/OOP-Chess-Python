import pytest
from players.player import Player
from players.white_player import WhitePlayer
from chessboard.board import Board

def test_white_player_initialization():
    board = Board.create_standard_board()
    white_player = board.white_player
    
    
    legal_moves = white_player.get_legal_moves()
    opponent_moves = white_player.get_opponent_moves()
    
    
    white_player.calculate_king_castles(legal_moves, opponent_moves)
    
    
    assert not white_player.is_in_check()

