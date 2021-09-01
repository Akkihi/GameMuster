from django.db import models


class GameData(models.Model):
    id = models.UUIDField(primary_key=True)
    data = models.JSONField()
