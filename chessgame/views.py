import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect


from chessengine.chessboard.board import Board
from chessengine.chessboard.alliance import Alliance
from chessengine.chessboard.boardutils import BoardUtils
from chessengine.chessboard.notation import Notation
from chessengine.chessboard.move import Move, MoveFactory, NoneMove
from chessengine.players.move_transition import MoveTransition


def initial_board(request):

    board_data = {}

    board = Board.create_standard_board()

    for piece in board.get_white_pieces() + board.get_black_pieces():
        piece_type = piece.get_piece_type().value
        alliance = 'WHITE' if piece.get_piece_alliance() == Alliance.WHITE else 'BLACK'
        board_data[piece.get_piece_position()] = [piece_type, alliance]

    return JsonResponse(board_data)


def initial_board_fen(request):

    board = Board.create_standard_board()
    board_data = BoardUtils.generate_fen(board);

    return JsonResponse({'fen': board_data})

#*******************************************************************************

def get_legal_moves(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            fen = data.get('fen')
            source_square = data.get('sourceSquare')

            if source_square is None or fen is None:
                return JsonResponse({'status': 'error', 'message': 'Missing data to get legal moves'}, status=400)

            board = BoardUtils.fen_to_board(fen)

            current_player = board.get_current_player().get_alliance()
            square = board.get_square(source_square)

            if not square.is_square_occupied():
                return JsonResponse({'status': 'error', 'message': 'Square does not have a piece'}, status=400)

            piece = square.get_piece()
            piece_color = piece.get_piece_alliance()
            pinned_pieces = board.get_pinned_pieces(board.get_current_player().get_opponent().get_active_pieces())
            print(f"Pinned pieces: {pinned_pieces}")

            if piece in pinned_pieces:
                return JsonResponse({'status': 'success', 'destinations': []})

            if piece_color != current_player:
                return JsonResponse({'status': 'error', 'message': 'Piece color does not match player color'}, status=400)
            
            legal_moves = piece.calculate_legal_moves(board)
            destinations, count = {}, 0
            if board.get_current_player().is_in_check:
                for move in board.get_legal_moves_when_in_check():
                    source = move.get_current_coordinate()
                    destination = move.get_destination_coordinate()
                    for m in legal_moves:
                        s, d = m.get_current_coordinate(), m.get_destination_coordinate()
                        if s == source and d == destination:
                            destinations[destination] = count
                            count += 1
                            # break
                    # destinations[destination] = count
                    # count += 1
                print(destinations)
                return JsonResponse({'status': 'success', 'destinations': destinations})

            for move in legal_moves:
                destination = move.get_destination_coordinate()
                destinations[destination] = count
                count += 1

            return JsonResponse({'status': 'success', 'destinations': destinations})



        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_protect
def make_move(request):
    if request.method == "POST":
        try:
            # Get move data from the request body
            data = json.loads(request.body)
            source_square = data.get('from')
            destination_square = data.get('to')
            fen = data.get('fen')

            if source_square is None or destination_square is None or fen is None:
                return JsonResponse({'status': 'error', 'message': 'Missing move data'}, status=400)

            board = BoardUtils.fen_to_board(fen)

            move = MoveFactory.create_move(board, source_square, destination_square)

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
    print("Checking highlight")
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


def get_all_legal_moves(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            fen = data.get('fen')

            if not fen:
                return JsonResponse({'status': 'error', 'message': 'Missing FEN data'}, status=400)

            board = BoardUtils.fen_to_board(fen)
            
            try:
                moves = {}
                current_player = board.get_current_player()
                active_pieces = Board.calculate_active_pieces(board.game_board, current_player.get_alliance())

                for piece in active_pieces:
                    square_coordinate = piece.get_piece_position()
                    legal_moves = [str(move) for move in piece.calculate_legal_moves(board)]
                    moves[square_coordinate] = {
                                                "piece": str(piece),
                                                "moves": legal_moves
                                            }

                return JsonResponse({'status': 'success', 'fen': moves})

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': 'Error calculating pieces'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def home_view(request):
    print("Home view called")
    context = {
        "range_64": range(64)  # This creates a list [0, 1, 2, ..., 63]
    }
    return render(request, 'chessgame/home.html', context)



