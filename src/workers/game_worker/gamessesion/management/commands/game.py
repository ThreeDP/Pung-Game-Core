import json
import random
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand

# Definindo algumas constantes
GAME_WIDTH = 850
GAME_HEIGHT = 550
BALL_SPEED = 5
MapPositions = [{"x": 800, "y": 225}, {"x": 25, "y": 225}]  # Posições iniciais dos jogadores

class Player:
    def __init__(self, user_id, x, y):
        self.user_id = user_id
        self.x = x
        self.y = y
        self.width = 25
        self.height = 100

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }

class Ball:
    def __init__(self):
        self.x = GAME_WIDTH // 2
        self.y = GAME_HEIGHT // 2
        self.radius = 10

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "radius": self.radius,
        }

class GameSession():
    def __init__(self, user_ids, gameId):
        self.channel_layer = get_channel_layer()
        self.tasks_movement_player = []
        self.gameId = gameId
        self.game = f"game_session_{gameId}"
        
        self.players = {}
        for index, user_id in enumerate(user_ids):
            position = MapPositions[index]
            self.players[user_id] = Player(user_id, position["x"], position["y"])

        self.ball = Ball()
        self.ball_direction = {
            "x": random.choice([-BALL_SPEED, BALL_SPEED]),
            "y": random.choice([-BALL_SPEED, BALL_SPEED])
        }

    async def add_player_channels(self):
        for player in self.players.values():
            await self.channel_layer.group_add(
                f"{self.game}_{player.user_id}",
                "game_worker")
            self.tasks_movement_player.append(asyncio.create_task(self.process_player_move(player)))

    async def update_ball_position(self):
        # Atualizar a posição da bola
        self.ball.x += self.ball_direction["x"]
        self.ball.y += self.ball_direction["y"]

        # Verificar colisão com as paredes superior e inferior
        if self.ball.y <= 0 or self.ball.y >= GAME_HEIGHT:
            self.ball_direction["y"] *= -1  # Inverter direção no eixo Y

        # Verificar colisão com os jogadores
        for player in self.players.values():
            if player.x <= self.ball.x <= player.x + player.width:
                if player.y <= self.ball.y <= player.y + player.height:
                    self.ball_direction["x"] *= -1  # Inverter direção no eixo X

        # Verificar se a bola saiu da tela
        if self.ball.x <= 0 or self.ball.x >= GAME_WIDTH:
            self.ball.x = GAME_WIDTH // 2  # Resetar bola para o centro
            self.ball.y = GAME_HEIGHT // 2  # Resetar a posição Y para o centro
            self.ball_direction = {
                "x": random.choice([-BALL_SPEED, BALL_SPEED]),
                "y": random.choice([-BALL_SPEED, BALL_SPEED])
            }

    async def notify_clients(self):
        # Enviar atualizações para os clientes conectados
        response_data = {
            "ball": self.ball.to_dict(),
            "players": {user_id: player.to_dict() for user_id, player in self.players.items()},
        }
        response_json = json.dumps(response_data)

        # Enviar os dados para todos os clientes via canal
        await self.channel_layer.group_send(
            self.game,  # Enviar para cada jogador individualmente
            {
                "type": "game.update",  # Tipo de mensagem para o consumer
                "game_state": response_data,
            }
        )
    
    async def process_player_move(self, player):
        while True:
            await asyncio.sleep(0.02)
            # if player.user_id == "2":
            #     player.y = random.randint(0, GAME_HEIGHT - player.height)
            #     continue
            print(f"Message! {self.game}_{player.user_id}")
            message = await self.channel_layer.receive_single(f"{self.game}_{player.user_id}")
            print(f"Message: {message}")
            if message is not None:
                print(f"To aqui {message}")
                move = message.get("move", {})
                self.players[player.user_id]["y"] += move.get("direction", 0)
    
    async def player_move(self, event):
        move = event['move']
        print(f"Sending move: {move}")
        await self.send(text_data=json.dumps(move))

    async def game_loop(self):
        while True:
            await self.update_ball_position()
            await self.notify_clients()
            await asyncio.sleep(1)

    async def startGame(self):
        await self.add_player_channels()
        await self.game_loop()

class Command(BaseCommand):
    help = "Run the game state worker"

    async def send_game_state(self):
        user_ids = ["1", "2"]  # IDs dos jogadores, por exemplo
        game_session = GameSession(user_ids, "1234")

        try:
            await game_session.startGame()
        except asyncio.CancelledError:
            self.stdout.write(self.style.WARNING("Worker has been stopped."))

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting game state worker..."))
        
        # Garantir que existe um loop de eventos assíncrono
        loop = asyncio.get_event_loop()  # Obtém o loop de eventos
        loop.create_task(self.send_game_state())  # Cria a tarefa assíncrona
        loop.run_forever()  # Inicia o loop de eventos para que a tarefa continue em execução
