import uuid

from django.db import models
from .game_model import  GameModel
from .player_model import PlayerModel

class ScoreModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False, unique=True, blank=False)
    playerId = models.ForeignKey(PlayerModel, on_delete=models.CASCADE)
    gameId = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.id = self.id or str(uuid.uuid4())
        super(ScoreModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"Score {self.id} - Player: {self.playerId.id} - Score: {self.score}"

    class Meta:
            db_table = 'Scores'