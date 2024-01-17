from django.urls import path
from .views import home_view, initial_board, check_highlight


urlpatterns = [
    path('', home_view, name='home'),
    path('initial-board/', initial_board, name='initial_board'),
    path('check-highlight/', check_highlight, name='check_highlight'),
    # ... other paths for this app
]