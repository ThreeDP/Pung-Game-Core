import json
import redis
import random
import asyncio

from channels.layers import get_channel_layer

# Game Settings imports
from gamesession.models.game_config import GameConfig, GameStatus
from gamesession.models.ball import Ball
from gamesession.models.player import Player

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class GameSession:
    def __init__(self, user_ids, gameId):
        self.game_status = GameStatus.PLAYING
        self.channel_layer = get_channel_layer()
        self.tasks_movement_player = []
        self.gameId = gameId
        self.game = f"game_session_{gameId}"
        
        self.players = {}
        for index, user_id in enumerate(user_ids):
            position = GameConfig.player_positions[index]
            self.players[user_id] = Player(user_id, position["x"], position["y"])

        self.ball = Ball()
        self.ball_direction = {
            "x": random.choice([-GameConfig.ball_speed, GameConfig.ball_speed]),
            "y": random.choice([-GameConfig.ball_speed, GameConfig.ball_speed])
        }

    async def add_player_channels(self):
        for player in self.players.values():
            self.tasks_movement_player.append(asyncio.create_task(self.process_player_move(player)))

    async def move_ball(self):
        self.ball.x += self.ball_direction["x"]
        self.ball.y += self.ball_direction["y"]
    
    async def check_screen_collision(self, y):
        if y <= 0 or y >= GameConfig.screen_height:
            self.ball_direction["y"] *= -1

    async def check_player_collision(self, x, y):
        for player in self.players.values():
            if player.x <= x <= player.x + player.width:
                if player.y <= y <= player.y + player.height:
                    self.ball_direction["x"] *= -1

    async def ball_reset(self):
        self.ball.x = GameConfig.screen_width // 2
        self.ball.y = GameConfig.screen_height // 2
        self.ball_direction = {
            "x": random.choice([-GameConfig.ball_speed, GameConfig.ball_speed]),
            "y": random.choice([-GameConfig.ball_speed, GameConfig.ball_speed])
        }
        asyncio.create_task(self.await_for_new_match())

    async def await_for_new_match(self):
        self.game_status = GameStatus.WAITING
        await asyncio.sleep(5)
        self.game_status = GameStatus.PLAYING

    async def update_ball_position(self):
        if self.game_status == GameStatus.PLAYING:
            ball_x = self.ball.x + self.ball_direction["x"]
            ball_y = self.ball.y + self.ball_direction["y"]
            
            await self.check_screen_collision(ball_y)
            await self.check_player_collision(ball_x, ball_y)
            if self.ball.x <= 0 or self.ball.x >= GameConfig.screen_width:
                await self.ball_reset()
                return

            await self.move_ball()

    async def notify_clients(self):
        response_data = {
            "ball": self.ball.to_dict(),
            "players": {user_id: player.to_dict() for user_id, player in self.players.items()},
        }

        await self.channel_layer.group_send(
            self.game,
            {
            "type": "game.update",
            "game_state": response_data,
            "expiry": 0.02
            }
        )
    
    async def process_player_move(self, player):
        queue_name = f"{self.game}_{player.user_id}"
        while True:
            await asyncio.sleep(0.005)
            try:
                message = redis_client.lpop(queue_name)
                if message is None:
                    continue
                data = json.loads(message)
                print(f"Mensagem processada para {queue_name}: {data}")

                move = data.get("move", {})
                player.y += move["direction"] * GameConfig.player_speed

            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
            except Exception as e:
                print(f"Erro ao processar mensagem: {e}")

    async def game_loop(self):
        while True:
            await self.update_ball_position()
            await self.notify_clients()
            await asyncio.sleep(0.02)

    async def startGame(self):
        await self.add_player_channels()
        await asyncio.create_task(self.await_for_new_match())
        await self.game_loop()