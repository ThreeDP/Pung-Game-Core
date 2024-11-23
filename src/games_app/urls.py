from django.urls import path
from .views.games_view import GameView

urlpatterns = [
    path('', GameView.as_view(), name='game')
]
