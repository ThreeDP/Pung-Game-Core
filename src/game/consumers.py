from channels.generic.websocket import AsyncWebsocketConsumer
import json

class Player:
    def __init__(self, player_id, x, y):
        self.id = player_id
        self.x = x
        self.y = y
        self.width = 25,
        self.height = 100,

    def move(self, direction):
        self.y += direction
    
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
    
player_one = Player(0, 50, 225)
player_two = Player(1, 500, 225)
ball = Ball()
movement_map = {
    'ArrowUp': -5,
    'ArrowDown': 5,
    'w': -5,
    's': 5
}

class http_consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = text_data

        if message in movement_map:
            if message in ['ArrowUp', 'ArrowDown']:
                player_two.move(movement_map[message])
            else:
                player_one.move(movement_map[message])

        response_data = {
            "player_one": player_one.to_dict(),
            "ball": ball.to_dict(),
            "player_two": player_two.to_dict(),
        }

        response_json = json.dumps(response_data)
        await self.send(text_data=response_json) 
