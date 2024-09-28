"""
WSGI config for coreGame project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import asyncio
import websockets

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreGame.settings')

application = get_wsgi_application()

async def echo(websocket, path):
    async for message in websocket:
        print(f"Recebido: {message}")
        # Aqui você pode usar os modelos do Django
        articles = Article.objects.all()  # Exemplo de consulta
        await websocket.send(f"Você disse: {message}. Total de artigos: {articles.count()}")

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("Servidor WebSocket está rodando na porta 8765...")
asyncio.get_event_loop().run_forever()
