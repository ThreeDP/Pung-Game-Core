import json
import redis
import random
import asyncio

from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async


# Game Settings imports
from games_worker.utils.game_config import GameConfig, GameStatus
from games_worker.utils.ball import Ball
from games_worker.utils.player import Player
from games_app.models.game_model import GameModel

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class GameSession:
    def __init__(self, players, gameId, roomId):
        self.game_status = GameStatus.PLAYING
        self.roomId = roomId
        self.channel_layer = get_channel_layer()
        self.tasks_movement_player = []
        self.gameId = gameId
        self.game = f"game_session_{gameId}"
        
        self.players = {}
        for index, player in enumerate(players):
            position = GameConfig.player_positions[index]
            self.players[player["id"]] = Player(player["id"], player["color"], position["x"], position["y"])

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
            "players": {player.color: player.to_dict() for player in self.players.values()},
        }
        json_response = json.dumps(response_data)

        await self.channel_layer.group_send(
            self.game,
            {
            "type": "game.update",
            "game_state": json_response,
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
        print("Game loop started")
        while True:
            await self.update_ball_position()
            await self.notify_clients()
            await asyncio.sleep(0.02)

    async def send_message_game_start(self):
        queue_name = f"room_{self.roomId[:8]}"
        print(f"Sending message game start {queue_name}")
        await self.channel_layer.group_send(
            queue_name,
            {
            "type": "game.started",
            "gameId": self.gameId,
            "expiry": 0.02
            }
        )

        game = await sync_to_async(GameModel.objects.filter(id=self.gameId).first)()
    
        while True:
            all_players_connected = 0
            players = await sync_to_async(list)(game.players.all())
            for player in players:
                if player.is_connected == True:
                    all_players_connected += 1
            if all_players_connected == 2:
                break
            await asyncio.sleep(2)
        ##game.status = 1
        #game.save()

    async def startGame(self):
        print("Game started")
        await self.add_player_channels()
        await self.send_message_game_start()
        #await asyncio.create_task(self.await_for_new_match())
        await self.game_loop()