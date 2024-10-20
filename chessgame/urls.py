from django.urls import path
from .views import home_view, initial_board, check_highlight, initial_board_fen, make_move


urlpatterns = [
    path('', home_view, name='home'),
    path('initial-board/', initial_board, name='initial_board'),
    path('initial-board-fen/', initial_board_fen, name='initial_board_fen'),
    path('make-move/', make_move, name='make_move'),
    # ... other paths for this app
]