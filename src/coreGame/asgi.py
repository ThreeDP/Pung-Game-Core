"""
ASGI config for coreGame project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from game.routing import websocket_urlpatterns
from game.consumers import BasePlayer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreGame.settings')

player_one = BasePlayer(0, 200, 5)
player_two = BasePlayer(0, 200, 370)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        websocket_urlpatterns
    ),
})