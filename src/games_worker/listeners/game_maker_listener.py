import redis
import json

from games_worker.game_core.game_session import GameSession
from games_app.models.game_model import GameModel
from games_app.models.player_model import PlayerModel
from asgiref.sync import sync_to_async
import asyncio

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class GameMakerListener:
    def __init__(self):
        self.game_sessions = {}
        self.queue_name = "create-game-queue"

    async def create_game(self, message):
        data = json.loads(message)
        game_session = await sync_to_async(GameModel.objects.create)(status=0, roomId=data["roomId"], created_by=data["ownerId"])
        
        players = []
        for player in data["players"]:
            players.append({"id": player["id"], "color": player["color"]})
            await sync_to_async(PlayerModel.objects.create)(id=player["id"], gameId=game_session, color=player["color"])
        
        await sync_to_async(game_session.save)()

        game_job = GameSession(players, game_session.id, data["roomId"])
        self.game_sessions[data["roomId"]] = game_job
        asyncio.create_task(game_job.startGame())
        return game_job
    
    async def listen(self):
        while True:
            await asyncio.sleep(1)
            message = redis_client.lpop(self.queue_name)
            if message is None:
                continue
            await self.create_game(message)
        

