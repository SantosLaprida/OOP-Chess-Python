from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


from chessboard.board import Board
from chessboard.alliance import Alliance


def initial_board(request):

    board = Board.create_standard_board()

    board_data = {}

    for piece in board.get_white_pieces() + board.get_black_pieces():
        piece_type = piece.get_piece_type().value
        alliance = 'WHITE' if piece.get_piece_alliance() == Alliance.WHITE else 'BLACK'
        board_data[piece.get_piece_position()] = [piece_type, alliance]

    return JsonResponse(board_data)
        

def home_view(request):
    print("Home view called")
    context = {
        "range_64": range(64)  # This creates a list [0, 1, 2, ..., 63]
    }
    return render(request, 'chessgame/home.html', context)


# Create your views here.
