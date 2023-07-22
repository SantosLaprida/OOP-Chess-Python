from django.urls import path
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    # ... other paths for this app
]