from django.urls import path
from game.consumers import  GameSessionConsumer

websocket_urlpatterns = [
    #path('api/v1/game-core/', http_consumer.as_asgi()),
    path('api/v1/game-core/<str:game_id>/', GameSessionConsumer.as_asgi()),
]