import asyncio

from games_worker.listeners.game_maker_listener import GameMakerListener
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Run <session_worker> to start the game state worker."

    async def send_game_state(self):
        game_maker_listener = GameMakerListener()

        try:
            await game_maker_listener.listen()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Worker has been stopped. Waiting for pending tasks..."))
            await game_maker_listener.wait_for_tasks()
            self.stdout.write(self.style.SUCCESS("All tasks have been completed."))
        except asyncio.CancelledError:
            self.stdout.write(self.style.WARNING("Worker has been stopped."))
            await game_maker_listener.wait_for_tasks()

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting game state worker..."))
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(self.send_game_state())
            loop.run_forever()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Worker has been stopped."))
            loop.stop()
