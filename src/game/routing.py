from django.urls import path
from .consumers import http_consumer

websocket_urlpatterns = [
    path('api/v1/game-core/', http_consumer.as_asgi()),
]

