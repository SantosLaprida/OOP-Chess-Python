from django.urls import path
from .views import home_view, initial_board


urlpatterns = [
    path('', home_view, name='home'),
    path('initial-board/', initial_board, name='initial_board'),
    # ... other paths for this app
]