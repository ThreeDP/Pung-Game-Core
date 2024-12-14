import redis
import json
import os

from games_worker.game_core.game_session import GameSession
from games_app.models.game_model import GameModel
from games_app.models.player_model import PlayerModel
from asgiref.sync import sync_to_async
import asyncio

redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=int(os.environ.get("REDIS_PORT", 6379)), db=0, decode_responses=True)

class GameMakerListener:
    def __init__(self):
        self.game_sessions = {}
        self.queue_name = "create-game-queue"
        self.running_tasks = set()

    async def create_game(self, message):
        data = json.loads(message)
        game_session = await sync_to_async(GameModel.objects.create)(
            status=0, roomId=data["roomId"], isSinglePlayer=data["isSinglePlayer"], created_by=data["ownerId"]
        )
        
        players = []
        for player in data["players"]:
            players.append({"id": player["id"], "color": player["color"]})
            try:
                await sync_to_async(PlayerModel.objects.create)(id=player["id"],name=player["name"], gameId=game_session, color=player["color"])
            except:
                return
        try:
            await sync_to_async(game_session.save)()
        except:
            return

        game_job = GameSession(players, game_session.id, data["roomId"])
        self.game_sessions[data["roomId"]] = game_job
        task = asyncio.create_task(game_job.startGame())
        self.running_tasks.add(task)
        task.add_done_callback(self.running_tasks.discard)
        return game_job
    
    async def listen(self):
        while True:
            await asyncio.sleep(1)
            message = redis_client.lpop(self.queue_name)
            if message is None:
                continue
            await self.create_game(message)

    async def wait_for_tasks(self):
        if self.running_tasks:
            await asyncio.wait(self.running_tasks)