from django.urls import path
from .consumers import http_consumer

websocket_urlpatterns = [
    path('ws/game/', http_consumer.as_asgi()),
]

