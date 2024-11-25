import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect


from chessboard.board import Board
from chessboard.alliance import Alliance
from chessboard.boardutils import BoardUtils
from chessboard.notation import Notation
from chessboard.move import Move, MoveFactory, NoneMove
from players.move_transition import MoveTransition


def initial_board(request):

    board_data = {}

    board = Board.create_standard_board()

    for piece in board.get_white_pieces() + board.get_black_pieces():
        piece_type = piece.get_piece_type().value
        alliance = 'WHITE' if piece.get_piece_alliance() == Alliance.WHITE else 'BLACK'
        board_data[piece.get_piece_position()] = [piece_type, alliance]

    return JsonResponse(board_data)



#*******************************************************************************
# WHAT PARAMETERS DO I NEED FROM THE FRONTEND?
def initial_board_fen(request):

    board = Board.create_standard_board()
    board_data = BoardUtils.generate_fen(board);

    return JsonResponse({'fen': board_data})

#*******************************************************************************

# @ csrf_protect
# def get_legal_moves(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             source_square = data.get('from')
#             destination_square = data.get('to')
#             fen = data.get('fen')
#             board = BoardUtils.fen_to_board(fen)
#             if not board.get_square(source_square).is_square_occupied():
#                 return []
#             else:
#                 return board.get_square().get_piece().get
#             pass
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_protect
def make_move(request):
    if request.method == "POST":
        try:
            # Get move data from the request body
            data = json.loads(request.body)
            source_square = data.get('from')
            destination_square = data.get('to')
            fen = data.get('fen')
            
            if not (source_square and destination_square and fen):
                return JsonResponse({'status': 'error', 'message': 'Missing move data'}, status=400)

            fen = data.get('fen')
            board = BoardUtils.fen_to_board(fen)

            move = MoveFactory.create_move(board, source_square, destination_square)

            # active_player = board.get_current_player()

            # print(f"Active player is {active_player}")

            # moves = board.get_current_player().get_legal_moves()
            # print(f"Moves for active player are {moves}")

            if isinstance(move, NoneMove):
                return JsonResponse({'status': 'error', 'message': 'Invalid move'}, status=400)
            
            # Execute the move
            move_transition = board.get_current_player().make_move(move)

            if move_transition.status == MoveTransition.MoveStatus.DONE:
                # THIS MEANS THAT THE MOVE WAS LEGAL AND VALID
                updated_board = move_transition.get_transition_board()
                new_fen = BoardUtils.generate_fen(updated_board)
                return JsonResponse({'status': 'success', 'fen': new_fen})
            else:
                return JsonResponse({'status': 'error', 'message': 'Move could not be completed'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

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



