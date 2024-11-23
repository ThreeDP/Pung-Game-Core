import uuid

from django.db import models
from .game_model import GameModel

class PlayerModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False, unique=True, blank=False)
    gameId = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    is_connected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.id = self.id or str(uuid.uuid4())
        super(PlayerModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"Player {self.id} - Connected: {self.is_connected}"

    class Meta:
            db_table = 'Players'