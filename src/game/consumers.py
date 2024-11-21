# import asyncio
# import json
# import random
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from collections import deque

# # Constantes do jogo
# PADDLE_SPEED = 10
# BALL_SPEED = 5  # A velocidade da bola (ajuste conforme necessário)
# GAME_WIDTH = 850  # Largura da área de jogo
# GAME_HEIGHT = 550  # Altura da área de jogo

# # Estado do jogo
# class Player:
#     def __init__(self, player_id, x, y):
#         self.id = player_id
#         self.x = x
#         self.y = y
#         self.width = 25
#         self.height = 100
#         self.is_connected = False
#         self.ws = None
#         self.score = 0

#     def move(self, direction):
#         new_y = self.y + direction
#         if 0 <= new_y <= GAME_HEIGHT - self.height:  # Previne o movimento para fora da tela
#             self.y = new_y
    
#     def to_dict(self):
#         return {
#             "x": self.x,
#             "y": self.y,
#             "width": self.width,
#             "height": self.height,
#         }

# class Ball:
#     def __init__(self):
#         self.x = 275
#         self.y = 275
#         self.radius = 10.0

#     def to_dict(self):
#         return {
#             "x": self.x,
#             "y": self.y,
#             "radius": self.radius,
#         }

# player_one = Player(0, 25, 225)
# player_two = Player(1, 800, 225)
# ball = Ball()

# movement_map = {
#     'ArrowUp': -PADDLE_SPEED,
#     'ArrowDown': PADDLE_SPEED,
#     'w': -PADDLE_SPEED,
#     's': PADDLE_SPEED
# }

# MapPositions = [
#     {"x": 25, "y": 225},
#     {"x": 800, "y": 225},
# ]

# class GameSession:
#     def __init__(self, userIds):
#         self.players = {}
#         for index, userId in enumerate(userIds):
#             position = MapPositions[index]
#             self.players[userId] = Player(userId, position["x"], position["y"])
        
#         self.ball = ball
#         self.ball_direction = {
#             "x": random.choice([-BALL_SPEED, BALL_SPEED]),
#             "y": random.choice([-BALL_SPEED, BALL_SPEED])
#         }  # Lista de clientes conectados

#     async def update_ball_position(self):
#         # Atualizar a posição da bola
#         self.ball.x += self.ball_direction["x"]
#         self.ball.y += self.ball_direction["y"]

#         # Verificar colisão com as paredes superior e inferior
#         if self.ball.y <= 0 or self.ball.y >= GAME_HEIGHT:
#             self.ball_direction["y"] *= -1  # Inverter a direção no eixo Y

#         # Verificar colisão com os jogadores
#         for player in self.players:
#             if player.x <= self.ball.x <= player.x + player.width:
#                 if player.y <= self.ball.y <= player.y + player.height:
#                     self.ball_direction["x"] *= -1  # Inverter a direção no eixo X

#         # Verificar se a bola saiu da tela
#         if self.ball.x <= 0 or self.ball.x >= GAME_WIDTH:
#             self.ball.x = GAME_WIDTH // 2  # Resetar a bola para o centro
#             self.ball.y = GAME_HEIGHT // 2  # Resetar a posição Y para o centro
#             self.ball_direction = {
#                 "x": random.choice([-BALL_SPEED, BALL_SPEED]),
#                 "y": random.choice([-BALL_SPEED, BALL_SPEED])
#             }

#     async def notify_clients(self):
#         # Enviar as atualizações para todos os clientes conectados
#         response_data = {
#             "player_one": players[0].to_dict(),
#             "ball": self.ball.to_dict(),
#             "player_two": players[1].to_dict(),
#         }
#         response_json = json.dumps(response_data)

#         # Enviar os dados para todos os clientes
#         for client in self.clients:
#             await client.send(text_data=response_json)

#     async def game_loop(self):
#         while True:
#             await self.update_ball_position()
#             await self.notify_clients()
#             await asyncio.sleep(0.02)  # Atualizar a cada 0.02 segundos (50fps)

# # Instância global do estado do jogo
# game_state = GameSession([0, 1])

# class http_consumer(AsyncWebsocketConsumer):
#     game_sessions = {}

#     async def connect(self):
#         headers = dict(self.scope['headers'])
#         userId = headers[b'X-User-Id'].decode('utf-8')
#         gameId = headers[b'X-Game-Id'].decode('utf-8')

#         session = self.game_sessions.get(gameId)

#         player = session.players.filter(id=userId).first()
#         if player is None:
#             self.close()
#             return
#         player.update(is_connected=True)
#         player.update(ws=self)
#         await self.accept()

#         # Inicia o loop do jogo se for o primeiro cliente
#         if len(session.players.filter(is_connected=True)) == 2:
#             asyncio.create_task(session.game_loop())

#     async def disconnect(self, close_code):
#         # Verificar se existe algum evento na fila para criar a game_session
#         redis = await aioredis.create_redis_pool('redis://localhost')
#         event = await redis.lpop('game_session_queue')
#         if event:
#             event_data = json.loads(event)
#             gameId = event_data['gameId']
#             userIds = event_data['userIds']
#             self.game_sessions[gameId] = GameSession(userIds)
        
#         headers = dict(self.scope['headers'])
#         userId = headers[b'X-User-Id'].decode('utf-8')
#         gameId = headers[b'X-Game-Id'].decode('utf-8')

#         session = self.game_sessions.get(gameId)
#         session.players.remove(ws=self)

#     async def receive(self, text_data):
#         message = text_data

#         if message in movement_map:
#             if message in ['ArrowUp', 'ArrowDown']:
#                 player_two.move(movement_map[message])
#             else:
#                 player_one.move(movement_map[message])

#         # Não envia nada individualmente, pois a bola e os jogadores são atualizados periodicamente


import logging
import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from .models import Game, Player, Score
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

class GameSessionConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        headers = dict(self.scope['headers'])
        self.gameId = self.scope['url_route']['kwargs']['game_id']
        self.userId = headers.get(b'X-User-Id', b'1').decode('utf-8')
        self.game_channel = f"game_session_{self.gameId}"
        self.player_channel = f"{self.game_channel}_{self.userId}"

        logger.info(f"User {self.userId} trying to connect to game {self.gameId}")

        game = await sync_to_async(Game.objects.filter(id=self.gameId).first)()
        if game is None:
            logger.info(f"User {self.userId} disconnected from game {self.gameId} - Game not found")
            await self.close()
            return

        user = await sync_to_async(Player.objects.filter(gameId=self.gameId, id=self.userId).first)()
        if user is None:
            logger.info(f"User {self.userId} disconnected from game {self.gameId} - User not found")
            await self.close(code="204")
            return

        user.is_connected = True
        await sync_to_async(user.save)()

        await self.channel_layer.group_add(
            self.game_channel, 
            self.channel_name)
        await self.channel_layer.group_add(
            "game_session_1234_1", 
            "consumer")
        
        logger.info(f"User {self.userId} connected to game {self.gameId}")
        await self.accept()

    async def disconnect(self, close_code):
        #headers = dict(self.scope['headers'])
        #self.userId = headers.get(b'x-user-id', b'1').decode('utf-8')

        user = await sync_to_async(Player.objects.filter(gameId=self.gameId, id=self.userId).first)()
        if user:
            user.is_connected = False
            user.save()

        await self.channel_layer.group_discard(
            self.game_channel,
            self.channel_name)
        await self.channel_layer.group_discard(
            "game_session_1234_1", 
            "game_worker")

    async def receive(self, text_data):
        #headers = dict(self.scope['headers'])
        #self.userId = headers.get(b'x-user-id', b'1').decode('utf-8')
        
        data = json.loads(text_data)
        direction = data.get('direction')
        
        if direction in ["w", "s"]:
            move = {
                "userId": self.userId,
                "direction": -5 if direction == "w" else 5
            }
            logger.info(f"User {self.userId} moved to {move['direction']}")
            channel = get_channel_layer()
            await channel.group_send(
                "game_session_1234_1",
                {
                    "type": "player.move",
                    "move": move
                }
            )
            logger.info(f"Finished User {self.userId} moved to {move['direction']} - {self.player_channel}")

    async def player_move(self, event):
        move = event['move']
        logger.info(f"Sending move: {move}")
        await self.send(text_data=json.dumps(move))

    async def game_update(self, event):
        game_state = event['game_state']
        #logger.info(f"Game state: {game_state}")
        await self.send(text_data=json.dumps(game_state))