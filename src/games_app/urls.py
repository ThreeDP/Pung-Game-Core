from django.urls import path
from .views.games_view import GameView

urlpatterns = [
    path('ranking/', GameView.as_view(), name='game')
]
