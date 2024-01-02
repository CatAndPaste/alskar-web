from django.db import models


class DiscordMessage(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=100)
    avatar_url = models.URLField()
    channel_id = models.BigIntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.author}: {self.content}"
