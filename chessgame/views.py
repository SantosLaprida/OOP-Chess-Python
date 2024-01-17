import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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



@csrf_exempt
def check_highlight(request):
    if request.method == "POST":
        data = json.loads(request.body)
        source_square = data['sourceSquare']
        board = data['board']

        # Logic to determine if the square should be highlighted
        should_highlight = False
        
        if board.get_square(source_square).is_square_occupied():
            piece = board.get_square(source_square).get_piece()
            if piece.get_piece_alliance() == board.get_current_player().get_alliance():
                
                should_highlight = True

        return JsonResponse({'shouldHighlight': should_highlight})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        


def handle_move(request):

    ########################################################################
    ########################################################################
    ########################################################################

    # TODO: Validate move AND FINISH JS FILE


    if request.method == 'POST':
        move_data = request.POST
        source_square = move_data['sourceSquare']
        destination_square = move_data['destinationSquare']
        board_state = move_data['board']

        import json
        try:
            board = json.loads(board_state)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid board data'}, status=400)
        
        # Validate move

        return JsonResponse({'status': 'success', 'message': 'Move processed'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        
    ########################################################################
    ########################################################################
    ########################################################################

def home_view(request):
    print("Home view called")
    context = {
        "range_64": range(64)  # This creates a list [0, 1, 2, ..., 63]
    }
    return render(request, 'chessgame/home.html', context)


# Create your views here.
