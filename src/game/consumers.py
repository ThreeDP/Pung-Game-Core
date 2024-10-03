from channels.generic.websocket import AsyncWebsocketConsumer
import json

class http_consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.x = 0
        self.y = 0
    
    async def disconnect(self, code):
        pass

    async def receive(self, data):
        message = data

        if message == 's':
            self.y += 5
        elif message == 'w':
            self.y -= 5
        elif message == 'a':
            self.x -= 5
        elif message == 'd':
            self.x += 5

        response_data = {
            "player_one": {
                "x": self.x,
                "y": self.y,
                "width": 100,
                "height": 25,
            },
            "ball": {
                "x": 250,
                "y": 200,
                "radius": 10.0
            },
            "player_two": {
                "x": 250,
                "y": 365,
                "width": 100,
                "height": 25,
            },
        }

        response_json = json.dumps(response_data)
        await self.send(text_data=response_json) 
