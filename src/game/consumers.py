import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from collections import deque

# Constantes do jogo
PADDLE_SPEED = 10
BALL_SPEED = 5  # A velocidade da bola (ajuste conforme necessário)
GAME_WIDTH = 850  # Largura da área de jogo
GAME_HEIGHT = 550  # Altura da área de jogo

# Estado do jogo
class Player:
    def __init__(self, player_id, x, y):
        self.id = player_id
        self.x = x
        self.y = y
        self.width = 25
        self.height = 100

    def move(self, direction):
        new_y = self.y + direction
        if 0 <= new_y <= GAME_HEIGHT - self.height:  # Previne o movimento para fora da tela
            self.y = new_y
    
    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }

class Ball:
    def __init__(self):
        self.x = 275
        self.y = 275
        self.radius = 10.0

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "radius": self.radius,
        }

player_one = Player(0, 25, 225)
player_two = Player(1, 800, 225)
ball = Ball()

movement_map = {
    'ArrowUp': -PADDLE_SPEED,
    'ArrowDown': PADDLE_SPEED,
    'w': -PADDLE_SPEED,
    's': PADDLE_SPEED
}

class GameState:
    def __init__(self):
        self.ball_direction = {"x": BALL_SPEED, "y": BALL_SPEED}  # Direção da bola
        self.players = [player_one, player_two]
        self.ball = ball
        self.clients = deque()  # Lista de clientes conectados

    async def update_ball_position(self):
        # Atualizar a posição da bola
        self.ball.x += self.ball_direction["x"]
        self.ball.y += self.ball_direction["y"]

        # Verificar colisão com as paredes superior e inferior
        if self.ball.y <= 0 or self.ball.y >= GAME_HEIGHT:
            self.ball_direction["y"] *= -1  # Inverter a direção no eixo Y

        # Verificar colisão com os jogadores
        for player in self.players:
            if player.x <= self.ball.x <= player.x + player.width:
                if player.y <= self.ball.y <= player.y + player.height:
                    self.ball_direction["x"] *= -1  # Inverter a direção no eixo X

        # Verificar se a bola saiu da tela
        if self.ball.x <= 0 or self.ball.x >= GAME_WIDTH:
            self.ball.x = GAME_WIDTH // 2  # Resetar a bola para o centro
            self.ball.y = GAME_HEIGHT // 2  # Resetar a posição Y para o centro
            self.ball_direction = {"x": BALL_SPEED, "y": BALL_SPEED}

    async def notify_clients(self):
        # Enviar as atualizações para todos os clientes conectados
        response_data = {
            "player_one": player_one.to_dict(),
            "ball": self.ball.to_dict(),
            "player_two": player_two.to_dict(),
        }
        response_json = json.dumps(response_data)

        # Enviar os dados para todos os clientes
        for client in self.clients:
            await client.send(text_data=response_json)

    async def game_loop(self):
        while True:
            await self.update_ball_position()
            await self.notify_clients()
            await asyncio.sleep(0.02)  # Atualizar a cada 0.02 segundos (50fps)

# Instância global do estado do jogo
game_state = GameState()

class http_consumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Adiciona o cliente à lista de clientes conectados
        game_state.clients.append(self)
        await self.accept()

        # Inicia o loop do jogo se for o primeiro cliente
        if len(game_state.clients) == 1:
            asyncio.create_task(game_state.game_loop())

    async def disconnect(self, close_code):
        # Remove o cliente da lista de clientes conectados
        game_state.clients.remove(self)

    async def receive(self, text_data):
        message = text_data

        if message in movement_map:
            if message in ['ArrowUp', 'ArrowDown']:
                player_two.move(movement_map[message])
            else:
                player_one.move(movement_map[message])

        # Não envia nada individualmente, pois a bola e os jogadores são atualizados periodicamente
