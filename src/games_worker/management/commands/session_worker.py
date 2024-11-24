import asyncio

from games_worker.listeners.game_maker_listener import GameMakerListener
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Run the game state worker"

    async def send_game_state(self):
        game_maker_listener = GameMakerListener()

        try:
            await game_maker_listener.listen()
        except asyncio.CancelledError:
            self.stdout.write(self.style.WARNING("Worker has been stopped."))

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting game state worker..."))
        
        # Garantir que existe um loop de eventos assíncrono
        loop = asyncio.get_event_loop()  # Obtém o loop de eventos
        loop.create_task(self.send_game_state())  # Cria a tarefa assíncrona
        loop.run_forever()  # Inicia o loop de eventos para que a tarefa continue em execução
