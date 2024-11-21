import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Adiciona o canal ao grupo e aceita a conexão
        await self.channel_layer.group_add("game_group", self.channel_name)
        await self.accept()

        # Inicia a tarefa em segundo plano
        self.game_state_task = asyncio.create_task(self.send_game_state())

    async def disconnect(self, close_code):
        # Remove o canal do grupo
        await self.channel_layer.group_discard("game_group", self.channel_name)
        
        # Cancela a tarefa em segundo plano
        if hasattr(self, 'game_state_task'):
            self.game_state_task.cancel()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        await self.channel_layer.group_send(
            "game_group",
            {
                "type": "chat_message",
                "message": message,
            }
        )

    async def player_move(self, event):
        move = event['move']
        print(f"Sending move: {move}")
        await self.send(text_data=json.dumps(move))