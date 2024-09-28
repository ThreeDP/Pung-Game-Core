import asyncio
import websockets
import json


async def echo(websocket, path):
    x = 0
    y = 0
    async for message in websocket:
        print(f"Recebido: {message}")
        if (message == 's'):
            y += 5
        elif (message == 'w'):
            y -= 5
        elif (message == 'a'):
            x -= 5
        elif (message == 'd'):
            x += 5

        response_data = {
            "player_one": {
                "x": x,
                "y": 10,
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
        reponse_json = json.dumps(response_data)
        await websocket.send(reponse_json)

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("Servidor WebSocket está rodando na porta 8765...")
asyncio.get_event_loop().run_forever()