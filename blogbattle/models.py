from django.db import models
from django.conf import settings  # Add this import

class Leaderboard(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use the proper way to reference User model
        on_delete=models.CASCADE, 
        null=True
    )
    score = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username or "Anonymous"