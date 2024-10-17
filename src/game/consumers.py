from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BasePlayer():
    def __init__(self, player_id, x, y):
        self._id = player_id
        self._x = x
        self._y = y
        self.height = 25
        self.width = 100

    def to_dict(self):
        return {
            "x": self._x,
            "y": self._y,
            "width": width,
            "height": height,
        }
    
    def move(self, op):
        self._y += op

class http_consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.x = 0
        self.y = 0
    
    async def disconnect(self, status_code):
        pass

    async def receive(self, text_data):
        message = text_data

        if message == 'j':
            player_two(-5)
        elif message == 'l':
            player_two(5)
        elif message == 'a':
            player_one(-5)
        elif message == 'd':
            player_one(5)

        response_data = {
            "player_one": player_one,
            "ball": {
                "x": 250,
                "y": 200,
                "radius": 10.0
            },
            "player_two": player_two,
        }

        response_json = json.dumps(response_data)
        await self.send(text_data=response_json) 
